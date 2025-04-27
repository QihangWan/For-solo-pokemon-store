from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count
from django.http import Http404
from django.core.paginator import Paginator
from django.db import connections
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Pokemon, Order, Cart

# 宝可梦列表视图（带分页、分类和位置范围搜索）
def pokemon_list(request):
    # 获取分类参数
    category = request.GET.get('category', 'real')
    print(f"Category: {category}")
    pokemons = Pokemon.objects.filter(category=category).order_by('id')  # 添加 order_by('id') 排序
    print(f"Found {pokemons.count()} Pokémon for category {category}")
    print(f"Database path: {Pokemon.objects.db}")
    print(f"Database file: {connections['default'].settings_dict['NAME']}")

    # 获取搜索参数
    query = request.GET.get('q', '')
    type_filter = request.GET.get('type', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    lat_min = request.GET.get('lat_min', '')
    lat_max = request.GET.get('lat_max', '')
    lon_min = request.GET.get('lon_min', '')
    lon_max = request.GET.get('lon_max', '')

    # 应用搜索条件
    if query:
        pokemons = pokemons.filter(Q(name__icontains=query) | Q(type__icontains=query))
    if type_filter:
        pokemons = pokemons.filter(type=type_filter)
    if price_min and price_max:
        pokemons = pokemons.filter(price__range=(price_min, price_max))
    if lat_min and lat_max:
        pokemons = pokemons.filter(location_y__range=(lat_min, lat_max))
    if lon_min and lon_max:
        pokemons = pokemons.filter(location_x__range=(lon_min, lon_max))

    # 分页：每页100只宝可梦
    paginator = Paginator(pokemons, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    types = Pokemon.objects.values('type').distinct()
    return render(request, 'pokemon_list.html', {
        'page_obj': page_obj,
        'query': query,
        'type_filter': type_filter,
        'category': category,
        'types': types
    })

# 宝可梦详情视图
def pokemon_detail(request, pk):
    pokemon = get_object_or_404(Pokemon, pk=pk)
    related = Pokemon.objects.filter(type=pokemon.type).exclude(pk=pk)[:3]
    return render(request, 'pokemon_detail.html', {
        'pokemon': pokemon,
        'related': related
    })

# 订购宝可梦视图
@login_required
def order_pokemon(request, pk):
    pokemon = get_object_or_404(Pokemon, pk=pk)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=pokemon.price)
        order.pokemons.set([pokemon])
        return redirect('pokemon_list')
    return render(request, 'order_form.html', {'pokemon': pokemon})

# 添加宝可梦到购物车视图
@login_required
def add_to_cart(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    Cart.objects.get_or_create(user=request.user, pokemon=pokemon)
    return redirect('pokemon_list')

# 购物车视图
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.pokemon.price for item in cart_items)
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if item_id:
            Cart.objects.filter(user=request.user, id=item_id).delete()
            return redirect('cart_view')
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# 结账视图
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('pokemon_list')
    pokemons = [item.pokemon for item in cart_items]
    total_price = sum(pokemon.price for pokemon in pokemons)
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.pokemons.set(pokemons)
    cart_items.delete()
    return redirect('pokemon_list')

# 管理员仪表板视图
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    total_revenue = sum(order.total_price for order in orders)
    type_stats = Pokemon.objects.values('type').annotate(count=Count('order'))
    return render(request, 'admin_dashboard.html', {
        'orders': orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'type_stats': type_stats
    })

# 订单历史视图
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

# 订单详情视图
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

# 用户注册视图
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pokemon_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 404错误处理视图
def handler404(request, exception):
    return render(request, '404.html', status=404)

# 500错误处理视图
def handler500(request):
    return render(request, '500.html', status=500)