import threading

import jsonfield
from django.db import models
from django.db.models.signals import post_save
from djongo import models as mongo_models
import psutil
from django.utils.html import format_html
from django.urls import reverse

import utils.log as ut_log
import utils.dt as ut_dt
from keepa_web.settings import LOG_DIR
from dashboard import tasks


# Create your models here.
class Category(models.Model):
    MARKET_CHOOSE = [
       (1, "com"), (2, "co.uk"), (3, "de"), (4, "fr"), (5, "co.jp"),
       (6, "ca"), (8, "it"), (9, "es"), (10, "in"), (11, "com.mx")
    ]
    id = models.IntegerField(primary_key=True)
    title = models.TextField(null=True, blank=True)
    domain = models.IntegerField(
        default=1, choices=MARKET_CHOOSE
    )

    def __str__(self) -> str:
        return f"{str(self.id)} - {str(self.title)}"

    def total_asin(self):
        return Product.objects.filter(rootCategory=self.id).count()

    def has_running_task(self):
        for task in Task.objects.filter(category=self):
            if task.is_running():
                return True
        return False


class Task(models.Model):
    _id = mongo_models.ObjectIdField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_asins = models.IntegerField(null=True, blank=True)
    started = models.DateTimeField(null=True, blank=True)
    ended = models.DateTimeField(null=True, blank=True, default=None)
    pid = models.IntegerField(null=True, blank=True, default=None)
    min = models.FloatField(null=True, blank=True, default=None)
    max = models.FloatField(null=True, blank=True, default=None)

    def got(self):
        return self.category.total_asin()

    def message(self):
        file_log = self.get_file_log()
        last_line = ut_log.get_last_line_of_file(file_log)
        return last_line.split("-")[-1].strip()

    def get_file_log(self):
        return str(LOG_DIR / f"{str(self._id)}.txt")

    def get_process(self):
        process = None
        if not self.pid:
            return process
        try:
            process = psutil.Process(self.pid)
        except:
            pass
        return process

    def is_running(self):
        process = self.get_process()
        if not process:
            return False
        return process.is_running()

    def start(self):
        if not self.is_running():
            thread = threading.Thread(target=tasks.start_task, args=(self,))
            thread.start()
            self.started=ut_dt.get_time_now()
            self.ended = None
            self.pid = thread.native_id
            self.save()

    def action_button(self):
        if not self.is_running():
            return format_html(
                f"<a href='{reverse('task-control', args=(self._id,))}'>Restart</a>"
            )
        return ""

    def getting_price_in_range(self):
        return f"{self.min} - {self.max}"


class Product(models.Model):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    productType = models.IntegerField(null=True, blank=True)
    asin = models.CharField(primary_key=True, max_length=20)
    domainId = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    trackingSince = models.IntegerField(null=True, blank=True)
    listedSince = models.IntegerField(null=True, blank=True)
    lastUpdate = models.IntegerField(null=True, blank=True)
    lastRatingUpdate = models.IntegerField(null=True, blank=True) 
    lastPriceChange = models.IntegerField(null=True, blank=True)
    lastEbayUpdate = models.IntegerField(null=True, blank=True)
    imagesCSV = models.TextField(null=True, blank=True)
    rootCategory = models.IntegerField(null=True, blank=True)
    categories = jsonfield.JSONField(null=True, blank=True)
    categoryTree = jsonfield.JSONField(null=True, blank=True)
    parentAsin = models.TextField(null=True, blank=True)
    variationCSV = models.TextField(null=True, blank=True)
    frequentlyBoughtTogether = jsonfield.JSONField(null=True, blank=True)
    eanList = jsonfield.JSONField(null=True, blank=True)
    upcList = jsonfield.JSONField(null=True, blank=True)
    manufacturer = models.TextField(null=True, blank=True)
    brand = models.TextField(null=True, blank=True)
    productGroup = models.TextField(null=True, blank=True)
    partNumber = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    binding = models.TextField(null=True, blank=True)
    numberOfItems = models.IntegerField(null=True, blank=True)
    numberOfPages = models.IntegerField(null=True, blank=True)
    publicationDate = models.IntegerField(null=True, blank=True)
    releaseDate = models.IntegerField(null=True, blank=True)
    languages  = jsonfield.JSONField(null=True, blank=True)
    model = models.TextField(null=True, blank=True)
    color = models.TextField(null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    edition = models.TextField(null=True, blank=True)
    format = models.TextField(null=True, blank=True)
    features = jsonfield.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    packageHeight = models.IntegerField(null=True, blank=True)
    packageLength = models.IntegerField(null=True, blank=True)
    packageWidth = models.IntegerField(null=True, blank=True)
    packageWeight = models.IntegerField(null=True, blank=True)
    itemHeight = models.IntegerField(null=True, blank=True)
    itemLength = models.IntegerField(null=True, blank=True)
    itemWidth = models.IntegerField(null=True, blank=True)
    itemWeight = models.IntegerField(null=True, blank=True)
    availabilityAmazon = models.IntegerField(null=True, blank=True)
    availabilityAmazonDelay = jsonfield.JSONField(null=True, blank=True)
    ebayListingIds = jsonfield.JSONField(null=True, blank=True)
    isAdultProduct = models.BooleanField(null=True, blank=True)
    launchpad = models.BooleanField(null=True, blank=True)
    audienceRating = models.TextField(null=True, blank=True)
    newPriceIsMAP = models.BooleanField(null=True, blank=True)
    isEligibleForTradeIn = models.BooleanField(null=True, blank=True)
    isEligibleForSuperSaverShipping = models.BooleanField(null=True, blank=True)
    fbaFees = jsonfield.JSONField(null=True, blank=True)
    variations = jsonfield.JSONField(null=True, blank=True)
    coupon = jsonfield.JSONField(null=True, blank=True)
    promotions = jsonfield.JSONField(null=True, blank=True)
    stats = jsonfield.JSONField(null=True, blank=True)
    salesRankReference = models.BigIntegerField(null=True, blank=True)
    salesRanks = jsonfield.JSONField(null=True, blank=True)
    rentalDetails = models.TextField(null=True, blank=True)
    rentalSellerId = models.TextField(null=True, blank=True)
    rentalPrices = jsonfield.JSONField(null=True, blank=True)
    offers = jsonfield.JSONField(null=True, blank=True)
    liveOffersOrder = jsonfield.JSONField(null=True, blank=True)
    buyBoxSellerIdHistory = jsonfield.JSONField(null=True, blank=True)
    isRedirectASIN = models.BooleanField(null=True, blank=True)
    isSNS = models.BooleanField(null=True, blank=True)
    offersSuccessful = models.BooleanField(null=True, blank=True)
    csv = jsonfield.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.asin


    def set_data(self, data):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)


def start_task(sender, instance, *args, **kwargs):
    if instance.has_running_task():
        return
    task = Task.objects.create(category=instance)
    task.start()

post_save.connect(start_task, sender=Category)
