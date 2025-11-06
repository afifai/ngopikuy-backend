from datetime import datetime
from dateutil.relativedelta import relativedelta

def validate_year_month(s: str) -> str:
    dt = datetime.strptime(s, "%Y-%m")
    return dt.strftime("%Y-%m")

def add_months(year_month: str, n: int) -> str:
    dt = datetime.strptime(year_month, "%Y-%m")
    dt = dt + relativedelta(months=n)
    return dt.strftime("%Y-%m")
