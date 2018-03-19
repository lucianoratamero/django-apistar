from app import app

from unittest.mock import patch
from apistar.test import TestClient
from apistar.backends.django_orm import migrate, flush

from core import views, models

# we need to manually create the database, since we're using py.test directly
migrate()


def test_welcome():
    """
    Testing a view directly.
    """
    data = views.welcome()
    assert data == {'message': 'Welcome to API Star!'}


def test_http_request():
    """
    Testing a view, using the test client.
    """
    client = TestClient(app)
    response = client.get('http://localhost/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to API Star!'}


@patch('apistar.backends.django_orm.Session')
def test_criar_produto(mocked_session):
    """
    Testing a view that uses django_orm.Session, mocking, using the test client.
    """
    post_data = {'nota': 5, 'nome': 'chocolate', 'tamanho': 'grande'}
    mocked_session().Produto().nome = post_data['nome']
    mocked_session().Produto().nota = post_data['nota']
    mocked_session().Produto().tamanho = post_data['tamanho']

    client = TestClient(app)
    response = client.post('/criar-produto', data=post_data)

    mocked_session().Produto.assert_called_with(**post_data)
    mocked_session().Produto().save.assert_called_once_with()
    assert response.status_code == 201
    assert response.json() == post_data


def test_criar_produto_unmocked():
    """
    Testing a view that uses django_orm.Session, no mocks, using the test client.
    """
    post_data = {'nota': 5, 'nome': 'chocolate', 'tamanho': 'grande'}
    assert models.Produto.objects.count() == 0

    client = TestClient(app)
    response = client.post('/criar-produto', data=post_data)

    assert response.status_code == 201
    assert response.json() == post_data

    assert models.Produto.objects.count() == 1
    db_produto = models.Produto.objects.get()
    assert db_produto.nome == post_data['nome']
    assert db_produto.nota == post_data['nota']
    assert db_produto.tamanho == post_data['tamanho']
    flush()  # remember to clean the db after using it
