from datetime import date, datetime
from flask import Blueprint, request, jsonify, abort
from ..extensions import db
from ..models import Expense

bp = Blueprint("expenses", __name__)

@bp.post("")
def add_expense():
    data = request.get_json(force=True, silent=True) or {}
    amount = data.get("amount")
    if amount is None:
        abort(400, description="amount is required")
    dt = data.get("date")
    category = data.get("category")
    note = data.get("note")
    d = date.today()
    if dt:
        d = datetime.strptime(dt, "%Y-%m-%d").date()
    e = Expense(amount=int(amount), date=d, category=category, note=note)
    db.session.add(e)
    db.session.commit()
    return jsonify(e.to_dict()), 201

@bp.get("")
def list_expenses():
    month = request.args.get("month")
    q = Expense.query
    if month:
        q = q.filter(Expense.date.like(f"{month}-%"))
    q = q.order_by(Expense.date.desc(), Expense.id.desc())
    return jsonify([e.to_dict() for e in q.all()])
