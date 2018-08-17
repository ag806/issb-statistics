"""Extract data on steel supply to UK market from ISSB tables.

This doesn't currently do any transforming, just converts xls to csv.
Adds a `year` column for consistency with other tables.

It then aggregates the non-alloy, stainless, and other-alloy data for ease of
combination with the other tables. "Long products" are grouped with "Heavy
sections etc", "Flat products" are grouped with "Sheets".

"""

import pandas as pd

with pd.ExcelFile('issb-tables/2017_Table18.xls') as xls:
    about = pd.read_excel(xls, sheet_name='About', header=None, index_col=0)[1]
    table = pd.read_excel(xls, sheet_name='Table')

table['year'] = 2016

table.to_csv('data/supply_by_alloy.csv', index=False)

table2 = table.copy()
table2.loc[table2['product'] == 'Flat products', 'product'] = 'Sheets, coated and uncoated'
table2.loc[table2['product'] == 'Long products', 'product'] = 'Heavy sections, sheet piling, rails and rolled accessories'

table2 = table2.groupby(['product', 'year'], as_index=False).agg({
    'product_category': 'first',
    'uk_production_to_industry': 'sum',
    'uk_production_to_stockholders': 'sum',
    'imports': 'sum',
})

table2.to_csv('data/supply.csv', index=False)
