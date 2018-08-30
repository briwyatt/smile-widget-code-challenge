from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')

    def __str__(self):
        return '{} - {}'.format(self.name)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} - ${} discount'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)


class ProductPrice(models.Model):
    title = models.CharField(max_length=50, help_text='Description of this pricing schedule for product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}: {}'.format(self.title, self.product.name, self.formatted_price)


    @property
    def formatted_price(self):
        return '${0:.2f}'.format(self.price / 100)
