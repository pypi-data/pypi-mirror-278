from importlib import import_module

from django.conf import settings

module, _class = settings.PZ_SERVICE_CLASS.rsplit(".", 1)

Service = getattr(import_module(module), _class)


class CheckoutService(Service):

    def retrieve(self, request):
        path = "/orders/checkout/?page=OrderNotePage"
        response = self.get(path, request=request, headers={"X-Requested-With": "XMLHttpRequest"})
        return self.normalize_response(response)

    def get_oney_context(self, request):
        response = self.retrieve(request)
        pre_order = response.data["pre_order"]

        context = {
            "address": {
                "country_code": pre_order["shipping_address"]["country"]["code"],
                "address_line": pre_order["shipping_address"]["line"],
                "municipality": pre_order["shipping_address"]["city"]["name"],
            },
            "orders": [
                {
                    "label": item["product"]["name"],
                    "type": item["product"]["attributes"].get("integration_product_state"),
                    "item_external_code": item["product"]["sku"],
                    "quantity": item["quantity"],
                    "price": item["total_amount"],
                }
                for item in pre_order["basket"]["basketitem_set"]
            ],
        }

        return context
