from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    is_claimed = db.Column(db.Boolean, default=False)

class CouponClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    browser_cookie = db.Column(db.String(100), nullable=False)
    claimed_at = db.Column(db.DateTime, default=datetime.utcnow)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.id'), nullable=False)

    @classmethod
    def is_eligible_for_claim(cls, ip_address, browser_cookie):
        # Check if the IP or cookie has claimed a coupon in the last hour
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_claim = cls.query.filter(
            (cls.ip_address == ip_address) | (cls.browser_cookie == browser_cookie),
            cls.claimed_at > one_hour_ago
        ).first()
        return recent_claim is None