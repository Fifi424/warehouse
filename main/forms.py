from django import forms
from .models import PvzLocation
from django.contrib.auth.models import User

class PvzLocationForm(forms.ModelForm):
    class Meta:
        model = PvzLocation
        fields = ['name', 'phone_number', 'rent_paid_until']

    name = forms.CharField(label="Название ПВЗ", max_length=100)
    phone_number = forms.CharField(label="Телефон", max_length=20)
    rent_paid_until = forms.DateField(label="Аренда оплачена до", widget=forms.DateInput(attrs={'type': 'date'}))

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
