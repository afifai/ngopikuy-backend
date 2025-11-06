import pandas as pd
from flask import Blueprint, request
from ..models import CashContribution, Expense, Purchase
from ..utils.csv_export import df_to_csv_response

bp = Blueprint("export", __name__)

@bp.get("/csv")
def export_csv():
    month = request.args.get("month")
    cash_q = CashContribution.query
    exp_q = Expense.query
    pur_q = Purchase.query
    if month:
        cash_q = cash_q.filter(CashContribution.year_month == month)
        exp_q = exp_q.filter(Expense.date.like(f"{month}-%"))
        pur_q = pur_q.filter(Purchase.date.like(f"{month}-%"))
    rows = []
    for c in cash_q.all():
        d = c.to_dict(); d["type"]="cash"; rows.append(d)
    for e in exp_q.all():
        d = e.to_dict(); d["type"]="expense"; rows.append(d)
    for p in pur_q.all():
        d = p.to_dict(); d["type"]="purchase"; rows.append(d)
    import pandas as pd
    df = pd.DataFrame(rows)
    if df.empty: df = pd.DataFrame(columns=["type"])
    fname = f"rekap_{month}.csv" if month else "rekap_all.csv"
    return df_to_csv_response(df, fname)
