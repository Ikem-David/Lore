# Lore

A full-stack e-commerce web application where users can browse in-stock products, manage a shopping cart, and complete a simulated checkout flow.

**Live demo:** [lore-ikem2.vercel.app](https://lore-ikem2.vercel.app)

## Features

- User authentication — sign up and log in
- Product browsing with real-time stock availability
- Cart management — add, update, and remove items
- Checkout flow with order confirmation (payment processing not yet integrated)
- Cloud-hosted product images for fast, reliable loading

## Tech Stack

**Frontend**
- React.js
- Deployed on Vercel

**Backend**
- FastAPI (Python)
- Deployed on Railway

**Database**
- MySQL (hosted on Aiven)

**Other**
- Cloudinary — image storage and delivery

## Architecture

```
Lore/
├── FrontEnd/   # React application
└── BackEnd/    # FastAPI service, MySQL integration
```

The frontend and backend are deployed independently and communicate over a REST API.

## Getting Started

### Prerequisites
- Node.js and npm
- Python 3.10+
- A MySQL database instance
- A Cloudinary account (for image uploads)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Ikem-David/Lore.git
   cd Lore
   ```

2. Set up the backend
   ```bash
   cd BackEnd
   pip install -r requirements.txt
   # configure your .env with database and Cloudinary credentials
   uvicorn main:app --reload
   ```

3. Set up the frontend
   ```bash
   cd ../FrontEnd
   npm install
   npm start
   ```

## Roadmap

- [ ] Integrate a real payment gateway (e.g. Stripe/Paystack)
- [ ] Add order history for logged-in users
- [ ] Admin dashboard for inventory management

## Author

**David Ikem**
[GitHub](https://github.com/Ikem-David)
