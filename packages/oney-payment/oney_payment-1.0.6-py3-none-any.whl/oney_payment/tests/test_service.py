import json

from django.conf import settings
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


@override_settings(PZ_SERVICE_CLASS="oney_payment.commerce.dummy.Service")
class TestCheckoutService(SimpleTestCase, MockResponseMixin):
    def setUp(self):
        from oney_payment.commerce.checkout import CheckoutService
        self.service = CheckoutService()
        self.request_factory = RequestFactory()

    @patch("oney_payment.commerce.dummy.Service.get")
    def test_retrieve(self, mock_get):
        mocked_response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"}
        )
        mock_get.return_value = mocked_response

        request = self.request_factory.get("/payment-gateway/oney/")
        response = self.service.retrieve(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("pre_order", response.data)

    @patch("oney_payment.commerce.dummy.Service.get")
    def test_get_oney_context(self, mock_get):
        mocked_response = self._mock_response(
            status_code=200,
            content=self._get_response("orders_checkout_response"),
            headers={"Content-Type": "application/json"}
        )
        mock_get.return_value = mocked_response

        checkout_response = self._get_response("orders_checkout_response")
        pre_order = json.loads(checkout_response)["pre_order"]

        request = self.request_factory.get("/payment-gateway/oney/")
        oney_context = self.service.get_oney_context(request)

        address = oney_context["address"]
        shipping_address = pre_order["shipping_address"]
        self.assertEqual(address["country_code"], shipping_address["country"]["code"])
        self.assertEqual(address["address_line"], shipping_address["line"])
        self.assertEqual(address["municipality"], shipping_address["city"]["name"])

        orders = oney_context["orders"]
        basket_items = pre_order["basket"]["basketitem_set"]
        self.assertEqual(len(orders), len(basket_items))

        for order, basket_item in zip(orders, basket_items):
            self.assertEqual(order["label"], basket_item["product"]["name"])
            self.assertEqual(order["type"], basket_item["product"]["attributes"]["integration_product_state"])
            self.assertEqual(order["item_external_code"], basket_item["product"]["sku"])
            self.assertEqual(order["quantity"], basket_item["quantity"])
            self.assertEqual(order["price"], basket_item["total_amount"])
