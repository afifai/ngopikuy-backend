from flask import Blueprint, request, jsonify, abort
from ..extensions import db
from ..models import Member

bp = Blueprint("members", __name__, url_prefix="/members")

@bp.post("")
def create_member():
    data = request.get_json(force=True, silent=True) or {}
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip() or None
    telegram_id = (data.get("telegram_id") or "").strip() or None
    if not name:
        abort(400, description="name is required")
    if telegram_id and Member.query.filter_by(telegram_id=telegram_id).first():
        abort(409, description="telegram_id already exists")
    m = Member(name=name, phone=phone, telegram_id=telegram_id)
    db.session.add(m)
    db.session.commit()
    return jsonify(m.to_dict()), 201

@bp.get("")
def list_members():
    rows = Member.query.order_by(Member.name.asc()).all()
    return jsonify([m.to_dict() for m in rows])

@bp.get("/<int:member_id>")
def get_member(member_id):
    m = Member.query.get_or_404(member_id)
    return jsonify(m.to_dict())

@bp.put("/<int:member_id>")
def update_member(member_id):
    m = Member.query.get_or_404(member_id)
    data = request.get_json(force=True, silent=True) or {}
    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            abort(400, description="name cannot be empty")
        m.name = name
    if "phone" in data:
        m.phone = (data.get("phone") or "").strip() or None
    if "telegram_id" in data:
        new_tid = (data.get("telegram_id") or "").strip() or None
        if new_tid and Member.query.filter(Member.telegram_id == new_tid, Member.id != member_id).first():
            abort(409, description="telegram_id already in use")
        m.telegram_id = new_tid
    db.session.commit()
    return jsonify(m.to_dict())

@bp.delete("/<int:member_id>")
def delete_member(member_id):
    m = Member.query.get_or_404(member_id)
    db.session.delete(m)
    db.session.commit()
    return "", 204
