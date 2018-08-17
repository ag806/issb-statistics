"""Extract data on UK steel production from ISSB tables.

This currently ignores the alloy/non-alloy split and uses on the "total" data.

ECSC products are one category that is reported; there is some double-counting
in the table of "other steel industry products" which are derived. 2007 was the
last year that details on how ECSC products are used to make derived products
were given (in Table 19). So we use that breakdown, scaled by total feedstock
use, to estimate how much of the ECSC production is used for feedstocks for
other products.

"""

import pandas as pd

with pd.ExcelFile('issb-tables/2017_Table16.xls') as xls:
    about = pd.read_excel(xls, sheet_name='About', header=None, index_col=0)[1]
    total = pd.read_excel(xls, sheet_name='Total')

with pd.ExcelFile('issb-tables/2007_Table19.xls') as xls:
    feedstocks2007 = pd.read_excel(xls, sheet_name='Feedstocks for derived products', index_col=0)['mass']

# Split the table into 3 parts: ECSC production, feedstock use, derived
# products

total['product'] = total['product'].str.lstrip('Derived products: ')

SPLIT_CELL = "Material from above used to manufacture 'derived products' below"
isplit = total['product'].tolist().index(SPLIT_CELL)
assert isplit >= 0, 'could not find split cell'
total_ecsc = total.iloc[:isplit]
total_derived = total.iloc[isplit + 1:]
total_derived_in = -total.iloc[isplit, 1:]
total_derived_in.name = 'mass'

# Allocate the feedstock use "derived_in" according to 2007 ratios.
ratios = feedstocks2007 / feedstocks2007.sum()
total_ecsc_for_derived = \
    ratios.to_frame() \
          .dot(total_derived_in.to_frame().T) \
          .reset_index()

# Unpivot to make a long table and save
total_ecsc_long = total_ecsc.melt(id_vars=['product'], var_name='year', value_name='mass')
total_derived_long = total_derived.melt(id_vars=['product'], var_name='year', value_name='mass')
total_ecsc_for_derived_long = total_ecsc_for_derived.melt(
    id_vars=['product'], var_name='year', value_name='mass')
# total_ecsc_for_derived = -total_derived_in.to_frame()

total_ecsc_long.to_csv('data/production_ecsc.csv', index=False)
total_derived_long.to_csv('data/production_derived.csv', index=False)
total_ecsc_for_derived_long.to_csv('data/production_ecsc_for_derived.csv', index=False)
