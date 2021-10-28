from django.db import models


class MenuItem(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __repr__(self):
        return '<MenuItem object ({}) "{}">'.format(self.id, self.description)

    def __str__(self):
        return '<MenuItem object ({}) "{}">'.format(self.id, self.description)

class Order(models.Model):
    class Status:
        CHOICES = (
            ('created', 'Created'),
            ('failed', 'Failed'),
        )
        CREATED = 'created'
        FAILED = 'failed'

    note = models.TextField(null=True, blank=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=Status.CHOICES, max_length=20)

    def __repr__(self):
        return '<Order object ({}) "{}">'.format(self.id, self.note)

    def __str__(self):
        return '<Order object ({}) "{}">'.format(self.id, self.note)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    menu_item = models.ForeignKey(MenuItem, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()

    def __repr__(self):
        return '<OrdertItem object ({}) {}x "{}">'.format(self.id, self.quantity, self.product.id)

    def __str__(self):
        return '<OrdertItem object ({}) {}x "{}">'.format(self.id, self.quantity, self.product.id)





