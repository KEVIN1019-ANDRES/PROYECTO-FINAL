

def test_proyecto(client):
    # Prueba la página principal
    response = client.get('/')
    assert response.status_code == 200
    assert b"VTR" in response.data

def test_pagina_vehiculos(client):
    response = client.get('/vehiculos')
    assert response.status_code == 200
    assert b"Nuestros Veh\xc3\xadculos" in response.data

def test_pagina_accesorios(client):
    response = client.get('/accesorios')
    assert response.status_code == 200
    assert b"Accesorios" in response.data

def test_pagina_servicios(client):
    response = client.get('/servicios')
    assert response.status_code == 200
    assert b"Servicios" in response.data

def test_funcionalidad_busqueda(client):
    response = client.get('/buscar?q=auto')
    assert response.status_code == 200
    assert b"Resultados de b\xc3\xbasqueda" in response.data

def test_carrito_compras(client):
    response = client.get('/carrito')
    assert response.status_code == 200
    assert b"Carrito" in response.data

def test_pagina_contacto(client):
    response = client.get('/contacto')
    assert response.status_code == 200
    assert b"Cont\xc3\xa1ctanos" in response.data
