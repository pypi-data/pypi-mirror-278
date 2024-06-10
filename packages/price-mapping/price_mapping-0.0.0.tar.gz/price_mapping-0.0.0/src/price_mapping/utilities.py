import polars as pl
from collections import defaultdict


class PriceTable:
    def __init__(
            self,
            df_route: pl.DataFrame,
            col_route_origin_state: str,
            col_route_destination_state: str,
            df_zone: pl.DataFrame,
            col_zone_state: str,
            col_zone_city: str,
            df_price: pl.DataFrame,
            col_price_route: str,
            col_price_zone: str,
            col_price_weight_group: str,
            col_price_basic_fee: str,
            col_price_increment: str,
            col_price_minus: str,
    ):
        # route
        self.df_route = df_route
        self.col_route_origin_state = col_route_origin_state
        self.col_route_destination_state = col_route_destination_state
        # zone
        self.df_zone = df_zone
        self.col_zone_state = col_zone_state
        self.col_zone_city = col_zone_city
        # price
        self.df_price = df_price
        self.col_price_route = col_price_route
        self.col_price_zone = col_price_zone
        self.col_price_weight_group = col_price_weight_group
        self.col_price_basic_fee = col_price_basic_fee
        self.col_price_increment = col_price_increment
        self.col_price_minus = col_price_minus

    def _preprocess(self, cols: list, name: str, df):
        df_pre_process = (
            df
            .with_columns(
                pl.concat_str([
                    pl.col(cols[0]).str.to_lowercase().str.strip_chars(),
                    pl.col(cols[1]).str.to_lowercase().str.strip_chars()
                ], separator='-').alias(name)
            )
            .drop(cols)
        )
        return df_pre_process

    def run(self):
        # route
        col_route = [self.col_route_origin_state, self.col_route_destination_state]
        self.df_route = self._preprocess(col_route, 'route_combine', self.df_route)

        # zone
        col_zone = [self.col_zone_state, self.col_zone_city]
        self.df_zone = self._preprocess(col_zone, 'zone_combine', self.df_zone)

        # price
        col_num = [
            self.col_price_route,
            self.col_price_zone,
            self.col_price_weight_group,
            self.col_price_basic_fee,
            self.col_price_increment,
            self.col_price_minus
        ]
        df_default = (
            self.df_price
            .select(col_num)
            .with_columns(
                pl.col(i).cast(pl.Float32, strict=False).fill_null(0)
                for i in col_num[2:]
            )
        )

        price = defaultdict(lambda: defaultdict(dict))
        for row in df_default.to_numpy():
            price[row[0]][row[1]].update({round(row[2], 2): row[3:].tolist()})

        return self.df_route, self.df_zone, price
