from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Outfit(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='outfits')
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    image = models.ImageField(upload_to='outfits/')
    stock = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rented', 'Rented'),
        ('Returned', 'Returned'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        delta = self.end_date - self.start_date
        days = delta.days if delta.days > 0 else 1
        self.total_price = days * self.outfit.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.outfit.name}"

class LateFee(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    days_late = models.IntegerField()
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Late Fee for {self.booking}"
