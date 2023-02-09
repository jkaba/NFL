# CFB Reference Scraper
# Author: Jameel Kaba

import pandas as pd
import requests, bs4
from bs4 import BeautifulSoup
import re
import urllib

def findTables(url):
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    divs = soup.findAll('div', id = "content")
    divs = divs[0].findAll("div", id=re.compile("^all"))
    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id=") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)
    return(ids)

def pullTable(url, tableID, header = False):
    res = requests.get(url)

    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id = tableID)
    data_rows = tables[0].findAll('tr')
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    if header == True:
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll("tr")
        data_header = data_header[0].findAll("th")
        header = []
        for i in range(len(data.columns)):
            header.append(data_header[i].getText())
        data.columns = header
        data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    return(data)
 
def pullLinks(url, tableID, header = False):
    res = requests.get(url)

    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id = tableID)
    data_rows = tables[0].findAll('tr')
    game_data = [[td.get('href') for td in data_rows[i].findAll(['a'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    if header == True:
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll("tr")
        data_header = data_header[0].findAll("th")
        header = []
        for i in range(len(data.columns)):
            header.append(data_header[i].getText())
        data.columns = header
        data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    return(data)
 
def listVals(table, key):
    lists = []
    for index in range(len(table)):
        lists.append(table[key][index])
    return lists

# Pull individual player statistics
url_list = pd.read_csv('temp_url_list.csv')
url_list = listVals(url_list, 'cfb_reference')

stat_list = []
tables = ['defense','rushing','receiving','kick_ret','punt_ret']

for u in range(len(url_list)):
    player_list = []
    url = url_list[u]
    player_list.append(url)
    for t in range(len(tables)):
        lookup = tables[t]
        player_list.append(lookup)
        if lookup in ['receiving','rushing','kick_ret','punt_ret']:
            columns = [0,1,2,5,6,7,9,10,11,13]
            #year, school, conference, G, receiving/rushing/return statistics

        elif lookup == 'defense':
            columns = [0,1,2,5,6,7,9,10,11,14,15,19,16,18]
            #year, school, conference, G, tackles, TFL, sacks, INT/TD, Pass Def, FF/FR/TD

        try:
            table_data = pullTable(url, lookup)
        except:
            table_data = []
        for column in columns:
            try:
                player_list.append(table_data.iloc[len(table_data) - 2, column])
            except:
                player_list.append('')
    stat_list.append(player_list)

dumpfile = open('dumpfile.csv','w')
writeLine = 'cfb_url,defense,year,school,conf,g,tkl,ast_tkl,tfl,sk,int,int_td,pass_def,ff,fr,fr_td' +\
            ',rushing,year,school,conf,g,att,yds,td,rec,yds,td,receiving,year,school,conf,g,rec,yds,td,att,yds,td' +\
            ',kick_ret,year,school,conf,g,kret,kyds,ktd,pret,pyds,ptd,punt_ret,year,school,conf,g,pret,pyds,ptd,kret,kyds,ktd' + '\n'
dumpfile.write(writeLine)

for index in range(len(stat_list)):
    writeLine = ''
    for i in range(len(stat_list[index])):
        writeLine += (str(stat_list[index][i]) + ',')
    writeLine += '\n'
    dumpfile.write(writeLine)
dumpfile.close()    