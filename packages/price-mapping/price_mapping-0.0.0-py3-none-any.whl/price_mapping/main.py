import duckdb
import polars as pl
from collections import defaultdict
import numpy as np
from tqdm import tqdm


class ESFLogic:
    def __init__(
            self,
            data,
            price_dict: defaultdict,
            col_route: str = 'route_',
            col_zone: str = 'zone_',
            col_weight: str = 'weight_',
            debug: bool = False
    ):
        self.data = data
        self.price_dict = price_dict
        self.col_route = col_route
        self.col_zone = col_zone
        self.col_weight = col_weight
        self.debug = debug

    def fee(self, array: list):
        # init
        route, urban, s_weight = array
        # lookups
        search_urban = self.price_dict.get(route, {}).get(urban)
        if not search_urban:
            return [0, 0, 0]
        # pre-calculate sorted keys for weight lookup
        sorted_keys = sorted((float(_) for _ in search_urban.keys()))
        # binary search
        weight = min(np.searchsorted(sorted_keys, s_weight), len(sorted_keys) - 1)
        weight = sorted_keys[weight]
        return search_urban[weight]

    def run(self):
        # mapping
        col = [self.col_route, self.col_zone, self.col_weight]
        fee_group_lst = [self.fee(i) for i in tqdm(self.data[col].to_numpy(), desc='Route-Zone-Weight Mapping')]
        col_name = ['basic_fee', 'extra_fee', 'weight_group']
        dict_ = {v: [_[i] for _ in fee_group_lst] for i, v in enumerate(col_name)}

        # df fee
        df_fee = pl.DataFrame(dict_)
        data = pl.concat([self.data, df_fee], how='horizontal')
        del self.data, df_fee

        # post process
        query = f"""
        select *
        , basic_fee + extra_fee * ceil(({self.col_weight} - weight_group) / 0.5) fee
        from data
        """
        data = duckdb.sql(query).pl()
        if not self.debug:
            data = data.drop(col_name)
        return data
