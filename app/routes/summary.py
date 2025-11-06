from collections import defaultdict
from flask import Blueprint, request, jsonify
from ..models import CashContribution, Expense, Purchase

bp = Blueprint("summary", __name__)

def monthly_summary(month: str):
    cash = CashContribution.query.filter(CashContribution.year_month == month).all()
    expenses = Expense.query.filter(Expense.date.like(f"{month}-%")).all()
    purchases = Purchase.query.filter(Purchase.date.like(f"{month}-%")).all()
    total_cash = sum(c.amount for c in cash)
    total_expenses = sum(e.amount for e in expenses)
    total_purchases = sum(p.amount for p in purchases)
    balance = total_cash + total_purchases - total_expenses
    by_member = defaultdict(int)
    for c in cash:
        key = c.member.name if c.member else f"member#{c.member_id}"
        by_member[key] += c.amount
    return {"month": month,"totals":{"cash_in":total_cash,"in_kind_purchases":total_purchases,"expenses":total_expenses,"balance":balance},"details":{"cash":[c.to_dict() for c in cash],"expenses":[e.to_dict() for e in expenses],"purchases":[p.to_dict() for p in purchases]},"by_member_cash":by_member}

@bp.get("/monthly")
def get_monthly():
    month = request.args.get("month")
    if not month:
        return {"error":"month=YYYY-MM required"},400
    return jsonify(monthly_summary(month))

@bp.get("/overall")
def overall():
    months = set([c.year_month for c in CashContribution.query.all()])
    months.update([e.date.strftime("%Y-%m") for e in Expense.query.all()])
    months.update([p.date.strftime("%Y-%m") for p in Purchase.query.all()])
    out = [monthly_summary(m) for m in sorted(months)]
    return jsonify(out)
