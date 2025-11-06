from flask import Blueprint, request, jsonify, abort
from ..extensions import db
from ..models import CashContribution, Member
from ..utils.dates import validate_year_month, add_months

bp = Blueprint("cash", __name__)

@bp.post("")
def add_cash():
    data = request.get_json(force=True, silent=True) or {}
    member_id = data.get("member_id")
    amount = data.get("amount")
    start_month = data.get("start_month")
    months = int(data.get("months") or 1)
    note = data.get("note")
    if not all([member_id, amount, start_month]):
        abort(400, description="member_id, amount, start_month are required")
    member = Member.query.get(member_id)
    if not member:
        abort(404, description="member not found")
    ym = validate_year_month(str(start_month))
    created = []
    for i in range(months):
        this_month = add_months(ym, i)
        cc = CashContribution(member_id=member_id, amount=int(amount), year_month=this_month, note=note)
        db.session.add(cc)
        created.append(cc)
    db.session.commit()
    return jsonify([c.to_dict() for c in created]), 201

@bp.get("")
def list_cash():
    member_id = request.args.get("member_id", type=int)
    month = request.args.get("month")
    q = CashContribution.query
    if member_id:
        q = q.filter(CashContribution.member_id == member_id)
    if month:
        q = q.filter(CashContribution.year_month == month)
    q = q.order_by(CashContribution.year_month.desc(), CashContribution.id.desc())
    return jsonify([c.to_dict() for c in q.all()])
