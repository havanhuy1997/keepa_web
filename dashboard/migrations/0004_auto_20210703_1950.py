# Generated by Django 3.2.5 on 2021-07-03 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_product_rootcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_id',
            field=models.BigIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='rootCategory',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]