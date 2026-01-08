from django.db import models
from django.contrib.auth.models import User

class Traveler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travelers')
    name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

# NEW: Destination Model
class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('beaches', 'Beaches'),
        ('mountains', 'Mountains'),
        ('cities', 'Cities'),
        ('nature', 'Nature'),
    ]
    
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_url = models.URLField(help_text="Enter image URL from Unsplash or other sources")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in INR")
    duration_days = models.IntegerField(help_text="Recommended duration in days")
    highlights = models.TextField(help_text="Key highlights (comma-separated)")
    is_featured = models.BooleanField(default=False, help_text="Show on homepage slider")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ['-created_at']