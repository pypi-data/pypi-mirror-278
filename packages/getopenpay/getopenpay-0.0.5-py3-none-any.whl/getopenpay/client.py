# -------------------------------------------- #
#  Note: please make sure you're editing       #
#  clients/custom_files/getopenpay/client.py   #
#                                              #
#  Other versions of this file will be         #
#  overwritten by the client generator.        #
# -------------------------------------------- #

from typing import NamedTuple

from getopenpay import ApiClient, Configuration


class ApiKeys(NamedTuple):
  publishable_key: str
  secret_key: str


class OpenPayClient:

  def __init__(self, api_keys: ApiKeys, host: str = 'https://connto.getopenpay.com'):
    self.api_keys = api_keys
    self.config = Configuration()
    self.config.host = host
    self.api_client = ApiClient(configuration=self.config)
    self.api_client.set_default_header('X-Publishable-Token', api_keys.publishable_key)
    self.api_client.set_default_header('Authorization', f'Bearer {api_keys.secret_key}')

  @property
  def accounts(self):
    # note these Apis are reinitialized everytime accounts are called.
    # they have lightweight inits for now
    from getopenpay.api import AccountsApi
    return AccountsApi(self.api_client)

  @property
  def authentication(self):
    from getopenpay.api import AuthenticationApi
    return AuthenticationApi(self.api_client)

  @property
  def chartmogul(self):
    from getopenpay.api import ChartmogulIntegrationApi
    return ChartmogulIntegrationApi(self.api_client)

  @property
  def coupons(self):
    from getopenpay.api import CouponsApi
    return CouponsApi(self.api_client)

  @property
  def credit_notes(self):
    from getopenpay.api import CreditNotesApi
    return CreditNotesApi(self.api_client)

  @property
  def users(self):
    from getopenpay.api import UsersApi
    return UsersApi(self.api_client)

  @property
  def customers(self):
    from getopenpay.api import CustomersApi
    return CustomersApi(self.api_client)

  @property
  def invites(self):
    from getopenpay.api import InvitesApi
    return InvitesApi(self.api_client)

  @property
  def invoice_items(self):
    from getopenpay.api import InvoiceItemsApi
    return InvoiceItemsApi(self.api_client)

  @property
  def invoices(self):
    from getopenpay.api import InvoicesApi
    return InvoicesApi(self.api_client)

  @property
  def payment_methods(self):
    from getopenpay.api import PaymentMethodsApi
    return PaymentMethodsApi(self.api_client)

  @property
  def prices(self):
    from getopenpay.api import PricesApi
    return PricesApi(self.api_client)

  @property
  def products(self):
    from getopenpay.api import ProductsApi
    return ProductsApi(self.api_client)

  @property
  def promotion_codes(self):
    from getopenpay.api import PromotionCodesApi
    return PromotionCodesApi(self.api_client)

  @property
  def refunds(self):
    from getopenpay.api import RefundsApi
    return RefundsApi(self.api_client)

  @property
  def subscription_items(self):
    from getopenpay.api import SubscriptionItemsApi
    return SubscriptionItemsApi(self.api_client)

  @property
  def subscriptions(self):
    from getopenpay.api import SubscriptionsApi
    return SubscriptionsApi(self.api_client)

  @property
  def charges(self):
    from getopenpay.api import ChargesApi
    return ChargesApi(self.api_client)

  @property
  def events(self):
    from getopenpay.api import EventsApi
    return EventsApi(self.api_client)

  @property
  def transition_eligibility(self):
    from getopenpay.api import TransitionEligibilityApi
    return TransitionEligibilityApi(self.api_client)

  @property
  def checkout(self):
    from getopenpay.api import CheckoutApi
    return CheckoutApi(self.api_client)

  @property
  def product_family(self):
    from getopenpay.api import ProductFamilyApi
    return ProductFamilyApi(self.api_client)

  @property
  def billing_portal(self):
    from getopenpay.api import BillingPortalApi
    return BillingPortalApi(self.api_client)

  @property
  def tax_integrations(self):
    from getopenpay.api import TaxIntegrationsApi
    return TaxIntegrationsApi(self.api_client)

  @property
  def processor(self):
    from getopenpay.api import ProcessorsApi
    return ProcessorsApi(self.api_client)

  @property
  def webhook_utils(self):
    from getopenpay.utils.webhook_utils import WebhookUtils
    return WebhookUtils()
