from django.db import models
from django.contrib.auth.models import User

# naming/models.py
class Pokemon(models.Model):
    CATEGORY_CHOICES = [
        ('real', 'Real Pokémon'),
        ('virtual', 'Virtual Pokémon'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sprite = models.URLField(blank=True)
    location_x = models.FloatField()
    location_y = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='real')  # 新增字段

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.pokemon.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemons = models.ManyToManyField(Pokemon)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order by {self.user.username} on {self.order_date}"