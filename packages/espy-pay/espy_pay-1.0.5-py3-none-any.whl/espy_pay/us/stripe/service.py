import stripe
from espy_pay.us.stripe.CONSTANTS import STRIPE_KEY
from espy_pay.general.schema import TranxDto
def create_stripe(data: TranxDto):
    """
    This function creates a payment intent on Stripe.
    Args:
        data (dict): A dictionary containing the payment data.
    """
    try:
        stripe.api_key = STRIPE_KEY
        intent = stripe.PaymentIntent.create(
            amount=data["amount"],
            currency=data["currency"],
            payment_method=data["payment_method"],
            confirmation_method="manual",
            confirm=True,
        )
        return intent
    except stripe.error as e:
        raise e