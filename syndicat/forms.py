from django import forms
from django.core.exceptions import ValidationError

from syndicat.models import Customer, Subscriber

#Formulaire pour les clients
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'john.doe@mail.com'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError("Le prénom est requis")
        if len(first_name) < 2:
            raise ValidationError("Le prénom est trop court")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise ValidationError("Le nom est requis")
        if len(last_name) < 2:
            raise ValidationError("Le nom est trop court")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Cet email est déjà utilisé")

        return email

#Formulaire pour les adhérents
class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('name', 'phone', 'adress', 'postal_code', 'city', 'siret', 'returned_report')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'JohnDoe & Ci'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+33 1 23 45 67 89'}),
            'adress': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '2 rue des tulipes'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '12345'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Paris'}),
            'siret': forms.TextInput(attrs={'class': 'form-input','placeholder':'01234567890123'}),
            'returned_report': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ne rien mettre si pas reçu'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Le nom de l’entreprise est requis")
        if len(name) < 2:
            raise ValidationError("Le nom de l’entreprise est trop court")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        cleaned_phone = phone.replace(' ', '') if phone else ''

        if not cleaned_phone.isdigit():
            raise ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres (espaces autorisés)")

        if len(cleaned_phone) < 10:
            raise ValidationError("Le numéro de téléphone semble trop court")

        return cleaned_phone

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code:
            raise ValidationError("Le code postal est requis")
        if not postal_code.isdigit() or len(postal_code) != 5:
            raise ValidationError("Le code postal doit contenir 5 chiffres")
        return postal_code

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise ValidationError("La ville est requise.")
        return city

    def clean_siret(self):
        siret = self.cleaned_data.get('siret')
        if not siret:
            raise ValidationError("Le numéro SIRET est requis")
        return siret