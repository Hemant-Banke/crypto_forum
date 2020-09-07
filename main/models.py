from django.conf import settings
from django.db import models


# Requests
class requests(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=254)

    # Request
    request = models.TextField(max_length=1000)

    createdon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.request[:50]


# Platforms
class platforms(models.Model):
    name = models.CharField(max_length=300, unique=True)
    site_url = models.CharField(max_length=300)

    image_url = models.CharField(max_length=1000)

    PL_TYPES = (
        ('exchange', 'Exchange'),
        ('coin', 'Coin'),
        ('give_away', 'Give Away'),
    )
    platform_type = models.CharField(max_length=100, choices=PL_TYPES)

    api_name = models.CharField(max_length=300,
        help_text='Provide if the name in API used is different then name given above',
        blank=True)

    # Info
    rating = models.PositiveIntegerField(default=5)
    video_id = models.CharField(max_length=1000, blank=True)

    description = models.TextField(blank=True)

    createdon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# Reviews
class review(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=254)

    platform = models.ForeignKey("platforms", on_delete=models.CASCADE)

    # review
    review = models.TextField()
    image = models.ImageField(blank = True, upload_to='photos/%Y/%m/%d', max_length=1000)
    rating = models.PositiveIntegerField(default=5)

    is_comment = models.BooleanField(default = False)
    parent = models.IntegerField(default = 0)

    is_problem = models.BooleanField(default = False)
    Prob_TYPES = (
        (0, 'None'),
        (1, 'Scam'),
        (2, 'Problems with withdrawals'),
        (3, 'Problems with deposits'),
        (4, 'Problems with KYC'),
        (5, 'Problems with Trade'),
        (6, 'Problems with Coins/Tokens'),
        (7, 'Problems with Customer Service'),
        (8, 'Problems with wallets'),
        (9, 'Other Problems'),
    )
    problem_type = models.PositiveIntegerField(choices=Prob_TYPES, default=0)
    is_problem_resolved = models.BooleanField(default = False)

    createdon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.review[:50]



# Saved Addresses
class address(models.Model):
    name = models.CharField(max_length=300)

    coin = models.CharField(max_length=300)
    exchange = models.CharField(max_length=300)
    network_type = models.CharField(max_length=300)
    address = models.CharField(max_length=1000)

    createdon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' : ' + self.coin + ' - ' + self.exchange

