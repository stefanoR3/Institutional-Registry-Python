import registry_logic as registry
import datetime

records = registry.fetch_registry_records(datetime.date(2026,9,15), datetime.date(2026,9,25))
registry.format_registry_data(records)
