"""
Billing endpoints - PLACEHOLDER FOR PAYMENT INTEGRATION
These endpoints are NOT implemented in MVP but are structured
for easy Stripe/Razorpay integration.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User, PlanTier
from app.schemas.schemas import UpgradeRequest, WebhookEvent
from app.api.dependencies import get_current_user
from app.services.tier_service import upgrade_user_plan
from datetime import datetime, timedelta


router = APIRouter()


@router.post("/billing/upgrade")
def upgrade_plan(
    request: UpgradeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    PLACEHOLDER: Upgrade user plan.
    
    TODO: Integrate with Stripe or Razorpay
    
    Integration Steps:
    1. Create Stripe/Razorpay Checkout Session
    2. Redirect user to payment page
    3. Handle webhook to confirm payment
    4. Call upgrade_user_plan() after successful payment
    
    Stripe Example:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': PLAN_PRICE_IDS[request.plan],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'{settings.FRONTEND_URL}/success',
            cancel_url=f'{settings.FRONTEND_URL}/cancel',
            client_reference_id=str(current_user.id)
        )
        
        return {"checkout_url": session.url}
    
    Razorpay Example:
        import razorpay
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        order = client.order.create({
            'amount': PLAN_PRICES[request.plan] * 100,  # paise
            'currency': 'INR',
            'receipt': f'order_{current_user.id}',
            'notes': {'plan': request.plan}
        })
        
        return {"order_id": order['id'], "amount": order['amount']}
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "message": "Payment integration not yet implemented. This is a placeholder endpoint.",
            "payment_provider": request.payment_method,
            "target_plan": request.plan,
            "documentation": "See README.md for integration guide"
        }
    )


@router.post("/billing/webhook")
async def payment_webhook(request: Request, db: Session = Depends(get_db)):
    """
    PLACEHOLDER: Handle payment webhook.
    
    TODO: Integrate with Stripe or Razorpay webhooks
    
    Stripe Webhook:
        import stripe
        
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = int(session['client_reference_id'])
            
            # Determine plan from price_id
            plan = get_plan_from_price_id(session['price_id'])
            expires_at = datetime.utcnow() + timedelta(days=30)
            
            # Upgrade user
            upgrade_user_plan(user_id, plan, expires_at, db)
        
        return {"status": "success"}
    
    Razorpay Webhook:
        import razorpay
        from razorpay.utility import Utility
        
        payload = await request.body()
        signature = request.headers.get('x-razorpay-signature')
        
        # Verify signature
        Utility.verify_webhook_signature(
            payload.decode('utf-8'),
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )
        
        data = await request.json()
        
        if data['event'] == 'payment.captured':
            payment = data['payload']['payment']['entity']
            user_id = int(payment['notes']['user_id'])
            plan = PlanTier[payment['notes']['plan']]
            
            expires_at = datetime.utcnow() + timedelta(days=30)
            upgrade_user_plan(user_id, plan, expires_at, db)
        
        return {"status": "success"}
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "message": "Webhook not yet implemented. This is a placeholder endpoint.",
            "documentation": "See README.md for webhook integration guide"
        }
    )


@router.get("/billing/plans")
def get_pricing_plans():
    """
    Get pricing information for all plans.
    This endpoint IS implemented and returns static pricing data.
    """
    return {
        "plans": [
            {
                "tier": "FREE",
                "name": "Free Trial",
                "price": 0,
                "currency": "USD",
                "billing_cycle": "forever",
                "features": [
                    "3 AI resume improvements",
                    "1 resume only",
                    "1 basic template",
                    "PDF export with watermark",
                    "No resume summary",
                    "No project generation"
                ],
                "limitations": [
                    "Limited AI usage",
                    "Watermarked exports",
                    "Single resume"
                ]
            },
            {
                "tier": "PRO",
                "name": "Professional",
                "price": 9.99,
                "currency": "USD",
                "billing_cycle": "monthly",
                "features": [
                    "50 AI actions per month",
                    "10 resumes",
                    "All templates unlocked",
                    "PDF export - no watermark",
                    "Project description generation",
                    "Resume summary generation",
                    "Basic tone control"
                ],
                "popular": True
            },
            {
                "tier": "ULTIMATE",
                "name": "Ultimate",
                "price": 19.99,
                "currency": "USD",
                "billing_cycle": "monthly",
                "features": [
                    "Unlimited AI usage",
                    "Unlimited resumes",
                    "All templates + future releases",
                    "Advanced resume rewriting",
                    "Advanced tone options",
                    "Priority AI processing",
                    "Early access to features"
                ],
                "recommended_for": "Power users & job agencies"
            }
        ]
    }
