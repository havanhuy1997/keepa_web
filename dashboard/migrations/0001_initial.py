# Generated by Django 3.2.4 on 2021-06-27 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('domain', models.IntegerField(choices=[(1, 'com'), (2, 'co.uk'), (3, 'de'), (4, 'fr'), (5, 'co.jp'), (6, 'ca'), (8, 'it'), (9, 'es'), (10, 'in'), (11, 'com.mx')], default=1)),
                ('filter', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productType', models.IntegerField(blank=True, null=True)),
                ('asin', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('domainId', models.IntegerField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('trackingSince', models.IntegerField(blank=True, null=True)),
                ('listedSince', models.IntegerField(blank=True, null=True)),
                ('lastUpdate', models.IntegerField(blank=True, null=True)),
                ('lastRatingUpdate', models.IntegerField(blank=True, null=True)),
                ('lastPriceChange', models.IntegerField(blank=True, null=True)),
                ('lastEbayUpdate', models.IntegerField(blank=True, null=True)),
                ('imagesCSV', models.TextField(blank=True, null=True)),
                ('rootCategory', models.IntegerField(blank=True, null=True)),
                ('categories', models.JSONField(blank=True, null=True)),
                ('categoryTree', models.JSONField(blank=True, null=True)),
                ('parentAsin', models.TextField(blank=True, null=True)),
                ('variationCSV', models.TextField(blank=True, null=True)),
                ('frequentlyBoughtTogether', models.JSONField(blank=True, null=True)),
                ('eanList', models.JSONField(blank=True, null=True)),
                ('upcList', models.JSONField(blank=True, null=True)),
                ('manufacturer', models.TextField(blank=True, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
                ('productGroup', models.TextField(blank=True, null=True)),
                ('partNumber', models.TextField(blank=True, null=True)),
                ('author', models.TextField(blank=True, null=True)),
                ('binding', models.TextField(blank=True, null=True)),
                ('numberOfItems', models.IntegerField(blank=True, null=True)),
                ('numberOfPages', models.IntegerField(blank=True, null=True)),
                ('publicationDate', models.IntegerField(blank=True, null=True)),
                ('releaseDate', models.IntegerField(blank=True, null=True)),
                ('languages', models.JSONField(blank=True, null=True)),
                ('model', models.TextField(blank=True, null=True)),
                ('color', models.TextField(blank=True, null=True)),
                ('size', models.TextField(blank=True, null=True)),
                ('edition', models.TextField(blank=True, null=True)),
                ('format', models.TextField(blank=True, null=True)),
                ('features', models.JSONField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('packageHeight', models.IntegerField(blank=True, null=True)),
                ('packageLength', models.IntegerField(blank=True, null=True)),
                ('packageWidth', models.IntegerField(blank=True, null=True)),
                ('packageWeight', models.IntegerField(blank=True, null=True)),
                ('itemHeight', models.IntegerField(blank=True, null=True)),
                ('itemLength', models.IntegerField(blank=True, null=True)),
                ('itemWidth', models.IntegerField(blank=True, null=True)),
                ('itemWeight', models.IntegerField(blank=True, null=True)),
                ('availabilityAmazon', models.IntegerField(blank=True, null=True)),
                ('availabilityAmazonDelay', models.JSONField(blank=True, null=True)),
                ('ebayListingIds', models.JSONField(blank=True, null=True)),
                ('isAdultProduct', models.BooleanField(blank=True, null=True)),
                ('launchpad', models.BooleanField(blank=True, null=True)),
                ('audienceRating', models.TextField(blank=True, null=True)),
                ('newPriceIsMAP', models.BooleanField(blank=True, null=True)),
                ('isEligibleForTradeIn', models.BooleanField(blank=True, null=True)),
                ('isEligibleForSuperSaverShipping', models.BooleanField(blank=True, null=True)),
                ('fbaFees', models.JSONField(blank=True, null=True)),
                ('variations', models.JSONField(blank=True, null=True)),
                ('coupon', models.JSONField(blank=True, null=True)),
                ('promotions', models.JSONField(blank=True, null=True)),
                ('stats', models.JSONField(blank=True, null=True)),
                ('salesRankReference', models.BigIntegerField(blank=True, null=True)),
                ('salesRanks', models.JSONField(blank=True, null=True)),
                ('rentalDetails', models.TextField(blank=True, null=True)),
                ('rentalSellerId', models.TextField(blank=True, null=True)),
                ('rentalPrices', models.JSONField(blank=True, null=True)),
                ('offers', models.JSONField(blank=True, null=True)),
                ('liveOffersOrder', models.JSONField(blank=True, null=True)),
                ('buyBoxSellerIdHistory', models.JSONField(blank=True, null=True)),
                ('isRedirectASIN', models.BooleanField(blank=True, null=True)),
                ('isSNS', models.BooleanField(blank=True, null=True)),
                ('offersSuccessful', models.BooleanField(blank=True, null=True)),
                ('csv', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_asins', models.IntegerField(blank=True, null=True)),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('ended', models.DateTimeField(blank=True, default=None, null=True)),
                ('pid', models.IntegerField(blank=True, default=None, null=True)),
                ('min', models.FloatField(blank=True, default=None, null=True)),
                ('max', models.FloatField(blank=True, default=None, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.category')),
            ],
        ),
    ]
