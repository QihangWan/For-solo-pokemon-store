import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from naming.models import Pokemon, Order

class Command(BaseCommand):
    help = 'Generate random orders'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=1000, help='Number of orders to generate')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        users = User.objects.all()
        pokemons = Pokemon.objects.all()

        if not users or not pokemons:
            self.stdout.write(self.style.ERROR('Please create users and import Pokémon data first'))
            return

        for _ in range(count):
            user = random.choice(users)
            selected_pokemons = random.sample(list(pokemons), k=random.randint(1, 5))
            total_price = sum(pokemon.price for pokemon in selected_pokemons)
            order = Order.objects.create(user=user, total_price=total_price)
            order.pokemons.set(selected_pokemons)
            self.stdout.write(self.style.SUCCESS(f'Generated order: {order}'))