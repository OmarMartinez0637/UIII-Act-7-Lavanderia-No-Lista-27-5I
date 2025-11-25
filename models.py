from django.db import models

class ClienteLavanderia(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    direccion_recogida = models.CharField(max_length=255)
    direccion_entrega = models.CharField(max_length=255)
    fecha_registro = models.DateField()
    notas_cliente = models.TextField()
    preferencias_lavado = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class ArticuloRopa(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    tipo_prenda = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    tamano = models.CharField(max_length=20)
    instrucciones_especiales = models.TextField()
    costo_lavado_estandar = models.DecimalField(max_digits=5, decimal_places=2)
    estado_articulo = models.CharField(max_length=50)
    es_delicado = models.BooleanField()
    id_cliente = models.ForeignKey(ClienteLavanderia, on_delete=models.CASCADE, related_name="articulos")

    def __str__(self):
        return f"{self.tipo_prenda} ({self.color})"


class EmpleadoLavanderia(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    turno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class PedidoLavanderia(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(ClienteLavanderia, on_delete=models.CASCADE, related_name="pedidos")
    fecha_recepcion = models.DateTimeField()
    fecha_entrega_estimada = models.DateField()
    fecha_entrega_real = models.DateTimeField(null=True, blank=True)
    estado_pedido = models.CharField(max_length=50)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    id_empleado_recepcion = models.ForeignKey(EmpleadoLavanderia, on_delete=models.SET_NULL, null=True, related_name="pedidos_recepcionados")
    comentarios_cliente = models.TextField()

    def __str__(self):
        return f"Pedido #{self.id_pedido}"


class DetallePedidoLavanderia(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(PedidoLavanderia, on_delete=models.CASCADE, related_name="detalles")
    id_articulo = models.ForeignKey(ArticuloRopa, on_delete=models.CASCADE, related_name="detalles")
    cantidad = models.IntegerField()
    tipo_servicio = models.CharField(max_length=50)
    costo_servicio_individual = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal_item = models.DecimalField(max_digits=10, decimal_places=2)
    manchas_detectadas = models.TextField()
    instrucciones_item = models.TextField()

    def __str__(self):
        return f"Detalle #{self.id_detalle}"


class MaquinaLavanderia(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    tipo_maquina = models.CharField(max_length=50)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    capacidad_kg = models.DecimalField(max_digits=5, decimal_places=2)
    estado_operativo = models.CharField(max_length=50)
    ultima_revision = models.DateField()
    num_serie = models.CharField(max_length=50)
    es_lavadora = models.BooleanField()
    es_secadora = models.BooleanField()

    def __str__(self):
        return f"{self.tipo_maquina} ({self.marca})"


class ReporteOperacional(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha_reporte = models.DateField()
    id_empleado = models.ForeignKey(EmpleadoLavanderia, on_delete=models.CASCADE, related_name="reportes")
    num_pedidos_procesados = models.IntegerField()
    kg_ropa_procesada = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_inactividad_maquinas = models.IntegerField()
    observaciones_turno = models.TextField()
    consumo_agua_litros = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.fecha_reporte}"
