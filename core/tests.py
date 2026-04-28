from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import date

from .models import Category, Transaction


class FinanceModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.income_category = Category.objects.create(
            user=self.user,
            name='Зарплата',
            category_type='income'
        )
        self.expense_category = Category.objects.create(
            user=self.user,
            name='Продукты',
            category_type='expense'
        )

    def test_category_creation(self):
        self.assertEqual(self.income_category.name, 'Зарплата')
        self.assertEqual(self.income_category.category_type, 'income')
        self.assertEqual(str(self.income_category), 'Зарплата (Доход)')

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('500.00'),
            date=date.today(),
            description='Покупка продуктов'
        )
        self.assertEqual(transaction.amount, Decimal('500.00'))
        self.assertEqual(transaction.description, 'Покупка продуктов')

    def test_category_user_unique_together(self):
        # Попытка создать дубликат категории у одного пользователя
        with self.assertRaises(Exception):
            Category.objects.create(
                user=self.user,
                name='Зарплата',
                category_type='income'
            )


class FinanceViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.category = Category.objects.create(
            user=self.user,
            name='Тестовая',
            category_type='expense'
        )

    def test_index_view_authenticated(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_transaction_list_view(self):
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100.00'),
            date=date.today(),
            description='Тест'
        )
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '100.00')

    def test_transaction_create_post(self):
        response = self.client.post(reverse('transaction_create'), {
            'category': self.category.id,
            'amount': '250.00',
            'date': date.today().isoformat(),
            'description': 'Новая транзакция'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().amount, Decimal('250.00'))

    def test_balance_calculation(self):
        # Доход
        income_cat = Category.objects.create(user=self.user, name='Доход', category_type='income')
        Transaction.objects.create(user=self.user, category=income_cat, amount=1000, date=date.today())
        # Расход
        Transaction.objects.create(user=self.user, category=self.category, amount=300, date=date.today())

        response = self.client.get(reverse('index'))
        content = response.content.decode()
        # Проверяем, что баланс = 700
        self.assertIn('700.00', content)


