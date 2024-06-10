from django.conf import settings
from django.template.response import TemplateResponse
from django.test import SimpleTestCase
from django.test import override_settings
from django.test.client import RequestFactory
from mock.mock import patch
from rest_framework import status

from oney_payment.tests.mixins import MockResponseMixin

try:
    settings.configure()
except RuntimeError:
    pass


@override_settings(
    ONEY_EXTENSION_URL="oney/extension_url",
    PZ_SERVICE_CLASS="oney_payment.commerce.dummy.Service",
    HASH_SECRET_KEY="hash_secret_key",
)
class TestOneyExtensionRedirectView(SimpleTestCase, MockResponseMixin):

    def setUp(self):
        self.request_factory = RequestFactory()

    @patch("oney_payment.commerce.dummy.Service.get")
    def test_get(self, mock_get):
        from oney_payment.views import OneyExtensionRedirectView

        response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"}
        )
        mock_get.return_value = response

        request = self.request_factory.get("/payment-gateway/oney/")
        response = OneyExtensionRedirectView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.template_name, "oney-extension-redirect-form.html")

        context = response.context_data
        self.assertIn("action_url", context)
        self.assertIn("action_method", context)
        self.assertIn("address_form", context)
        self.assertIn("order_formset", context)
        self.assertIn("hash_form", context)
