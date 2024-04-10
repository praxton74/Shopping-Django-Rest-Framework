import pytest
from django.urls import reverse
from faker import Faker
from faker_commerce import Provider
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from orders.models import Category


@pytest.mark.django_db
class TestCategoryAPIView:

    @pytest.fixture
    def fake(self):
        fake = Faker()
        fake.add_provider(Provider)
        return fake

    @pytest.fixture
    def categories(self):
        return baker.make(Category, 15)

    def test_category_list_api(self, client, categories):
        url = reverse('category-list')
        response = client.get(url)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(categories) == 15 == Category.objects.count()
        for item1, item2 in zip(categories, response.data):
            assert item1.id == item2['id']
            assert item1.name == item2['name']

    def test_category_detail_api(self, client, fake, categories):
        random_category = fake.random.choice(categories)
        url = reverse('category-detail', (random_category.id,))
        response = client.get(url)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 4
        assert response.data['id'] == random_category.id
        assert response.data['name'] == random_category.name
