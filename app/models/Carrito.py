from app.admin.models.producto import Producto
from app.admin.models.vehiculo import Vehiculo

class Carrito:
    def __init__(self):
        self.carrito = []




    def agregar_vehiculo(self, vehiculo_id, cantidad):
        vehiculo = Vehiculo.query.get(vehiculo_id)
        if vehiculo:
            item = {'vehiculo': vehiculo,'cantidad': cantidad}
            self.carrito.append(item)
        
        
        
    def agregar_producto(self, producto_id, vehiculo_id, cantidad):
        producto = Producto.query.get(producto_id)
        if producto:
            item = {'producto': producto, 'cantidad': cantidad}
            self.carrito.append(item)
            

    def calcular_total(self):
        total = 0
        for item in self.carrito:
            if item['tipo'] == 'producto':
                total += item['producto'].precioproducto * item['cantidad']
            elif item['tipo'] == 'vehículo':
                total += item['vehiculo'].preciovehiculo * item['cantidad']
        return total
    
    def tamañoD(self):   
        return len(self.carrito)

    def getItems(self):
        return self.carrito
    
    def vaciarcarrito(self):
        self.carrito = []
    