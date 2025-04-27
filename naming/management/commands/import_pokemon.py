import requests
import random
from django.core.management.base import BaseCommand
from naming.models import Pokemon
from faker import Faker

class Command(BaseCommand):
    help = 'Import Pokémon data from PokéAPI and generate virtual Pokémon'

    def handle(self, *args, **kwargs):
        # Step 1: Import real Pokémon from PokéAPI
        Pokemon.objects.all().delete()
        self.stdout.write(self.style.WARNING('Deleted all existing Pokémon data.'))
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=898')
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch data from PokéAPI'))
            return

        pokemons = response.json()['results']
        real_count = 0
        for pokemon in pokemons:
            try:
                details = requests.get(pokemon['url']).json()
                name = details['name']
                types = [t['type']['name'] for t in details['types']]
                sprite = details['sprites']['front_default']
                price = round(random.uniform(5.00, 50.00), 2)
                location_x = random.uniform(-180, 180)
                location_y = random.uniform(-90, 90)
                Pokemon.objects.create(
                    name=name,
                    type=types[0],
                    price=price,
                    sprite=sprite,
                    location_x=location_x,
                    location_y=location_y,
                    category='real'
                )
                real_count += 1
                if real_count % 100 == 0:
                    self.stdout.write(self.style.SUCCESS(f'Imported {real_count} Real Pokémon'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error importing Pokémon {name}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'Finished importing {real_count} Real Pokémon'))

        # Step 2: Generate virtual Pokémon with Faker
        fake = Faker()
        used_names = set()
        virtual_count = 0
        for i in range(6102):
            try:
                while True:
                    base_name = fake.first_name()
                    name = f"{base_name}_{i}"
                    if name not in used_names:
                        used_names.add(name)
                        break

                types = ['fire', 'water', 'grass', 'electric', 'psychic', 'normal']
                price = round(random.uniform(5.00, 50.00), 2)
                location_x = random.uniform(-180, 180)
                location_y = random.uniform(-90, 90)
                Pokemon.objects.create(
                    name=name,
                    type=random.choice(types),
                    price=price,
                    sprite='',
                    location_x=location_x,
                    location_y=location_y,
                    category='virtual'
                )
                virtual_count += 1
                if virtual_count % 100 == 0:
                    self.stdout.write(self.style.SUCCESS(f'Generated {virtual_count} Virtual Pokémon'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error generating virtual Pokémon {name}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'Finished generating {virtual_count} Virtual Pokémon'))

        # Step 3: Confirm final data counts
        total_count = Pokemon.objects.count()
        real_count = Pokemon.objects.filter(category='real').count()
        virtual_count = Pokemon.objects.filter(category='virtual').count()
        self.stdout.write(self.style.SUCCESS(f'Total Pokémon: {total_count}'))
        self.stdout.write(self.style.SUCCESS(f'Real Pokémon: {real_count}'))
        self.stdout.write(self.style.SUCCESS(f'Virtual Pokémon: {virtual_count}'))