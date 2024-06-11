#!/usr/bin/env python

from  adslibraries import bibtex_to_ads_libraries, ads_libraries_to_bibtex
from click.testing import CliRunner

test_str='''@article{D'Ai2017,
 adsnote = {Provided by the SAO/NASA Astrophysics Data System},
 adsurl = {https://ui.adsabs.harvard.edu/abs/2017MNRAS.470.2457D},
 archiveprefix = {arXiv},
 author = {{D'A{\`\i}}, A. and {Cusumano}, G. and {Del Santo}, M. and {La Parola}, V. and {Segreto}, A.},
 doi = {10.1093/mnras/stx1146},
 eprint = {1705.03404},
 journal = {\mnras},
 keywords = {line: formation - line: identification, stars: individual: (4U 1626-67) - X-rays: binaries, X-rays: general, Astrophysics - High Energy Astrophysical Phenomena},
 month = sep,
 number = {2},
 pages = {2457-2468},
 primaryclass = {astro-ph.HE},
 title = {{A broad-band self-consistent modelling of the X-ray spectrum of 4U 1626-67}},
 volume = {470},
 year = {2017}
}

@article{Vybornov2018,
 adsnote = {Provided by the SAO/NASA Astrophysics Data System},
 adsurl = {https://ui.adsabs.harvard.edu/abs/2018A&A...610A..88V},
 archiveprefix = {arXiv},
 author = {{Vybornov}, V. and {Doroshenko}, V. and {Staubert}, R. and {Santangelo}, A.},
 doi = {10.1051/0004-6361/201731750},
 eid = {A88},
 eprint = {1801.01349},
 journal = {\\aap},
 keywords = {X-rays: binaries, stars: magnetic field, pulsars: individual: V 0332+53, accretion, accretion disks, Astrophysics - High Energy Astrophysical Phenomena},
 month = mar,
 pages = {A88},
 primaryclass = {astro-ph.HE},
 title = {{Changes in the cyclotron line energy on short and long timescales in V 0332+53}},
 volume = {610},
 year = {2018}
}
'''


def test_upload_download():
    with open('test.bib', 'w') as ff:
        ff.write(test_str)

    runner = CliRunner()

    runner.invoke(bibtex_to_ads_libraries, ['test.bib', 'test1'])
    runner.invoke(ads_libraries_to_bibtex, ['test1.bib', 'test1'])


    f1 = open("test.bib", "r") 
    f2 = open("test1.bib", "r") 
    
    f1_data = f1.readlines()
    f2_data = f2.readlines()
    
    comparison=True

    for i, (line1, line2) in enumerate(zip(f1_data, f2_data)):
        # matching line1 from both files
        if line1 == line2: 
            #print("Line ", i, ": IDENTICAL")
            pass
        else:
            comparison=False
            print("Line ", i, ":")
            # else print that line from both files
            print("\tFile 1:", line1, end='')
            print("\tFile 2:", line2, end='')
    
    if comparison:
        print('Test is successful')

    # closing files
    f1.close()                                      
    f2.close()  

    assert comparison, "Files differ !"