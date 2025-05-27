from django.conf import settings
from transbank.webpay.webpay_plus.transaction import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
# Configura Webpay al inicio (hazlo solo una vez, idealmente en una función init o middleware)
Transaction.build_for_integration(
    commerce_code='597055555532',
    api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
)

webpay_options = WebpayOptions(
    commerce_code=settings.WEBPAY_CONFIG['COMMERCE_CODE'],
    api_key=settings.WEBPAY_CONFIG['API_KEY'],
    integration_type=IntegrationType.TEST
)
