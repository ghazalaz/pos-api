# Generated by Django 3.2.8 on 2021-10-26 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20211025_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_item',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('failed', 'Failed')], default='created', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order'),
        ),
    ]