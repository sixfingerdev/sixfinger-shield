"""Stripe payment integration"""
import stripe
from flask import current_app
from .models import User, Credit, Transaction
from .database import db

def init_stripe():
    """Initialize Stripe with API key"""
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

def create_checkout_session(user_id, package_name):
    """Create a Stripe checkout session for credit purchase"""
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    packages = current_app.config.get('CREDIT_PACKAGES', {})
    package = packages.get(package_name)
    
    if not package:
        raise ValueError("Invalid package")
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'{package_name.title()} Package',
                        'description': f'{package["credits"]} credits',
                    },
                    'unit_amount': package['price'] * 100,  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=current_app.config.get('STRIPE_SUCCESS_URL', 
                f'{current_app.config.get("BASE_URL", "http://localhost:5000")}/payment/success?session_id={{CHECKOUT_SESSION_ID}}'),
            cancel_url=current_app.config.get('STRIPE_CANCEL_URL',
                f'{current_app.config.get("BASE_URL", "http://localhost:5000")}/payment/cancel'),
            client_reference_id=str(user_id),
            metadata={
                'user_id': user_id,
                'package': package_name,
                'credits': package['credits']
            }
        )
        return session
    except Exception as e:
        current_app.logger.error(f"Stripe checkout error: {e}")
        raise

def handle_successful_payment(session):
    """Handle successful payment and credit user account"""
    try:
        user_id = int(session.metadata.get('user_id'))
        credits_amount = int(session.metadata.get('credits'))
        package = session.metadata.get('package')
        
        user = User.query.get(user_id)
        if not user:
            current_app.logger.error(f"User {user_id} not found for payment")
            return False
        
        # Get or create credit record
        credit = Credit.query.filter_by(user_id=user_id).first()
        if not credit:
            credit = Credit(user_id=user_id, balance=0, total_purchased=0, total_used=0)
            db.session.add(credit)
        
        # Add credits
        credit.balance += credits_amount
        credit.total_purchased += credits_amount
        
        # Create transaction record
        transaction = Transaction(
            user_id=user_id,
            amount=credits_amount,
            transaction_type='purchase',
            description=f'Purchased {package} package',
            stripe_payment_id=session.payment_intent
        )
        db.session.add(transaction)
        
        db.session.commit()
        
        current_app.logger.info(f"Added {credits_amount} credits to user {user_id}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error handling payment: {e}")
        db.session.rollback()
        return False

def verify_webhook_signature(payload, sig_header):
    """Verify Stripe webhook signature"""
    webhook_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')
    
    if not webhook_secret:
        current_app.logger.warning("No webhook secret configured")
        return None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        return event
    except ValueError as e:
        current_app.logger.error(f"Invalid payload: {e}")
        return None
    except stripe.error.SignatureVerificationError as e:
        current_app.logger.error(f"Invalid signature: {e}")
        return None
