from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(default='Aucun email')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Subscriber(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='subscriber')
    name = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    siret = models.CharField(max_length=150)
    returned_report = models.CharField(max_length=100, null=True, default='Pas reçu', blank=True)

    def __str__(self):
        return f'{self.customer.id} - {self.customer.first_name} {self.customer.last_name}'
