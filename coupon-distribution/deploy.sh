#!/bin/bash

# Backend deployment
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Frontend build
cd ../frontend
npm install
npm run build

# Return to project root
cd ..

echo "Deployment preparation complete. 
Next steps:
1. Set up your production database
2. Configure environment variables
3. Use gunicorn to serve the Flask backend
4. Serve frontend build files via static hosting" 