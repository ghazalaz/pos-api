# Generated by Django 3.2.8 on 2021-10-27 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModifireGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ModifireItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bonus.modifiregroup')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('created', 'Created'), ('failed', 'Failed')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('menu_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bonus.menuitem')),
                ('modifier_group', models.ManyToManyField(to='bonus.ModifireGroup')),
                ('modifiers', models.ManyToManyField(to='bonus.ModifireItem')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bonus.order')),
            ],
        ),
    ]
