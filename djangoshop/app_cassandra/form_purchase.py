from django import forms


class PurchaseForm(forms.Form):

    email = forms.EmailField(label='Your email', max_length=90, required=True)

    repeat_email = forms.EmailField(label='Repeat email', max_length=90,
                                    required=True)

    quantity = forms.DecimalField(label='Quantity', min_value=1, max_value=999,
                                  required=True)