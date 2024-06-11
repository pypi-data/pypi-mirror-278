# adslibraries

__CAUTION__: this is a simple functional project, although it should work as generally expected

It saves your personal ads libraries (https://ui.adsabs.harvard.edu/user/libraries/)
into a bibtex file that can be used in latex
It saves bibtex citation keys as "FirstAuthorYear" (e.g. Ferrigno2017)
If not unique, it adds a letter to the other occurrencies (e.g. Ferrigno2017, Ferrigno2017a)

It is possible to choose a set of personal libraries or "all".

*You need to store your ADS tocken into the file $HOME/.ads/dev_key* 
*see* https://ui.adsabs.harvard.edu/user/settings/token

## Source of methods
https://github.com/adsabs/adsabs-dev-api/blob/master/Libraries_API.ipynb

## Installation
```bash
$ pip install ads-libraries
$ python setup.py install
```
## Help
```bash
$ save_ads_libraries --help
```

## Example:
```bash
$ save_ads_libraries my_ads.bib all
```