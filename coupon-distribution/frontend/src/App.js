import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [couponStatus, setCouponStatus] = useState({
    can_claim: true,
    remaining_time: 0,
    total_coupons: 0,
    claimed_coupons: 0
  });
  const [couponMessage, setCouponMessage] = useState('');
  const [couponCode, setCouponCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [animationClass, setAnimationClass] = useState('');

  // Memoized function to check coupon status
  const checkCouponStatus = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`${API_BASE_URL}/coupon-status`);
      setCouponStatus(response.data);
    } catch (error) {
      console.error('Error checking coupon status:', error);
      setCouponMessage('Unable to check coupon status. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Trigger initial status check and set up periodic checks
  useEffect(() => {
    checkCouponStatus();
    const statusInterval = setInterval(checkCouponStatus, 30000); // Check every 30 seconds
    return () => clearInterval(statusInterval);
  }, [checkCouponStatus]);

  // Claim coupon with enhanced error handling
  const claimCoupon = async () => {
    try {
      setIsLoading(true);
      setAnimationClass('animate-fade-in');
      
      const response = await axios.post(`${API_BASE_URL}/claim-coupon`);
      
      if (response.data.success) {
        setCouponCode(response.data.coupon_code);
        setCouponMessage(response.data.message);
        
        // Trigger confetti-like animation
        triggerConfetti();
      } else {
        setCouponMessage(response.data.message);
        setAnimationClass('');
      }
      
      // Refresh status after claiming
      await checkCouponStatus();
    } catch (error) {
      console.error('Error claiming coupon:', error);
      setCouponMessage(
        error.response?.data?.message || 
        'An unexpected error occurred. Please try again.'
      );
      setAnimationClass('');
    } finally {
      setIsLoading(false);
    }
  };

  // Simulated confetti animation
  const triggerConfetti = () => {
    const confettiContainer = document.createElement('div');
    confettiContainer.style.position = 'fixed';
    confettiContainer.style.top = '0';
    confettiContainer.style.left = '0';
    confettiContainer.style.width = '100%';
    confettiContainer.style.height = '100%';
    confettiContainer.style.pointerEvents = 'none';
    confettiContainer.style.zIndex = '9999';

    for (let i = 0; i < 50; i++) {
      const confetti = document.createElement('div');
      confetti.style.position = 'absolute';
      confetti.style.width = '10px';
      confetti.style.height = '10px';
      confetti.style.borderRadius = '50%';
      confetti.style.backgroundColor = getRandomColor();
      confetti.style.left = `${Math.random() * 100}%`;
      confetti.style.top = '-10px';
      confetti.style.animation = `fall ${Math.random() * 3 + 2}s linear ${Math.random()}s infinite`;
      
      confettiContainer.appendChild(confetti);
    }

    document.body.appendChild(confettiContainer);
    
    setTimeout(() => {
      document.body.removeChild(confettiContainer);
    }, 5000);
  };

  // Helper to get random color for confetti
  const getRandomColor = () => {
    const colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6'];
    return colors[Math.floor(Math.random() * colors.length)];
  };

  // Format remaining time
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}m ${remainingSeconds}s`;
  };

  return (
    <div className="App">
      <div className={`coupon-container ${animationClass}`}>
        <h1>Coupon Distribution</h1>
        
        {couponCode && (
          <div className="coupon-success">
            <h2>🎉 Congratulations!</h2>
            <p>Your Coupon Code: <strong>{couponCode}</strong></p>
          </div>
        )}

        {couponMessage && (
          <div className={`message ${couponCode ? 'success' : 'error'}`}>
            {couponMessage}
          </div>
        )}

        {!couponStatus.can_claim && (
          <div className="cooldown-message">
            Please wait {formatTime(couponStatus.remaining_time)} before claiming another coupon.
          </div>
        )}

        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          marginBottom: '20px',
          color: '#7f8c8d'
        }}>
          <span>Total Coupons: {couponStatus.total_coupons}</span>
          <span>Claimed: {couponStatus.claimed_coupons}</span>
        </div>

        <button 
          onClick={claimCoupon} 
          disabled={!couponStatus.can_claim || isLoading}
        >
          {isLoading ? 'Processing...' : 
           (couponStatus.can_claim ? 'Claim Coupon' : 'Cooldown Active')}
        </button>
      </div>
    </div>
  );
}

export default App; 