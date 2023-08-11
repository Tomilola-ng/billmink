from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from accounts.models import Profile
from .choices import donation_types
from django.utils.text import slugify
from bills.choices import currency_types
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from PIL import Image

User = settings.AUTH_USER_MODEL

class Campaign(models.Model, HitCountMixin):
    name = models.CharField(max_length=100, unique = True)
    slug = models.SlugField()
    image = models.ImageField(default='no-person.png', upload_to='pages_pic')
    user = models.OneToOneField(User, related_name= "page_user" ,on_delete=models.CASCADE)
    goal_amount = models.FloatField(default = 0) 
    current_amount = models.FloatField(
        default = 0)
    description = models.TextField()
    message = models.CharField(default='Thank you for your donation', max_length=50)
    donation_type = models.CharField( choices = donation_types, default='Support', max_length=20, verbose_name='Donation category')
    currency = models.CharField( choices = currency_types, default='NGN', max_length=50, verbose_name='Currency')
    public = models.BooleanField(default = True)
    created = models.DateTimeField(default = timezone.now )
    updated = models.DateField(auto_now=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    
    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(self.name)
            campaign = Campaign.objects.get( pk = self.pk )

            if not campaign.slug:
                campaign.slug = slugify(self.name)
            if campaign.image != self.image and campaign.image != 'no-person.png':
                campaign.image.delete(save=False)
        except Campaign.DoesNotExist:
            # Please Ignore
            pass
        
        super().save()

        img = Image.open(self.image.path)
        if img.height > 180 or img.width > 320:
            output_size = (320, 180)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.name} ~ { self.donation_type }'
    
    class Meta:
        ordering = ['-created']
        
    def get_absolute_url(self):
        return reverse('campaign_detail_view', args=[self.slug] )


class Donor(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donors')
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(default = timezone.now )