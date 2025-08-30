from django import forms

class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=255, label="Имя Фамилия")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=20, required=False, label="Телефон")
    address = forms.CharField(widget=forms.Textarea, label="Адрес")
