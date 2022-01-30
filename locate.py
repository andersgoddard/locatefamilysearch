import requests
import pandas as pd
import numpy as np
import textdistance
from bs4 import BeautifulSoup

def get_results(address, postcode):
    dataframe = get_database_for(postcode)
    results = dataframe
    if len(dataframe) > 0:
        results = get_most_relevant_results(dataframe, address)
        results = results.drop('Similarity', axis=1)
    return results
    
def get_database_for(postcode):
    df_list = get_dataframe_list(postcode) 
    if len(df_list) > 0:
        return pd.concat(df_list)
    else:
        return pd.DataFrame()   

def get_dataframe_list(postcode):
    index = 0
    df_list = list()
    
    while True:
        print("Fetching page " + str(index+1) + "...")
        page = get_web_response(postcode, index+1)
        if page.status_code != 200:
            break
        else:
            index += 1
            df_list.append(get_dataframe(page.text))
            
    return df_list

def get_web_response(postcode, index):
    url ='https://www.locatefamily.com/Street-Lists/UK/' + postcode + '/index' + str(index) + '.html'
    response = requests.get(url)
    return response

def get_dataframe(text):
    data = get_database_rows(text)
    df = pd.DataFrame(data, columns=['Name', 'Address', 'Phone', 'Similarity'])
    return df
    
def get_database_rows(text):
    names = get_name_list(text)
    addresses = get_address_list(text)
    phone_numbers = get_phone_numbers(text)
    similarities = [0] * len(names)
    database_rows = zip(names, addresses, phone_numbers, similarities)
    return list(database_rows)

def get_name_list(text):
    html = parse_text(text)
    given_names = html.find_all("span", itemprop="givenName")
    family_names = html.find_all("span", itemprop="familyName")
    names = zip(given_names, family_names)
    full_names = list()
    for name in names:
        given_name = clean_string(name[0].string)
        family_name = clean_string(name[1].string)
        full_names.append(given_name + " " + family_name)
    return full_names

def parse_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup
        
def clean_string(string):
    cleaned_string = string.replace('\xa0', '')
    return cleaned_string

def get_address_list(text):
    html = parse_text(text)
    addresses = html.find_all("span", itemprop="streetAddress")
    cleaned_addresses = clean_addresses(addresses)
    return cleaned_addresses

def clean_addresses(addresses):
    cleaned_addresses = list()
    for address in addresses: 
        cleaned_addresses.append(clean_string(address.string))
    return cleaned_addresses

def get_phone_numbers(text):
    html = parse_text(text)
    phone_numbers = html.find_all("span", itemprop="telephone")
    cleaned_phone_numbers = clean_phone_numbers(phone_numbers)
    return cleaned_phone_numbers

def clean_phone_numbers(numbers):
    cleaned_phone_numbers = list()
    for number in numbers:
        if number.string == None:
            cleaned_phone_numbers.append('')
        else:              
            cleaned_phone_numbers.append(clean_string(number.string))
    return cleaned_phone_numbers

def get_most_relevant_results(dataframe, address):
    all_results = get_similar_addresses(dataframe, address)
    most_relevant_results = all_results[all_results['Similarity']==1.0]    

    if len(most_relevant_results) > 0:
        return most_relevant_results
    
    most_relevant_results = all_results[all_results['Similarity']>=0.85]
    
    if len(most_relevant_results) > 10:
        most_relevant_results = most_relevant_results.head(10)
    
    return most_relevant_results

def get_similar_addresses(dataframe, address):
    dataframe = dataframe.replace(np.nan, '', regex=True)
    dataframe['Similarity'] = dataframe.apply(lambda row: get_similarity(row[1], address), axis=1)
    dataframe = dataframe.sort_values(by=['Similarity'], ascending=False)
    return dataframe

def get_similarity(word1, word2):
    return textdistance.ratcliff_obershelp(word1, word2)