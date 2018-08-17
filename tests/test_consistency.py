import datapackage
import pandas as pd
import os.path

DATAPACKAGE = os.path.join(os.path.dirname(__file__), '../datapackage.json')


def test_uk_steel_delivered_to_uk_is_consistent():
    """Two tables provide this: (A) the difference between UK production and
    exports in Tables 16 and 17; and (B) Table 18 "supply to UK market".
    This test checks they match.

    """

    # Load data
    p = datapackage.Package(DATAPACKAGE)
    dfs = {r.name: pd.DataFrame(r.read(keyed=True)) for r in p.resources}

    # Version A: production - exports
    prod1 = dfs['production_ecsc'].set_index(['year', 'product'])['mass']
    prod2 = dfs['production_derived'].set_index(['year', 'product'])['mass']
    exports = dfs['exports'].set_index(['year', 'product'])['mass']
    prod = pd.concat([prod1, prod2])
    A = (prod - exports).loc[2016]

    # Version B: supply
    supply = dfs['supply'].groupby(['product']).sum()
    B = supply[['uk_production_to_stockholders', 'uk_production_to_industry']] \
        .sum(axis='columns')

    # Compare
    df = pd.concat({'A': A, 'B': B}, axis=1)
    df['diff'] = df['A'].astype(float) - df['B']

    problems = (abs(df['diff']) > 0.5) | (pd.isnull(df['diff']))
    assert not any(problems), \
        'Differences found:\n\n%s\n' % df[problems]
