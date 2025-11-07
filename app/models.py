from datetime import datetime, date
from .extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def _base_dict(self):
        return {
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class Member(BaseModel):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(50))
    telegram_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(100))  # <-- baru
    opening_balance = db.Column(db.Integer, nullable=False, default=0)  # <-- baru

    cash_contributions = db.relationship("CashContribution", backref="member", lazy=True)
    purchases = db.relationship("Purchase", backref="member", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "telegram_id": self.telegram_id,
            "username": self.username,
            "opening_balance": self.opening_balance,
            **self._base_dict(),
        }

class CashContribution(BaseModel):
    __tablename__ = "cash_contributions"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    year_month = db.Column(db.String(7), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "member_name": self.member.name if self.member else None,
            "year_month": self.year_month,
            "amount": self.amount,
            "note": self.note,
            **self._base_dict(),
        }

class Expense(BaseModel):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    category = db.Column(db.String(100))
    note = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "category": self.category,
            "note": self.note,
            **self._base_dict(),
        }

class Purchase(BaseModel):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    months_equivalent = db.Column(db.Integer, nullable=False, default=1)
    date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "member_name": self.member.name if self.member else None,
            "amount": self.amount,
            "months_equivalent": self.months_equivalent,
            "date": self.date.isoformat(),
            "description": self.description,
            **self._base_dict(),
        }
