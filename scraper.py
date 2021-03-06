# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:16:33 2020

@author: Harbing Lou
"""

"""Fetches & stores the current S&P 500 symbols."""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


def get_url_text(symbol):
    
    URL = 'https://money.cnn.com/quote/shareholders/shareholders.html?symb='+symbol +'&subView=institutional'

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup)
    table = soup.find_all('table')[4]
    rows = table.find_all('tr')
    return rows

#%% list of holder names
def extract_shareholder(rows):
    
    snp_list = []
    
    for row in rows[1:]: 
        holder_list= []
        element = row.find_all('td')
    
        holder_list.append( element[0].getText())
        holder_list.append( element[1].getText())
        holder_list.append( element[2].getText())
        holder_list.append( element[3].getText())
        holder_list.append( element[4].getText())
        holder_list.append( element[5].getText())
        
        snp_list.append(holder_list)
        #print(holder_list)
        
    return snp_list

#convert to dataframe first 
    #a_series = pd.Series(holder_list, index = holder_frame.columns)

    #holder_dict_frame = pd.DataFrame.from_dict(holder_dict)
    #holder_frame[len(holder_frame)]  = holder_list
    #holder_frame.append(a_series, ignore_index=True)
    
    #holder_frame.append(holder_list, ignore_index=True)
    #print(element)
    #snp_list.append(holder_dict)
#%% main app
holder_frame = pd.DataFrame(columns = [ "Stakeholder", "Stake","Shares owned","Total value ($)", "Shares bought / sold", "Total change","Symbol"])

snp_list  = pd.read_csv('SP 500.csv')
for i in snp_list['Symbol']: #loop through all companies names in SNP 500
    print(i)
    try:
        raw_text = get_url_text(i)
    except:
        continue
    snp_result = extract_shareholder(raw_text)
    holder_frame_single = pd.DataFrame(snp_result, columns = ["Stakeholder", "Stake","Shares owned","Total value ($)", "Shares bought / sold", "Total change"])  
    #holder_frame.loc[len(holder_frame)] = snp_list
    holder_frame_single['Symbol'] = i
    holder_frame = holder_frame.append(holder_frame_single, ignore_index=True)
    
    
    # it takes quite a while to run through 500 companies.


#%%
holder_frame.to_csv("shareholder.csv",index=False)

#%%
"""
    holder_dict["Stakeholder"] = element[0].getText()
    holder_dict["Stake"] = element[1].getText()
    holder_dict["Shares owned"] = element[2].getText()
    holder_dict["Total value ($)"] = element[3].getText()
    holder_dict["Shares bought / sold"] = element[4].getText()
    holder_dict["Total change"] = element[5].getText()
"""