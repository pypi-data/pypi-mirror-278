from pathlib import Path
import duckdb
from src.price_mapping.utilities import PriceTable
from src.price_mapping.main import ESFLogic
from core_pro import Sheet


# data
path = Path('/Users/kevinkhang/Downloads/fe_esf/2024-05-01/raw')
file = sorted(path.glob('*available*.parquet'))

# table price
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

# data
query = f"""
with t as (
    select * 
    , lower(buyer_address_state) || '-' || lower(seller_pickup_address) route_combine
    , lower(buyer_address_state) || '-' || lower(buyer_address_city) zone_combine
    from read_parquet('{path / f'*available*.parquet'}')
)
select t.*
,r.Route route_
,z.Zone zone_
from t
left join df_route r on t.route_combine = r.route_combine
left join df_zone z on t.zone_combine = z.zone_combine
where seller_type = 'Default'
"""
df = duckdb.sql(query).pl()
esf = ESFLogic(
    price_dict=price,
    data=df,
    col_route='route_',
    col_zone='zone_',
    col_weight='final_weight'
)
df = esf.run()
