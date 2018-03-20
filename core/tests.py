
from django.test import TestCase
from apistar.test import TestClient
from model_mommy import mommy
from django_apistar.apps import App

from core import models, schemas


class TestCreateProduct(TestCase):

    def test_criar_produto_unmocked(self):
        """
        Testing a view that uses django_orm.Session, no mocks, using the test client.
        """
        client = TestClient(App)
        post_data = {'nota': 5, 'nome': 'chocolate', 'tamanho': 'grande'}
        assert models.Produto.objects.count() == 0

        response = client.post('/criar-produto/', data=post_data)

        assert response.status_code == 201
        assert response.json() == post_data

        assert models.Produto.objects.count() == 1
        db_produto = models.Produto.objects.get()
        assert db_produto.nome == post_data['nome']
        assert db_produto.nota == post_data['nota']
        assert db_produto.tamanho == post_data['tamanho']


class TestListProducts(TestCase):

    def test_listar_produtos(self):
        client = TestClient(App)
        produto = mommy.make(models.Produto, nota=5, tamanho='grande')

        response = client.get('/listar-produtos/')
        content = response.json()

        expected_produto = schemas.Produto(produto.__dict__)
        self.assertEqual(1, len(content))
        self.assertEqual(expected_produto, content[0])
