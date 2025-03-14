from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Coupon, CouponClaim
import os
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# More robust CORS configuration
cors_config = {
    'origins': [
        'http://localhost:3000',  # Local development
        'https://coupon-distribution.netlify.app',  # Example production URL
        os.environ.get('FRONTEND_URL', '')  # Allow custom frontend URL
    ],
    'supports_credentials': True
}
CORS(app, resources={
    r"/*": cors_config
})

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///coupons.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    
    # Seed initial coupons if not exists
    if Coupon.query.count() == 0:
        initial_coupons = [
            Coupon(code=f'COUP-{i:03d}', is_claimed=False) 
            for i in range(1, 51)  # Increased to 50 unique coupons
        ]
        db.session.bulk_save_objects(initial_coupons)
        db.session.commit()

@app.route('/claim-coupon', methods=['POST'])
def claim_coupon():
    # Get client IP and generate/use browser cookie
    ip_address = request.remote_addr
    browser_cookie = request.cookies.get('coupon_tracker') or str(uuid.uuid4())
    
    with app.app_context():
        # Check eligibility based on IP and cookie
        if not CouponClaim.is_eligible_for_claim(ip_address, browser_cookie):
            return jsonify({
                'success': False, 
                'message': 'You can only claim one coupon per hour.'
            }), 429
        
        # Find an unclaimed coupon
        unclaimed_coupon = Coupon.query.filter_by(is_claimed=False).first()
        
        if not unclaimed_coupon:
            return jsonify({
                'success': False, 
                'message': 'No coupons available at the moment.'
            }), 404
        
        # Mark coupon as claimed
        unclaimed_coupon.is_claimed = True
        
        # Record the claim
        claim = CouponClaim(
            ip_address=ip_address, 
            browser_cookie=browser_cookie, 
            coupon_id=unclaimed_coupon.id
        )
        
        db.session.add(claim)
        db.session.commit()
        
        response = jsonify({
            'success': True, 
            'coupon_code': unclaimed_coupon.code,
            'message': 'Coupon claimed successfully!'
        })
        
        # Set browser cookie for tracking
        response.set_cookie('coupon_tracker', browser_cookie, max_age=3600)
        
        return response

@app.route('/coupon-status', methods=['GET'])
def coupon_status():
    ip_address = request.remote_addr
    browser_cookie = request.cookies.get('coupon_tracker')
    
    with app.app_context():
        # Total coupon statistics
        total_coupons = Coupon.query.count()
        claimed_coupons = Coupon.query.filter_by(is_claimed=True).count()
        
        if browser_cookie:
            last_claim = CouponClaim.query.filter_by(
                browser_cookie=browser_cookie
            ).order_by(CouponClaim.claimed_at.desc()).first()
            
            if last_claim:
                time_since_claim = datetime.utcnow() - last_claim.claimed_at
                remaining_time = max(0, 3600 - time_since_claim.total_seconds())
                
                return jsonify({
                    'can_claim': remaining_time == 0,
                    'remaining_time': remaining_time,
                    'total_coupons': total_coupons,
                    'claimed_coupons': claimed_coupons
                })
        
        return jsonify({
            'can_claim': True,
            'remaining_time': 0,
            'total_coupons': total_coupons,
            'claimed_coupons': claimed_coupons
        })

# Advanced rate limiting and logging middleware
@app.before_request
def log_request_info():
    # Optional: Implement more advanced logging
    app.logger.info(f'Request from {request.remote_addr} to {request.path}')

if __name__ == '__main__':
    app.run(debug=True) 