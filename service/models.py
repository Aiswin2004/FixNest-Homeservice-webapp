from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    """
    Provider categories: Roses, Lilies, Orchids, Sunproviders, etc.
    DDL: CREATE TABLE shop_category (id INTEGER PRIMARY KEY, name VARCHAR(100), ...)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
# Create your models here.
class Provider(models.Model):
    """
    Individual provider products.
    ForeignKey = Database Relation (Many providers → One category)
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name="provider")
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='providers')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    adhaar_no = models.CharField(max_length=20,blank=True, null=True)
    provider_address = models.CharField(max_length=255, blank=True, null=True)
    #image_url = models.URLField(blank=True, default='')
    image = models.ImageField(upload_to='providers/', blank=True, null=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    is_featured = models.BooleanField(default=False)
    is_bestworker = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    is_approved = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0
    
    @property
    def image_url(self):
        try:
            if self.image and self.image.name:
                return self.image.url
        except Exception:
            pass
        return ''
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Provider.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

class ProviderWork(models.Model):
    """
    Stores recently completed works of a provider.
    One provider can have many completed works.
    """

    provider = models.ForeignKey(Provider,on_delete=models.CASCADE,related_name='works')

    work_title = models.CharField(max_length=200)

    work_image = models.ImageField(upload_to='provider_works/')

    customer_name = models.CharField(max_length=150)

    customer_phone = models.CharField(max_length=15)

    work_address = models.TextField()

    completed_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.provider.name} - {self.work_title}"
    

    
class ProviderBlockedDate(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField()
    unavailable_time = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.provider} blocked until {self.end_time}"




class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="provider_bookings"
    )

    customer_name = models.CharField(max_length=100)

    customer_phone = models.CharField(max_length=15)

    service_address = models.TextField()

    booking_date = models.DateField()

    booking_time = models.TimeField()

    problem_description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} → {self.provider.name}"