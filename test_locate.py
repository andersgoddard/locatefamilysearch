import pytest
import pandas as pd
from locate import *

# The first two tests scrape 73 web pages, so they take circa 10-15 seconds to run
# I have saved a local CSV file with the data for further testing

# def test_web_scrape():
    # pages = get_number_of_pages('W2')
    # assert pages == 73
    
# def test_get_full_database():
    # df = get_database_for('W2')
    
    # assert len(df) == 5761
    # assert df.iloc[5760]['Name'] == 'John De-Grave'
    # assert df.iloc[5760]['Address'] == 'PO Box LB45'
    # assert df.iloc[5760]['Phone'] == '020 73513939'
    # assert df.iloc[5760]['Similarity'] == 0

# The below test scrapes 22 web pages, so it is also commented out. 
# However, this tests the full backend functionality, so should be periodically run

# def test_full_backend():
    # address = '210 Lincoln Avenue'
    # postcode = 'TW2'
    
    # results = get_results(address, postcode)
    
    # assert len(results) == 8
    # assert results.iloc[0]['Address'] == '104 Lincoln Avenue'

        
@pytest.fixture
def data():
    data = get_web_response('W2', 1)
    return data.text

@pytest.fixture
def data_cache():
    data_cache = pd.read_csv('out.csv')
    return data_cache

def test_get_number_of_addresses(data):
    address_num = get_number_of_addresses(data)
    assert address_num == 80
    
def test_get_list_of_addresses(data):
    address_list = get_address_list(data)
    assert len(address_list) == 80
    
def test_address(data):
    address_list = get_address_list(data)
    assert address_list[2] == '35 Byres Rd, G12'
    
def test_get_list_of_names(data):
    name_list = get_name_list(data)
    assert len(name_list) == 80
    
def test_name(data):
    name_list = get_name_list(data)
    assert name_list[0] == 'Michael Schroeter'
    
def test_get_list_of_numbers(data):
    phone_list = get_phone_numbers(data)
    assert len(phone_list) == 80
    
def test_get_phone_number(data):
    phone_list = get_phone_numbers(data)
    assert phone_list[2] == '01413 342361'
    assert phone_list[0] == ''
    
def test_get_tuple(data):
    database_rows = get_database_rows(data)
    assert len(database_rows) == 80
    
    third_row = database_rows[2]
    assert third_row[0] == 'Karnail Singh'
    assert third_row[1] == '35 Byres Rd, G12'
    assert third_row[2] == '01413 342361'
    assert third_row[3] == 0
    
def test_get_dataframe(data):
    dataframe = get_dataframe(data)
    assert len(dataframe) == 80
    assert dataframe.iloc[2]['Name'] == 'Karnail Singh'
    assert dataframe.iloc[2]['Address'] == '35 Byres Rd, G12'
    assert dataframe.iloc[2]['Phone'] == '01413 342361'
    assert dataframe.iloc[2]['Similarity'] == 0

def test_address_similarities():
    address1 = '35 Byres Rd G12'
    address2 = '35 Byres Rd G12'
    address3 = '37 Byres Rd G12'
    address4 = '35 Byres Road G12'
    address5 = '35 Byres Road'
    
    assert get_similarity(address1, address2) == 1
    assert get_similarity(address1, address3) - 0.93 < 0.01
    assert get_similarity(address1, address4) - 0.94 < 0.01
    assert get_similarity(address1, address5) - 0.78 < 0.01
    
def test_get_relevant_results(data_cache):
    address = '34 Palace Court'
    results = get_similar_addresses(data_cache, address)
    
    assert results.iloc[0]['Address'] == address
    
def test_refine_results(data_cache):
    address = '34 Palace Court'
    results = get_most_relevant_results(data_cache, address)
    
    assert len(results) == 15
    
    address = '25 Clanricarde Gardens'
    results = get_most_relevant_results(data_cache, address)
    
    assert len(results) == 4
    
    address = '7 Palace Court'
    results = get_most_relevant_results(data_cache, address)
    
    assert len(results) == 10
    