from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from mainapp.models import Order


# class OrderForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['order_date'].label = 'Дата получения'
#
#     order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'min': f"{datetime.today().strftime('%Y-%m-%d')}"}))
#     first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'pizda', 'placeholder': 'Борис'}))
#     last_name = forms.CharField(label='Фамилмя', widget=forms.TextInput(attrs={'placeholder': 'Немцов'}))
#     phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'placeholder': '+7 (987) 654 32 10'}))
#     address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={'placeholder': 'г. Москва, ул. Поддубная...'}))
#     comment = forms.CharField(label='Комментарий к заказу',widget=forms.Textarea(attrs={'class': 'fs20','placeholder': 'Ваш комментарий...'}))
#     products_information = forms.CharField(label='',widget=forms.Textarea(attrs={'class': 'full_invisible_absolute'}))
#
#     def clean_date(self):
#         order_date = self.cleaned_data['date']
#         if order_date < datetime.date.today():
#             raise forms.ValidationError("The date cannot be in the past!")
#         return order_date
#     class Meta:
#         model = Order
#         fields = (
#             'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment','products_information'
#         )

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Login'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    class Meta:
        fields = ('username', 'password')
class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения'

    buying_type = forms.ChoiceField(choices=Order.BUYING_TYPE_CHOICES,widget=forms.Select(attrs={'class':'col-md-4 form-select me-4'}))
    order_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date', 'min': f"{datetime.today().strftime('%Y-%m-%d')}"}))
    order_time = forms.TimeField(required=False,widget=forms.TextInput(attrs={'type': 'time', 'min': f"{datetime.today().strftime('%CC-%MM')}"}))
    comment = forms.CharField(label='Комментарий к заказу',widget=forms.Textarea(attrs={'class': 'fs20','placeholder': 'Ваш комментарий...'}))
    products_information = forms.CharField(label='',widget=forms.Textarea(attrs={'class': 'full_invisible_absolute'}))
    # buying_type = forms.RadioSelect(label='Комментарий к заказу')
    def clean_date(self):
        order_date = self.cleaned_data['date']
        if order_date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return order_date
    class Meta:
        model = Order
        fields = (
            'buying_type', 'order_date', 'order_time', 'comment','products_information'
        )