#!/usr/bin/env python
# coding: utf-8

import requests
import os, sys, math
import unidecode
import bibtexparser
import click

import logging

stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler]
logging.basicConfig(level=logging.INFO, format=' %(message)s', handlers=handlers)

logger = logging.getLogger(__name__)

class ads_library(object):

    def __init__(self, max_authors=11):

        self.config = self.get_config()
        self.url = self.config['url'] + '/libraries'
        self.payload = self.config['headers']
        r = requests.get(self.url, headers=self.payload)
        self.libraries = r.json()['libraries']

        self.max_authors = max_authors

        logger.info("These are your ADS libraries:")
        for l in self.libraries:
            logger.info("%s %s" % (l['name'], l['id']))
        logger.info("")
    def get_config(self):
        """
        Load ADS developer key from file
        :return: str
        """

        try:
            with open(os.path.expanduser(os.environ['HOME']+'/.ads/dev_key')) as f:
                token = f.read().strip()
        except IOError:
            logger.error('The script assumes you have your ADS developer token in the'
                  'folder: {}'.format(os.environ['HOME']+'/.ads/dev_key'))

        return {
            'url': 'https://api.adsabs.harvard.edu/v1/biblib',
            'headers': {
                'Authorization': 'Bearer:{}'.format(token),
                'Content-Type': 'application/json',
            }
        }


    def get_library(self, library_id, num_documents):
        """
        Get the content of a library when you know its id. As we paginate the
        requests from the private library end point for document retrieval,
        we have to repeat requests until we have all documents.
        :param library_id: identifier of the library
        :type library_id:
        :param num_documents: number of documents in the library
        :type num_documents: int
        :return: list
        """

        start = 0
        rows = 25
        num_paginates = int(math.ceil(num_documents / (1.0*rows)))

        documents = []
        for i in range(num_paginates):
            logger.debug('Pagination {} out of {}'.format(i+1, num_paginates))

            r = requests.get(
                '{}/libraries/{id}?start={start}&rows={rows}'.format(
                    self.config['url'],
                    id=library_id,
                    start=start,
                    rows=rows
                ),
                headers=self.config['headers']
            )

            # Get all the documents that are inside the library
            try:
                data = r.json()['documents']
            except ValueError:
                raise ValueError(r.text)

            documents.extend(data)

            start += rows

        return documents


    def get_libraries(self, library_names=['all']):
        """Get all your ADS libraries and store them in self.all_libraries.
        If librariy names is not "all" it will store only the libraries matching the names

        Args:
            library_names (list, optional): if all, gett all libraries otherwise, the ones matching the names. Defaults to ['all'].
        """        
        all_libraries = []
        for l in self.libraries:
            for library_name in library_names:
                if l['name'] == library_name or library_name == 'all':
                    logger.debug("%s %s" %(l['name'], l['id']))
                    r = requests.get(self.url+'/'+l['id'], headers=self.payload)
                    all_libraries.append(r.json())
    
        self.all_libraries = all_libraries
        

    def get_all_export(self):
        export_url = self.config['url'] .replace('biblib', 'export/bibtex')

        all_library_documents = []
        for library in self.all_libraries:
            library_documents = self.get_library(library['metadata']['id'], library['metadata']['num_documents'])
            all_library_documents.append(library_documents)

        import itertools

        all_library_documents = list(itertools.chain.from_iterable(all_library_documents))
        logger.debug(all_library_documents)
        parameters = {'bibcode' : all_library_documents,
                      'maxauthor' : self.max_authors,
                      'keyformat' : "%1H%Y",
                      "sort":  "pubdate asc"
                      }

        r = requests.post(export_url, headers=self.payload, json=parameters)

        return r.json()


    def get_all_papers(self, fields = 'year,doi,first_author,bibcode,bibstem,pub,doctype,abstract,title,volume,pubdate,page,issue,author,citation_count,date,aff'):
        """gets all papers from the selected libraries with the fields defined in fields

        Args:
            fields (str, optional): ields to be retrieved from ADS. Defaults to 'year,doi,first_author,bibcode,bibstem,pub,doctype,abstract,title,volume,pubdate,page,issue,author,citation_count,date,aff'.
        """        
        search_url = self.config['url'] .replace('biblib', 'search/query')

        all_papers = []
        for library in self.all_libraries:
            library_documents = self.get_library(library['metadata']['id'], library['metadata']['num_documents'])
            for bibcode in library_documents:
                parameters = {'q': 'bibcode:%s' % bibcode, 'fl': fields}
                r = requests.get(search_url, headers=self.payload, params=parameters)
                all_papers.append(r)

        self.all_papers = all_papers

    @staticmethod
    def convert_list(vv):
        """apply unidecode to the string in the list or to the string
            It also replaces { and } with null

        Args:
            vv (list or str): list or string to be cleaned

        Returns:
            str: string without unicode characters and list joined using spaces
        """        
        if isinstance(vv, list):
            clean_vv = ' '.join(unidecode.unidecode(vv))
        else:
            clean_vv = unidecode.unidecode(vv)
        if isinstance(clean_vv, str):
            clean_vv = clean_vv.replace('{', '').replace('}','')
        return clean_vv
    
    def load_papers_from_bibtex(self, bibtex_fname):
        """Load the paper from a bitex file into self.all_papers

        Args:
            bibtex_fname (str): name of the file to load

        Raises:
            Exception: file not existing

        Returns:
            int: zero if success
        """        

        if not os.path.isfile(bibtex_fname):
            raise Exception(f'The file {bibtex_fname} does not exist')

        with open(bibtex_fname) as bibtex_file:
            self.all_papers = bibtexparser.load(bibtex_file).entries
        
        return 0


    def add_papers_to_ads_library(self, library_name, bibtex_fname):

        self.get_libraries([library_name])
        if len(self.all_libraries) == 0:
            raise BaseException(f'The library {library_name} does not exist in your ADS')
        
        self.load_papers_from_bibtex(bibtex_fname)
        bibcodes = []
        for ee in self.all_papers:
            bibcode = ads_library.get_bibcode(ee)
            if bibcode is not None:
                bibcodes.append(bibcode)
        
        if len(bibcodes)>0:
            parameters = {'bibcode': bibcodes, 'action' : 'add'}
            r = requests.post(
            '{}/documents/{id}'.format(
                self.config['url'],
                id=self.all_libraries[0]['metadata']['id']
            ),
            headers=self.config['headers'],
            json=parameters)
            print(r.text)

        return 0

    @staticmethod
    def get_bibcode(entry):
        if 'adsurl' in entry:
            return entry['adsurl'].split('/')[-1].replace('}','')
        else:
            return None

    def clean_dict(self, ads_entry):
        """Cleans the dictionary of ADS entries

        Args:
            ads_entry (disctionary ): ADS entry

        Returns:
             entry_id, entry_type, clean_dict
            two strings and one dictionary:  
        """        
        clean_dict = {}
        vv = ads_entry['doctype']
        if vv == 'eprint' or vv == 'circular' or vv == 'newsletter':
            vv = 'article'
        entry_type = vv
        for kk, vv in ads_entry.items():
            if kk == 'author':
                if len(vv) > self.max_authors:
                    vv = vv[0:self.max_authors+1]+['et al.']
                new_author = " and ".join([ self.abbreviate_name(n) for n in vv])
                clean_dict.update({kk: new_author})
                entry_id = unidecode.unidecode(vv[0].split(',')[0].replace(' ',''))+ads_entry['year']
            elif kk == 'doctype':
                continue

            elif kk == 'bibstem':
                clean_vv = vv[0].replace('&','\\&')
                if clean_vv == 'arXiv':
                    clean_vv = 'arXiv e-prints'
                clean_dict.update({'journal': clean_vv})
            elif kk == 'page':
                clean_dict.update({'pages': self.convert_list(vv)})
            elif kk == 'pub' and entry_type == 'inproceedings':
                clean_dict.update({'booktitle': self.convert_list(vv)})
            elif kk == 'aff' and entry_type == 'phdthesis':
                clean_dict.update({'school': self.convert_list(vv)})
            elif kk == 'aff':
                continue
            elif kk == 'abstract' or kk == 'title':
                clean_dict.update({kk: "\"%s\"" % self.convert_list(vv)})
            else:
                clean_dict.update({kk: self.convert_list(vv)})

        return entry_id, entry_type, clean_dict

    @staticmethod
    def abbreviate_name(name):

        nn = name.split(',')
        new_name = '{%s}' % nn[0]
        #print(nn)
        if len(nn)>1:
            nn1 = nn[1].split()
            new_name += ', ' + nn1[0][0]+'.'
            if len(nn1) > 1:
                for x in nn1[1:]:
                    new_name += ' ' + x
        return new_name

    def create_bib_entries_from_export(self):

        exported = self.get_all_export()

        try:
            export_str = exported['export']
        except KeyError:
            raise('ADS exported dict is ' + str(exported))

        logger.debug("bibtex string : %s" % export_str)

        bib_parser = bibtexparser.bparser.BibTexParser(interpolate_strings=False)
        bib_entries = bib_parser.parse(export_str)

        logger.info("These are the bibtex entries that we are about to save\n**************************")
        new_bib_database_entries = self.clean_id(bib_entries.entries)
        bib_entries.entries = new_bib_database_entries
        logger.info('**************************\n')

        self.bib_entries = bib_entries


    def create_bib_entries(self):
        bib_entries = bibtexparser.bparser.BibTexParser(interpolate_strings=True)

        for r in self.all_papers:
            entry_id, entry_type, cleaned_dict = self.clean_dict(r.json()['response']['docs'][0])
            logger.debug(entry_id + ' ' + entry_type)
            bib_entries._add_entry(entry_id=entry_id, entry_type=entry_type, fields=cleaned_dict)

        logger.info("These are the bibtex entries that we are about to save\n**************************")
        new_bib_database_entries = self.clean_id(bib_entries.bib_database.entries)
        bib_entries.bib_database.entries = new_bib_database_entries
        logger.info('**************************\n')

        self.bib_entries = bib_entries.bib_database

    @staticmethod
    def clean_id(entries):

        ads_export = True
        keys = entries[0].keys()
        if 'date' in keys and 'bibcode' in keys:
            ads_export = False

        if ads_export:
            ordered_entries = sorted(entries, key=lambda k: "%s%s" % (k['ID'], k['adsurl']))
        else:
            ordered_entries = sorted(entries, key=lambda k: "%s%s" % (k['ID'], k['date']))

        #order list by ID
        old_id = '0'
        numb = 1
        start = ord('a') - 1
        for entry in ordered_entries:
            if entry['ID'] == old_id:
                logger.debug("Changing the ID for duplication")
                entry['ID'] = entry['ID'] + chr(start + numb)
                numb += 1
            else:
                numb = 1
                old_id = entry['ID']
            if ads_export:
                logger.info('%s %s' % (entry['ID'], entry['title']))
            else:
                logger.info('%s %s %s' % (entry['ID'], entry['title'], entry['bibcode']))

        #add a letter to a an n-th occurency
        #order list by bibcode
        #remove duplicated bibcode

        if ads_export:
            key = 'adsurl'
        else:
            key = 'bibcode'

        cleaned_entries = sorted(entries, key=lambda k: k[key])
        old_bibcode = '0'
        to_be_deleted = []
        for i, entry in enumerate(cleaned_entries):
            if entry[key] == old_bibcode:
                logger.debug(f'Delete {old_bibcode}')
                to_be_deleted.append(i)
            old_bibcode = entry[key]
        to_be_deleted.reverse()
        logger.debug(to_be_deleted)
        for ii in to_be_deleted:
            logger.debug(ii, cleaned_entries[ii]['title'], cleaned_entries[ii-1]['title'])
            logger.debug(ii, cleaned_entries[ii][key], cleaned_entries[ii-1][key])
            del cleaned_entries[ii]

        return cleaned_entries

    def write_bibtex_file(self, output_filename='ads.bib'):
        from bibtexparser.bwriter import BibTexWriter
        writer = BibTexWriter()
        with open(output_filename, 'w') as bibtex_file:
            bibtex_file.write(writer.write(self.bib_entries))


