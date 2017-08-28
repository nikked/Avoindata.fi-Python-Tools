### TODO

* Kaynti ja postiosoite
* Rekisterointi paikkakunnat
	* BisCompanyRegisteredOffice

	
* Only take addresses with type 1 (active most recent address)
* Yhteystiedot (version 1)
	* puh nro
	* kotisivu 
* Liquidations	

 Melko kovalla kädellä olette karsineet tietoja. Osoitteiden osalta tein pienen pistokokeen - BisAddress version (integer): Yksi tarkoittaa nykyistä versiota ja >1 historiallisia osoitteita. Esim. 2443455-9 osoitteena on Helsinki mutta siinä on version = 2 (=vanha osoite). Yksi eli uudempi osoite on Espoon. Myös Kaupparekisterin kuulutustiedot näyttävät Espoota http://avoindata.prh.fi/opendata/tr/v1/2443455-9 Näköjään prh api oikuttelee juuri nyt, niin en pääse tarkistamaan vastaavaa bis-apia.

 Jos karsia halutaan, niin se on ihan ok. Mukaan ottaisin kuitenkin ainakin viimeiset osoitetiedot (TYPE,Osoitteen laji, käyntiosoite 1 , postiosoite 2 ) lisäksi yrityksen kotipaikan selvittelyjen takia myös ehkä rekisteröinti paikkakunnat ja yhteystiedot, joista löytyy mm. puhelinnumerot ja mahdollisesti kotisivu. Version -kentän arvo pitää noissakin huomioida eli version=1. Lisäksi jos löytyy liquidations-tietoja niin ne olisi hyvä huomioida. Esim. 0616325-7 "version" : 1,
"description" : "Konkurssissa",
"type" : "KONK"....... --> En päässyt tarkistamaan tätäkään bis-apista eli YTJ -tiedoista.Toisin sanoen näkyi omista aiemmin poimituista.


# Avoindata.fi: Python tools
> A collection of Python scripts helping to generate some open data packages for https://www.avoindata.fi/fi

## PRH COMPANY REGISTER
> https://avoindata.prh.fi/ytj.html

* Scripts that get the data of all active Finnish companies of the following company forms:
	* limited liability companies
	* public limited companies
	* housing companies
	* co-operatives
	* insurance companies
	* public insurance companies
* Output formats:
	* csv
	* json

### scripts/prh/get_prh_data.py
> Note that running this scripts takes days in its full extent. This is because PRH has limited the usage of their API to 300 queries per minute total for all users. The size of the total dataset is almost 3 GB

* A script that gets data from PRH's company API from 1978 to 2017
* It makes a query based on the following parameters:
	1. A company registration time period defined as one month
	2. Business line code as defined by Statistics Finland:
	http://tilastokeskus.fi/meta/luokitukset/toimiala/001-2008/index_en.html
* The data is saved on: data/json/prh_data


### scripts/prh/make_csv_of_prh_data.py
* A script that iterates through all the json files downloaded by the get_prh_data.py and makes a csv of them
* Companies that do not exist anymore are ignored. These are identified by finding a trade register note with the description 'Ceased' or 'Lakannut' (in Finnish).

### Identifying changes to companies
* Newly registered companies can be identified by running the get_prh_data.py script for the current period
* Lately ceased companies can be identified by querying the 'Finnish trade register's public notices' API: https://avoindata.prh.fi/tr_en.html


## POSTCODES
> Scripts related to the postcodes open data set found in https://www.avoindata.fi/data/fi/dataset/postcodes

* Two functionalities
	1. transforms .opt files to the more common .csv format from the dataset: https://www.avoindata.fi/data/fi/dataset/rakennusten-osoitetiedot-koko-suomi
	2. appends the globally common WGS84 coordinates to the data in addition to the Finnish ETRS standard

### scripts/postcodes/opt_to_csv.py
* This script is the real work horse. It reads OPT's and outputs csv with the WGS coordinates appended

### scripts/postcodes/find_mismatching_data.py
* A script that finds erroneous data in the original dataset
* It searches for lacking:
	* Postcodes
	* Municipalities
	* Provinces
	* Addresses

### scripts/postcodes/locations_converters.py
* functions for handling multiple files at once and a geo conversion accuracy tester



## LIITYNTAKATALOGI
> A script that gets the amount of connections organizations have to the National Data Exchange Layer (KAPA)

### scripts/liityntakatalogi.py
* This scripts scrapes the liityntakatalogi website and writes the amount of connections to an CSV file
