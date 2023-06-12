class Carrito:
    def __init__(self, request):
        self.session = request.session
        

        # Obtener el carrito de la sesión o inicializarlo si no existe
        if "carrito" not in self.session:
            self.session["carrito"] = {}
        self.carrito = self.session["carrito"]

    def agregar(self, producto):
        id = str(producto.id_producto)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id": producto.id_producto,
                "nombre": producto.nombre_producto,
                "precio": producto.precio,
                "acumulado": producto.precio,
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += producto.precio
            self.carrito[id]["precio"] = producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id_producto)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.id_producto)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= producto.precio
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True