@click.command()
@click.argument("bibtex_file", nargs=1) #, help="Name of the bibtex file to load"
@click.argument("library_name", nargs=1) #, help="Name of library to update (it must exist)"

def bibtex_to_ads_libraries(bibtex_file, library_name):

    """Upload the content of a bibtex file into a personal library

    update_ads_library bibtex_files library_names

    bibtex_files  STRING Name of the bibtex file to load
    library_name STRING Name of libraries to upload (it must exist)
    
    NB : Note that you need to save you ADS key () in %s/.ads/dev_key
    """ % os.environ['HOME']

    library_obj = ads_library()

    library_obj.add_papers_to_ads_library(library_name, bibtex_file)


@click.command()
@click.argument("bibtex_file", nargs=1) #, help="Name of the bibtex file to save"
@click.argument("library_names", nargs=-1) #, help="Names of libraries to export: all saves all"
@click.option("--max_authors", default=11,
              help="Maximum number of authors to save in the bibtex file")
@click.option("--use_ads_export/--do_not_use_ads_export", default=True,
              help="Use export to bibtex in ADS or custom-written parser")

def ads_libraries_to_bibtex(bibtex_file, library_names, max_authors,use_ads_export):

    """Saves the personal ADS libraries into a bibtex file

    save_ads_libraries bibtex_files library_names

    bibtex_files  STRING Name of the ADS file to save
    library_names STRINGS Names of libraries to save: "all" saves them all
    
    NB : Note that you need to save you ADS key () in %s/.ads/dev_key
    """ % os.environ['HOME']

    library_obj = ads_library(max_authors=max_authors)

    library_obj.get_libraries(library_names=library_names)

    if use_ads_export:
        library_obj.create_bib_entries_from_export()
    else:
        library_obj.get_all_papers()
        library_obj.create_bib_entries()


    library_obj.write_bibtex_file(bibtex_file)

if __name__ == "__main__":
    ads_libraries_to_bibtex()


