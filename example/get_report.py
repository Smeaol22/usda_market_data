from datetime import datetime

from src.production_cost import ProductionCostStates, get_cost_production_historic

date_str_1 = '01-01-2020'
date_str_2 = '28-02-2020'
tms1 = datetime.timestamp(datetime.strptime(date_str_1, "%d-%m-%Y"))
tms2 = datetime.timestamp(datetime.strptime(date_str_2, "%d-%m-%Y"))
df_response = get_cost_production_historic(ProductionCostStates.illinois, start_date=tms1, end_date=tms2)
