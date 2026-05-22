"""
Subscription management endpoints using Stripe.

Handles checkout sessions, webhooks, and subscription status.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Depends, status
from sqlalchemy.orm import Session
import secrets

from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.config import settings
from app.services.limits import get_usage_summary, get_user_limits

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


def get_stripe():
    """Get configured Stripe client or raise error."""
    if not STRIPE_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe is not configured"
        )
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe API key not configured"
        )
    stripe.api_key = settings.stripe_secret_key
    return stripe


@router.get("/status")
def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's subscription status.
    """
    return {
        "tier": current_user.subscription_tier or "free",
        "status": current_user.subscription_status or "active",
        "ends_at": current_user.subscription_ends_at,
        "stripe_customer_id": current_user.stripe_customer_id,
        "referral_code": current_user.referral_code,
        "referral_count": current_user.referral_count or 0
    }


@router.get("/usage")
def get_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current usage and limits for the user.
    """
    return get_usage_summary(current_user, db)


@router.post("/checkout")
def create_checkout_session(
    plan: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a Stripe checkout session for subscription.

    Args:
        plan: 'pro' or 'pro_plus'
    """
    stripe_client = get_stripe()

    # Validate plan
    if plan not in ["pro", "pro_plus"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan. Must be 'pro' or 'pro_plus'"
        )

    # Get price ID
    price_id = settings.stripe_pro_price_id if plan == "pro" else settings.stripe_pro_plus_price_id

    if not price_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Price ID for {plan} not configured"
        )

    # Create or get Stripe customer
    if not current_user.stripe_customer_id:
        customer = stripe_client.Customer.create(
            email=current_user.email,
            metadata={"user_id": current_user.id}
        )
        current_user.stripe_customer_id = customer.id
        db.commit()

    # Create checkout session
    try:
        session = stripe_client.checkout.Session.create(
            customer=current_user.stripe_customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            mode="subscription",
            success_url=f"{settings.frontend_url}/dashboard?subscription=success",
            cancel_url=f"{settings.frontend_url}/pricing?subscription=canceled",
            metadata={
                "user_id": current_user.id,
                "plan": plan
            },
            subscription_data={
                "trial_period_days": 14,
                "metadata": {
                    "user_id": current_user.id,
                    "plan": plan
                }
            }
        )

        return {"checkout_url": session.url, "session_id": session.id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create checkout session: {str(e)}"
        )


@router.post("/portal")
def create_portal_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a Stripe customer portal session for managing subscription.
    """
    stripe_client = get_stripe()

    if not current_user.stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription found"
        )

    try:
        session = stripe_client.billing_portal.Session.create(
            customer=current_user.stripe_customer_id,
            return_url=f"{settings.frontend_url}/settings"
        )

        return {"portal_url": session.url}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create portal session: {str(e)}"
        )


@router.post("/cancel")
def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel the current subscription at period end.
    """
    stripe_client = get_stripe()

    if not current_user.stripe_subscription_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription to cancel"
        )

    try:
        # Cancel at period end (not immediately)
        stripe_client.Subscription.modify(
            current_user.stripe_subscription_id,
            cancel_at_period_end=True
        )

        current_user.subscription_status = "canceled"
        db.commit()

        return {"message": "Subscription will be canceled at the end of the billing period"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel subscription: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events.
    """
    if not STRIPE_AVAILABLE or not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe not configured"
        )

    stripe.api_key = settings.stripe_secret_key

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe signature"
        )

    try:
        if settings.stripe_webhook_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.stripe_webhook_secret
            )
        else:
            # In development without webhook secret
            import json
            event = json.loads(payload)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payload"
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )

    # Handle events
    event_type = event.get("type") if isinstance(event, dict) else event.type
    data = event.get("data", {}).get("object", {}) if isinstance(event, dict) else event.data.object

    if event_type == "checkout.session.completed":
        await handle_checkout_completed(data, db)

    elif event_type == "customer.subscription.updated":
        await handle_subscription_updated(data, db)

    elif event_type == "customer.subscription.deleted":
        await handle_subscription_deleted(data, db)

    elif event_type == "invoice.payment_failed":
        await handle_payment_failed(data, db)

    return {"status": "success"}


async def handle_checkout_completed(session: dict, db: Session):
    """Handle successful checkout."""
    user_id = session.get("metadata", {}).get("user_id")
    plan = session.get("metadata", {}).get("plan", "pro")

    if not user_id:
        return

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return

    subscription_id = session.get("subscription")

    user.stripe_subscription_id = subscription_id
    user.subscription_tier = plan
    user.subscription_status = "active"
    db.commit()


async def handle_subscription_updated(subscription: dict, db: Session):
    """Handle subscription update (upgrade/downgrade)."""
    customer_id = subscription.get("customer")

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        return

    status = subscription.get("status")
    user.subscription_status = status

    # Update end date
    current_period_end = subscription.get("current_period_end")
    if current_period_end:
        user.subscription_ends_at = datetime.fromtimestamp(current_period_end)

    db.commit()


async def handle_subscription_deleted(subscription: dict, db: Session):
    """Handle subscription cancellation."""
    customer_id = subscription.get("customer")

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        return

    user.subscription_tier = "free"
    user.subscription_status = "canceled"
    user.stripe_subscription_id = None
    db.commit()


async def handle_payment_failed(invoice: dict, db: Session):
    """Handle failed payment."""
    customer_id = invoice.get("customer")

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        return

    user.subscription_status = "past_due"
    db.commit()


# Referral endpoints
@router.get("/referral-code")
def get_referral_code(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get or generate referral code for current user.
    """
    if not current_user.referral_code:
        # Generate unique referral code
        code = secrets.token_urlsafe(6).upper()[:8]
        current_user.referral_code = code
        db.commit()

    return {
        "referral_code": current_user.referral_code,
        "referral_count": current_user.referral_count or 0,
        "referral_link": f"{settings.frontend_url}/register?ref={current_user.referral_code}"
    }


@router.post("/apply-referral")
def apply_referral_code(
    code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Apply a referral code to current user's account.
    """
    if current_user.referred_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already used a referral code"
        )

    # Find referrer
    referrer = db.query(User).filter(User.referral_code == code.upper()).first()

    if not referrer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid referral code"
        )

    if referrer.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot use your own referral code"
        )

    # Apply referral
    current_user.referred_by = referrer.id
    referrer.referral_count = (referrer.referral_count or 0) + 1
    db.commit()

    return {
        "message": "Referral code applied successfully",
        "referrer_id": referrer.id
    }
