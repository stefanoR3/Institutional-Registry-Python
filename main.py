import registry_module as reg_mod
import pandas_module as pd_mod
import datetime

records = reg_mod.fetch_registry_records()#datetime.date(2026,9,11))
df = pd_mod.get_registry_data(records)
df = pd_mod.format_registry_data(df)
reg_mod.registry_export(df) #why doesnt work?