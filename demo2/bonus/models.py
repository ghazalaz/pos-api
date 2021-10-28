from django.db import models


class ModifierGroup(models.Model):
    name = models.CharField(max_length=200)

    def __repr__(self):
        return '<ModifireGroup object ({}) "{}">'.format(self.id, self.name)

    def __str__(self):
        return '<ModifireGroup object ({}) "{}">'.format(self.id, self.name)


class ModifierItem(models.Model):
    group = models.ForeignKey(ModifierGroup, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = [['name', 'group']]


    def __repr__(self):
        return '<ModifireItem object ({}) "{}">'.format(self.id, self.name)

    def __str__(self):
        return '<ModifireItem object ({}) "{}">'.format(self.id, self.name)


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __repr__(self):
        return '<MenuItem object ({}) "{}">'.format(self.id, self.name)

    def __str__(self):
        return '<MenuItem object ({}) "{}">'.format(self.id, self.name)


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
        return '<OrdertItem object ({}) {}x "{}">'.format(self.id, self.quantity, self.menu_item.id)

    def __str__(self):
        return '<OrdertItem object ({}) {}x "{}">'.format(self.id, self.quantity, self.menu_item.id)

class OrderModifier(models.Model):
    order_item = models.ForeignKey(OrderItem, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(ModifierGroup, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(ModifierItem,null=True, on_delete=models.SET_NULL)



