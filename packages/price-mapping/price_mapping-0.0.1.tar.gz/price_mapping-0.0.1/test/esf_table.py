from src.price_mapping.utilities import PriceTable
from core_pro import Sheet
import polars as pl


sh = '1kAE5QZD7vDCxODwRAD0ocdusiqPvXHNpUjJmvyMzZes'
df_route = Sheet(sh).google_sheet_into_df('route', 'A:C')
df_zone = Sheet(sh).google_sheet_into_df('zone', 'A:C')
df_price = Sheet(sh).google_sheet_into_df('default', 'A:G')

table = PriceTable(
    df_route=df_route,
    col_route_origin_state='Origin_State',
    col_route_destination_state='Destination_State',
    df_zone=df_zone,
    col_zone_city='City',
    col_zone_state='State',
    df_price=df_price,
    col_price_zone='Zone(O)',
    col_price_route='Route(O)',
    col_price_weight_group='Weight',
    col_price_basic_fee='*Original Fee(R)',
    col_price_increment='Increment amount(O)',
    col_price_minus='Minus'
)
df_route, df_zone, price = table.run()
