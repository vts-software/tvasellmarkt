from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, Order, Review, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def product_list(request):
    """
    Главная страница: выводит список всех товаров.
    """
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, slug):
    """
    Детальная страница товара по его slug.
    """
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_detail(request, slug):
    """
    Страница категории по ее slug.
    """
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'shop/category_detail.html', {'category': category, 'products': products})


def cart_detail(request):
    """
    Корзина для гостей и авторизованных пользователей.
    Возвращает список элементов в одинаковом формате:
    [{'product': ..., 'quantity': ...}, ...]
    """
    items = []

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('product')
        for item in cart_items:
            items.append({
                'product': item.product,
                'quantity': item.quantity
            })
    else:
        session_cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=session_cart.keys())
        for product in products:
            quantity = session_cart[str(product.id)]
            items.append({
                'product': product,
                'quantity': quantity
            })

    total_quantity = sum(item['quantity'] for item in items)
    total_price = sum(item['product'].price * item['quantity'] for item in items)

    return render(request, 'shop/cart_detail.html', {
        'items': items,
        'total_quantity': total_quantity,
        'total_price': total_price
    })


def cart_add(request, product_id):
    """
    Добавление товара в корзину.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.add_product(product)
    else:
        session_cart = request.session.get('cart', {})
        session_cart[str(product_id)] = session_cart.get(str(product_id), 0) + 1
        request.session['cart'] = session_cart

    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    """
    Удаление товара из корзины.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.remove_product(product)
    else:
        session_cart = request.session.get('cart', {})
        if str(product_id) in session_cart:
            del session_cart[str(product_id)]
            request.session['cart'] = session_cart

    return redirect('shop:cart_detail')


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')

    if not items:
        return redirect('shop:cart_detail')  # Нельзя оформить пустую корзину

    total_price = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(user=request.user, total_price=total_price)

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart.items.all().delete()
    return redirect('shop:order_detail', order_id=order.id)


@login_required
def order_list(request):
    """
    Список заказов пользователя.
    """
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """
    Детальная страница заказа по его ID.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})


@login_required
def add_review(request, slug):
    """
    Добавление отзыва к товару.
    """
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating'))
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, "Пожалуйста, введите корректный рейтинг от 1 до 5.")
            return redirect('shop:add_review', slug=slug)
        
        comment = request.POST.get('comment', '')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        messages.success(request, "Ваш отзыв успешно добавлен!")
        return redirect('shop:product_detail', slug=slug)
    
    return render(request, 'shop/add_review.html', {'product': product})