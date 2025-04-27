from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Pokemon, Cart, Order

class PokemonTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # 创建测试宝可梦
        self.pokemon = Pokemon.objects.create(
            name='Test Pokémon',
            type='fire',
            price=10.00,
            sprite='https://example.com/sprite.png',
            location_x=0,
            location_y=0,
            category='real'
        )

    def test_pokemon_list(self):
        response = self.client.get(reverse('pokemon_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Pokémon')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('add_to_cart', args=[self.pokemon.id]))
        self.assertEqual(response.status_code, 302)  # 重定向到列表页
        self.assertTrue(Cart.objects.filter(user=self.user, pokemon=self.pokemon).exists())

    def test_cart_view(self):
        self.client.login(username='testuser', password='testpass')
        Cart.objects.create(user=self.user, pokemon=self.pokemon)
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Pokémon')

    def test_checkout(self):
        self.client.login(username='testuser', password='testpass')
        Cart.objects.create(user=self.user, pokemon=self.pokemon)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # 重定向到列表页
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        self.assertFalse(Cart.objects.filter(user=self.user).exists())

class ErrorPageTest(TestCase):
    def test_404_page(self):
        response = self.client.get('/invalid/')
        self.assertEqual(response.status_code, 404)

class CommandTest(TestCase):
    def test_import_pokemon(self):
        from django.core.management import call_command
        call_command('import_pokemon')
        self.assertTrue(Pokemon.objects.count() >= 2000)