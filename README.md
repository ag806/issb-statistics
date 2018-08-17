ISSB statistics on UK steel production, trade, and use.

## Data

Data from tables published by ISSB on the UK steel industry.

## License


## Preparation

The tables have been digitised by hand into the `issb-tables` subfolder. To
process these into neat CSV files (in the `data` folder), run these Python
scripts:

```python
python scripts/extract_uk_steel_production.py
python scripts/extract_uk_steel_exports.py
python scripts/extract_uk_market_supply.py
```
