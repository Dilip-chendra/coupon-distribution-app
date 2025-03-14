# Coupon Distribution Web Application

## 🌟 Enhanced Features

### Advanced Coupon Distribution
- Round-robin coupon allocation
- Real-time coupon availability tracking
- Comprehensive usage statistics

### User Experience
- Responsive and modern UI design
- Animated interactions
- Clear feedback mechanisms
- Loading states and error handling

### Security Enhancements
- Robust IP and cookie-based claim prevention
- One-hour cooldown between claims
- Secure cookie management

## 🚀 Technology Stack
- **Backend**: Python Flask
- **Frontend**: React.js with modern hooks
- **Database**: SQLite
- **Deployment**: Heroku/Render

## 🔒 Abuse Prevention Strategies
1. **IP Address Tracking**
   - Unique claim tracking per IP
   - Prevents multiple claims within an hour

2. **Browser Cookie Management**
   - Unique session tracking
   - Prevents browser-based exploitation

3. **Rate Limiting**
   - Configurable claim cooldown
   - Automatic claim blocking

## 🎨 UI/UX Highlights
- Animated confetti on successful coupon claim
- Responsive design
- Modern, clean interface
- Informative status messages
- Loading indicators
- Hover and interaction effects

## 📊 Coupon Statistics
- Total coupon count
- Claimed coupon tracking
- Real-time status updates

## 🛠 Local Development

### Prerequisites
- Python 3.8+
- Node.js 14+
- pip
- npm

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🌐 Deployment Options
- Heroku
- Render
- PythonAnywhere

## 🔮 Future Roadmap
- Admin dashboard
- More sophisticated bot detection
- Enhanced rate limiting
- Internationalization support

## 📜 License
MIT License 