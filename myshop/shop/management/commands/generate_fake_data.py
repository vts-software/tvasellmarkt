from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from shop.models import Category, Product, Review, Cart, Order, OrderItem
from faker import Faker
import random

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт тестовые фейковые данные для моделей магазина"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== Генерация тестовых данных ==="))

        # знСоздаём пользователей
        users = []
        for _ in range(5):
            username = fake.unique.user_name()
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password="test1234",
                phone=fake.phone_number()
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Создано {len(users)} пользователей"))

        # Создаём категории
        categories = []
        for _ in range(5):
            name = fake.word().capitalize()
            cat = Category.objects.create(name=name, slug=slugify(name))
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS(f"Создано {len(categories)} категорий"))

        # Создаём товары
        products = []
        for _ in range(20):
            category = random.choice(categories)
            name = fake.sentence(nb_words=3)
            product = Product.objects.create(
                category=category,
                name=name,
                slug=slugify(name)[:50],
                description=fake.text(200),
                price=round(random.uniform(10, 2000), 2),
                available=random.choice([True, False])
            )
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f"Создано {len(products)} товаров"))

        # Создаём отзывы
        for _ in range(20):
            Review.objects.create(
                product=random.choice(products),
                user=random.choice(users),
                rating=random.randint(1, 5),
                comment=fake.sentence()
            )
        self.stdout.write(self.style.SUCCESS("Созданы отзывы"))

        # Создаём заказы
        orders = []
        for _ in range(10):
            user = random.choice(users)
            order = Order.objects.create(
                user=user,
                status=random.choice(['new', 'paid', 'shipped', 'completed']),
                total_price=0
            )
            total = 0
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                price = product.price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total += price * quantity
            order.total_price = total
            order.save()
            orders.append(order)

        self.stdout.write(self.style.SUCCESS(f"Создано {len(orders)} заказов"))

        self.stdout.write(self.style.SUCCESS("=== Готово! ==="))