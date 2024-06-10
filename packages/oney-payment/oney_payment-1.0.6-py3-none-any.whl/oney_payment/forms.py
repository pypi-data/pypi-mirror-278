from django import forms


class AddressForm(forms.Form):
    country_code = forms.CharField()
    address_line = forms.CharField()
    municipality = forms.CharField()

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)


class OrderForm(forms.Form):
    label = forms.CharField()
    type = forms.IntegerField()
    item_external_code = forms.CharField()
    quantity = forms.IntegerField()
    price = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)


class HashForm(forms.Form):
    hash = forms.CharField()
    salt = forms.CharField()

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
