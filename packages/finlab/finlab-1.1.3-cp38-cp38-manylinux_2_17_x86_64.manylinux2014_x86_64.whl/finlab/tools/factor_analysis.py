import pandas as pd
from finlab import data
from finlab.tools.event_study import create_factor_data
from tqdm import tqdm
from finlab.dataframe import FinlabDataFrame


def ic(factor, adj_close, days=[10, 20, 60, 120]):

    if isinstance(factor, pd.DataFrame):
        factor = {'factor': factor}

    for fname, f in factor.items():
        factor[fname] = FinlabDataFrame(f).index_str_to_date()

    first_ele = next(iter(factor))
    findex = factor[first_ele].index
    fcol = factor[first_ele].columns

    ind = factor.copy()
    adj = adj_close.copy()

    inter_index = findex.intersection(adj.index)
    inter_col = fcol.intersection(adj.columns)

    adj = adj.loc[inter_index]
    adj = adj[inter_col]

    for fname, f in factor.items():
        ind[fname] = ind[fname].loc[inter_index]
        ind[fname] = ind[fname][inter_col]

    ics = {}

    total = len(days) * len(factor)
    with tqdm(total=total, desc="Processing") as pbar:
        for d in days:
            ret = adj.shift(-d-1) / adj.shift(-1) - 1

            for fname, f in ind.items():
                ic = f.apply(lambda s: s.corr(ret.loc[s.name]), axis=1)
                ics[f"{fname}_{d}"] = ic
                pbar.update(1)

    return pd.concat(ics, axis=1)
