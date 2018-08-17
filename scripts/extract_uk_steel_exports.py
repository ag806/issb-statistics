"""Extract data on UK steel exports from ISSB tables.

This currently ignores the alloy/non-alloy split and uses only the "total"
data.

"""

import pandas as pd

with pd.ExcelFile('issb-tables/2017_Table17.xls') as xls:
    about = pd.read_excel(xls, sheet_name='About', header=None, index_col=0)[1]
    total = pd.read_excel(xls, sheet_name='Total')

# Unpivot to make a long table and save
total_long = total.melt(id_vars=['product_category', 'product'], var_name='year', value_name='mass')
total_long.to_csv('data/exports.csv', index=False)
