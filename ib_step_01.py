from __future__ import division

__author__ = 'Jan Rock, YOTTALABS Ltd.'

import pandas as pd
import string
import sys
from collections import Counter

# PHASE A #################################################################################################

dataset = pd.read_csv("csv_paf.csv", header=1, sep=',')
dataset.columns = ['zip','town','street','number','house','flat','company','id']
total_orig = dataset['id'].count()

#drop duplicates in NAME
dataset = dataset.drop_duplicates(subset=['company','street','id'],take_last=True)

#drop null for address and company field
dataset = dataset[dataset.street.notnull()]
dataset = dataset[dataset.company.notnull()]
dataset = dataset.reset_index(drop=True)

#resort
dataset = dataset.sort(['company'], ascending=[1])
dataset = dataset.reset_index(drop=True)

#reseting to upper case + column selection
dataset = dataset[['company','street','number','town']]
company = dataset.company.str.upper()
street = dataset.street.str.upper()
town = dataset.town.str.upper()
number = dataset.number
result = pd.concat([company, street, number, town], axis=1)

#extract name and address composite pattern
result_cmp = pd.DataFrame()
result_cmp["name"] = result['company']
result_cmp["address"] = result['street'].map(str) + ' ' + result['number'] + ' ' + result['town']

#split - only for name
patt_nm_split = pd.DataFrame(result_cmp.name.str.split().tolist()).ix[0:]
df_nm_size = len(patt_nm_split.columns)

#insert clasification columns
vals = []
for x in range(0L, df_nm_size*2):
    if x % 2 == 1:
        vals.append(x)
patt_nm_split.columns = vals

for x in range (1L, df_nm_size*2):
    if x+2 <= df_nm_size*2:
        if x % 2 == 0 and x >= 1:
            patt_nm_split[x] = None
        patt_nm_split[df_nm_size*2] = None
patt_nm_split.sort_index(axis=1, inplace=True)

result_ds = pd.DataFrame()
result_ds = patt_nm_split
result_ds["address"] = result_cmp["address"]

print (result_ds)
sys.exit()

# PHASE 2 #################################################################################################

# create demo - register with companies to simulate exact match step
''' Old code
tds_pattern = pd.DataFrame()
tds_pattern = ['10 SQUARED','POCKLINGTON INDUSTRIAL ESTATE   YORK']
'''

# company register. Andrey
ts_data = pd.read_csv("csv_paf.csv", sep=',')
ts_data.columns = ['zip','address_1', 'address_2', 'address_3', 'address_4', 'address_5',
                        'address_6', 'address_7', 'address_8', 'address_9', 'name_1', 'Name', 'id',
                        'code_1', 'code_2', 'code_3']

ts_companies = ts_data[pd.notnull(ts_data['Name'])]
ts_companies = ts_companies.ix[0:, ['zip','address_1','address_4','name_1','Name','id']]
print ts_companies.head

# definite companies set (based on Ltd / plc) - classifiaction also added
company_set = ts_companies.ix[0:, ['Name']]
company_set = company_set[company_set['Name'].str.contains("Ltd| plc", na=False)]
company_set['classification'] = 2
print company_set.head

# individuals register. Sample individuals set, randomly generated - classifiaction also added
individuals_set = pd.read_csv('C:/Users/andrey.sobolev/Desktop/BIPB/Projects/Royal Mail/Data/name_data.csv', sep=',')

individuals_set['classification'] = -2
print ts_individuals.head

#concatenating commercial and individual sets
frames = company_set, individuals_set
t_set = pd.concat(frames)
t_set = t_set.reset_index(drop=True)
print t_set.head

#exact match. Populates 'classification' where match (currently only '2' as no idividuals' names in dataset
matched = ts_data.merge(t_set, how='left', on='Name')
print matched.head
