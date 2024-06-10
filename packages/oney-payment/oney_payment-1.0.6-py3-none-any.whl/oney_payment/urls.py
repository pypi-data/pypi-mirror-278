from django.conf.urls import url

from oney_payment.views import OneyExtensionRedirectView

urlpatterns = [
    url(r"^$", OneyExtensionRedirectView.as_view(), name="extension_redirect"),
]
