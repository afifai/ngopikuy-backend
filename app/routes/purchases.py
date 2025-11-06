from datetime import date, datetime
from flask import Blueprint, request, jsonify, abort
from ..extensions import db
from ..models import Purchase, Member

bp = Blueprint("purchases", __name__)

@bp.post("")
def add_purchase():
    data = request.get_json(force=True, silent=True) or {}
    member_id = data.get("member_id")
    amount = data.get("amount")
    months_equivalent = data.get("months_equivalent", 1)
    dt = data.get("date")
    description = data.get("description")
    if not all([member_id, amount]):
        abort(400, description="member_id and amount are required")
    member = Member.query.get(member_id)
    if not member:
        abort(404, description="member not found")
    d = date.today()
    if dt:
        d = datetime.strptime(dt, "%Y-%m-%d").date()
    p = Purchase(member_id=member_id, amount=int(amount), months_equivalent=int(months_equivalent), date=d, description=description)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@bp.get("")
def list_purchases():
    member_id = request.args.get("member_id", type=int)
    month = request.args.get("month")
    q = Purchase.query
    if member_id:
        q = q.filter(Purchase.member_id == member_id)
    if month:
        q = q.filter(Purchase.date.like(f"{month}-%"))
    q = q.order_by(Purchase.date.desc(), Purchase.id.desc())
    return jsonify([p.to_dict() for p in q.all()])
