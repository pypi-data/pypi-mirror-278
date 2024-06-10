import hashlib
import uuid

from django.conf import settings
from django.forms import formset_factory
from django.template.response import TemplateResponse
from django.views.generic import View

from oney_payment.commerce.checkout import CheckoutService
from oney_payment.forms import OrderForm, AddressForm, HashForm


class OneyExtensionRedirectView(View):
    checkout_service = CheckoutService()

    def get(self, request):
        context = self.checkout_service.get_oney_context(request)
        session_id = request.GET.get("sessionId")

        OrderFormSet = formset_factory(OrderForm, extra=0)
        address_form = AddressForm(initial=context["address"])
        order_formset = OrderFormSet(initial=context["orders"])

        salt = uuid.uuid4().hex[:10]
        hash_str = f"{salt}|{session_id}|{settings.HASH_SECRET_KEY}"
        _hash = hashlib.sha512(hash_str.encode("utf-8")).hexdigest()
        hash_form = HashForm(initial={"hash": _hash, "salt": salt})

        return TemplateResponse(
            request=request,
            template="oney-extension-redirect-form.html",
            context={
                "action_url": f"{settings.ONEY_EXTENSION_URL}?sessionId={session_id}",
                "action_method": "POST",
                "address_form": address_form,
                "order_formset": order_formset,
                "hash_form": hash_form,
            }
        )
