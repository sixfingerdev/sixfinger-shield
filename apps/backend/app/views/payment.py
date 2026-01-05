"""Payment and credit management views"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from ..models import Credit, Transaction
from ..database import db
from ..forms import CreditPurchaseForm
from ..payments import create_checkout_session, handle_successful_payment, verify_webhook_signature
import stripe

payment_bp = Blueprint('payment_blueprint', __name__)

@payment_bp.route('/credits', methods=['GET'])
@login_required
def credits():
    """View credit balance and purchase options"""
    credit = Credit.query.filter_by(user_id=current_user.id).first()
    
    if not credit:
        # Create credit record if it doesn't exist
        credit = Credit(user_id=current_user.id, balance=0, total_purchased=0, total_used=0)
        db.session.add(credit)
        db.session.commit()
    
    form = CreditPurchaseForm()
    packages = current_app.config.get('CREDIT_PACKAGES', {})
    
    return render_template('payment/credits.html', credit=credit, form=form, packages=packages)

@payment_bp.route('/purchase', methods=['POST'])
@login_required
def purchase():
    """Create Stripe checkout session for credit purchase"""
    form = CreditPurchaseForm()
    
    if form.validate_on_submit():
        package = form.package.data
        
        try:
            # Create Stripe checkout session
            session = create_checkout_session(current_user.id, package)
            
            # Redirect to Stripe checkout
            return redirect(session.url, code=303)
            
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('payment_blueprint.credits'))
        except Exception as e:
            current_app.logger.error(f"Payment error: {e}")
            flash('Payment processing error. Please try again.', 'error')
            return redirect(url_for('payment_blueprint.credits'))
    
    flash('Invalid form submission.', 'error')
    return redirect(url_for('payment_blueprint.credits'))

@payment_bp.route('/success', methods=['GET'])
@login_required
def success():
    """Payment success page"""
    session_id = request.args.get('session_id')
    
    if session_id:
        flash('Payment successful! Your credits have been added.', 'success')
    
    return redirect(url_for('dashboard_blueprint.index'))

@payment_bp.route('/cancel', methods=['GET'])
@login_required
def cancel():
    """Payment cancelled page"""
    flash('Payment cancelled.', 'info')
    return redirect(url_for('payment_blueprint.credits'))

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    """Stripe webhook handler"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    # Verify webhook signature
    event = verify_webhook_signature(payload, sig_header)
    
    if not event:
        return jsonify({"error": "Invalid signature"}), 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Handle successful payment
        success = handle_successful_payment(session)
        
        if success:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "Failed to process payment"}), 500
    
    # Return success for other events
    return jsonify({"status": "received"}), 200

@payment_bp.route('/history', methods=['GET'])
@login_required
def history():
    """View transaction history"""
    transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(Transaction.created_at.desc()).limit(50).all()
    
    return render_template('payment/history.html', transactions=transactions)

# API endpoints
@payment_bp.route('/api/balance', methods=['GET'])
@login_required
def api_balance():
    """Get credit balance (API endpoint)"""
    credit = Credit.query.filter_by(user_id=current_user.id).first()
    
    if not credit:
        return jsonify({
            "balance": 0,
            "total_purchased": 0,
            "total_used": 0
        }), 200
    
    return jsonify({
        "balance": credit.balance,
        "total_purchased": credit.total_purchased,
        "total_used": credit.total_used
    }), 200

@payment_bp.route('/api/transactions', methods=['GET'])
@login_required
def api_transactions():
    """Get transaction history (API endpoint)"""
    limit = request.args.get('limit', 50, type=int)
    limit = min(limit, 100)  # Max 100 transactions
    
    transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    return jsonify({
        "transactions": [
            {
                "id": t.id,
                "amount": t.amount,
                "type": t.transaction_type,
                "description": t.description,
                "created_at": t.created_at.isoformat()
            }
            for t in transactions
        ]
    }), 200
