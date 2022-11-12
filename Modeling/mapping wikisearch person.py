#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
import time, sys

from os.path import exists
from time import sleep
from urllib.error import HTTPError
import os

streetnames = pd.read_csv('spacy_out.csv', encoding='UTF-8-SIG', sep=';')
streetnames.head()

streetnamesDe = streetnames[streetnames["STN_LANG"] == "de"]

streetnamesDe = streetnamesDe[["STR_ESID", "STN_LABEL_FINAL"]]

personLabels = ['wikiQLabel', 'wikiQ', 'givenname', 'familyname', 'sex', 'birth', "death", "placebirth", "placedeath", "image"]
streetnamesDeTempl = streetnamesDe.reindex(columns = streetnamesDe.columns.tolist() + personLabels)



workfile = "mapping wiki person_out.csv"
if exists(workfile):
    streetnamesDeWork = pd.read_csv(workfile, encoding='UTF-8-SIG', sep=';').drop("Unnamed: 0", axis = 1)
else:
    streetnamesDeTempl.to_csv(workfile, encoding='UTF-8-SIG', sep=';')
    streetnamesDeWork = streetnamesDeTempl.copy()


streetnamesDeWork = streetnamesDeWork.sort_values(["STR_ESID"])

findLastChecked = streetnamesDeWork.dropna(subset=["wikiQLabel"])

findLastChecked = findLastChecked.sort_values(["STR_ESID"], ascending = False)


lastCheckedESID = 0

if len(findLastChecked.index) > 0:
    lastCheckedESID = findLastChecked['STR_ESID'].loc[findLastChecked.index[0]]
    
print("Last Check ESDI:", lastCheckedESID)



wdUrl = "https://query.wikidata.org/sparql"
user_agent = 'Streetnamequery/1.0 (https://github.com/CaptainInler/cassda-zertifikatsarbeit)'
sparql = SPARQLWrapper(wdUrl, agent=user_agent)



def queryPeopleName(sparql, subject):
    #print(wdKey)
    query = """
    SELECT ?subject ?subjectLabel ?givennameLabel ?familynameLabel ?sexLabel ?birth ?death ?placebirth ?placedeath ?imageLabel
    WHERE {
      hint:Query hint:optimizer "None".
      SERVICE wikibase:mwapi {
        bd:serviceParam wikibase:api "EntitySearch";
                        wikibase:endpoint "www.wikidata.org";
                        mwapi:search "%s";
                        mwapi:language "de".
        ?subject wikibase:apiOutputItem mwapi:item .
      }
      ?subject wdt:P31 wd:Q5.
      OPTIONAL {?subject wdt:P735 ?givenname;}
      OPTIONAL {?subject wdt:P734 ?familyname;}
      OPTIONAL {?subject wdt:P21 ?sex;}
      OPTIONAL {?subject wdt:P569 ?birth;}
      OPTIONAL {?subject wdt:P570 ?death;}
      OPTIONAL {?subject wdt:P19 ?placebirth;}
      OPTIONAL {?subject wdt:P20 ?placedeath;}
      OPTIONAL {?subject wdt:P18 ?image.}
      SERVICE wikibase:label { bd:serviceParam wikibase:language "de" . }   
    }
    LIMIT 1 
    """ % (subject)
    #print(query)
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql



i = 0
z=0
total = int(len(streetnamesDeWork.index))

        
for x in streetnamesDeWork.index:
    esid = streetnamesDeWork['STR_ESID'][x]
    #print(f"\t{esid}",end="\r")




    if int(esid) > lastCheckedESID:
        i+=1
    else:
        z+=1
        #print(z)
        continue
        
    #print(i)
    subject = streetnamesDeWork['STN_LABEL_FINAL'][x]
    #print(f"Subjekt: {subject}")

    sparql = queryPeopleName(sparql, subject)
    
    try:
        results = sparql.query()
        #print(results.info())
    except HTTPError as e:
        print(f"{i} Anfragen ausgeführt")
        #Prüfen auf Statuscode 429 (Too many Requests)
        if e.status == 429:
            print(f'Statuscode 429 aufgetreten: Anfrage geht in {e.headers.get("retry-after")}sec weiter')
            sleep(int(e.headers.get("retry-after"))+2)
            i-=1
            continue
        else:
            raise

    result = results.convert()
    #print(result)
    results_df = pd.json_normalize(result['results']['bindings'])
    #print(results_df)
    
    if not results_df.empty:
               
        STR_ESID = streetnamesDeWork['STR_ESID'][x]
        STN_LABEL_FINAL = streetnamesDeWork['STN_LABEL_FINAL'][x]
        wikiQ = results_df['subject.value'][0]
        wikiQLabel = results_df['subjectLabel.value'][0]
        givenname = results_df['givennameLabel.value'][0] if 'givennameLabel.value' in results_df else np.nan
        familyname = results_df['familynameLabel.value'][0] if 'familynameLabel.value' in results_df else np.nan
        sex = results_df['sexLabel.value'][0] if 'sexLabel.value' in results_df else np.nan
        birth = results_df['birth.value'][0] if 'birth.value' in results_df else np.nan
        death = results_df['death.value'][0] if 'death.value' in results_df else np.nan
        placebirth = results_df['placebirth.value'][0] if 'placebirth.value' in results_df else np.nan
        placedeath = results_df['placedeath.value'][0] if 'placedeath.value' in results_df else np.nan
        image = results_df['image.value'][0] if 'image.value' in results_df else np.nan

        
        values = [STR_ESID, STN_LABEL_FINAL, wikiQ, wikiQLabel, givenname, familyname, sex, birth, death, placebirth, placedeath, image]
        #print(values)
        streetnamesDeWork.loc[x] = values
        #print(f"{subjectStr} | {wikiQLabel}: {wikiQ} -> {instance}")
        with open("esid.txt", "w") as fp:
            fp.write(f"{esid}")

    #print(x)
        streetnamesDeWork.to_csv(workfile, encoding='UTF-8-SIG', sep=';')
    #if i>10:
        #break
