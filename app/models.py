from datetime import datetime
from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coupons = db.relationship("Coupon", backref="user", lazy=True)
    transactions = db.relationship("Transaction", backref="user", lazy=True)

class Region(db.Model):
    __tablename__ = "regions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    fighters = db.relationship("Fighter", backref="region", lazy=True)
    matches_x = db.relationship("Match", foreign_keys="Match.region_x_id", backref="region_x", lazy=True)
    matches_y = db.relationship("Match", foreign_keys="Match.region_y_id", backref="region_y", lazy=True)

class Fighter(db.Model):
    __tablename__ = "fighters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    matches_x = db.relationship("Match", foreign_keys="Match.fighter_x_id", backref="fighter_x", lazy=True)
    matches_y = db.relationship("Match", foreign_keys="Match.fighter_y_id", backref="fighter_y", lazy=True)

class Match(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True)
    match_type = db.Column(db.Enum("fighter", "region"), nullable=False)
    fighter_x_id = db.Column(db.Integer, db.ForeignKey("fighters.id"))
    fighter_y_id = db.Column(db.Integer, db.ForeignKey("fighters.id"))
    region_x_id = db.Column(db.Integer, db.ForeignKey("regions.id"))
    region_y_id = db.Column(db.Integer, db.ForeignKey("regions.id"))
    match_date = db.Column(db.Date, nullable=False)
    match_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum("pending", "finished"), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship("Event", backref="match", lazy=True)

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"), nullable=False)
    event_type = db.Column(db.Enum("victory_x", "victory_y", "draw", "double_chance_x"), nullable=False)
    odd = db.Column(db.Numeric(5,2), nullable=False)
    is_winner = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coupon_items = db.relationship("CouponItem", backref="event", lazy=True)

class SpecialEvent(db.Model):
    __tablename__ = "special_events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    odd = db.Column(db.Numeric(5,2), nullable=False)
    is_winner = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coupon_items = db.relationship("CouponItem", backref="special_event", lazy=True)

class Coupon(db.Model):
    __tablename__ = "coupons"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stake = db.Column(db.Numeric(10,2), nullable=False)
    total_odd = db.Column(db.Numeric(10,2), nullable=False)
    possible_gain = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.Enum("pending","won","lost"), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("CouponItem", backref="coupon", lazy=True)

class CouponItem(db.Model):
    __tablename__ = "coupon_items"
    id = db.Column(db.Integer, primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey("coupons.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    special_event_id = db.Column(db.Integer, db.ForeignKey("special_events.id"))
    odd = db.Column(db.Numeric(5,2), nullable=False)

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.Enum("deposit", "withdraw", "bet", "win"), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.Enum("pending","approved","rejected"), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
