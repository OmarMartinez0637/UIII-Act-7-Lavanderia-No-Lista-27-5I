from django.db import models

class ClienteLavanderia(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    direccion_recogida = models.CharField(max_length=255, blank=True)
    direccion_entrega = models.CharField(max_length=255, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    notas_cliente = models.TextField(blank=True, null=True)
    preferencias_lavado = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class EmpleadoLavanderia(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    turno = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    dni = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class ArticuloRopa(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    tipo_prenda = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    tamano = models.CharField(max_length=20)
    instrucciones_especiales = models.TextField(blank=True, null=True)
    costo_lavado_estandar = models.DecimalField(max_digits=7, decimal_places=2)
    estado_articulo = models.CharField(max_length=50)
    es_delicado = models.BooleanField(default=False)
    cliente = models.ForeignKey(ClienteLavanderia, on_delete=models.SET_NULL, null=True, related_name='articulos')

    def __str__(self):
        return f"{self.tipo_prenda} ({self.color})"

class PedidoLavanderia(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(ClienteLavanderia, on_delete=models.CASCADE, related_name='pedidos')
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    fecha_entrega_estimada = models.DateField(null=True, blank=True)
    fecha_entrega_real = models.DateTimeField(null=True, blank=True)
    estado_pedido = models.CharField(max_length=50)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=50, blank=True)
    empleado_recepcion = models.ForeignKey(EmpleadoLavanderia, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_recepcion')
    comentarios_cliente = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id_pedido}"

class DetallePedidoLavanderia(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(PedidoLavanderia, on_delete=models.CASCADE, related_name='detalles')
    articulo = models.ForeignKey(ArticuloRopa, on_delete=models.SET_NULL, null=True, blank=True, related_name='detalles')
    cantidad = models.IntegerField(default=1)
    tipo_servicio = models.CharField(max_length=50)
    costo_servicio_individual = models.DecimalField(max_digits=7, decimal_places=2)
    subtotal_item = models.DecimalField(max_digits=10, decimal_places=2)
    manchas_detectadas = models.TextField(blank=True, null=True)
    instrucciones_item = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Detalle #{self.id_detalle} Pedido {self.pedido.id_pedido}"

class MaquinaLavanderia(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    tipo_maquina = models.CharField(max_length=50)
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    capacidad_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    estado_operativo = models.CharField(max_length=50)
    ultima_revision = models.DateField(null=True, blank=True)
    num_serie = models.CharField(max_length=50, blank=True)
    es_lavadora = models.BooleanField(default=False)
    es_secadora = models.BooleanField(default=False)
    # Nuevo campo: Relación con EmpleadoLavanderia
    id_empleado = models.ForeignKey(
        EmpleadoLavanderia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Empleado que hizo el reporte"
    )

    def __str__(self):
        return f"{self.tipo_maquina} {self.marca} {self.modelo}"

class ReporteOperacional(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha_reporte = models.DateField(auto_now_add=True)
    empleado = models.ForeignKey(
        EmpleadoLavanderia,
        on_delete=models.CASCADE,  # obligatorio, si se borra el empleado se borran sus reportes
        related_name='reportes',
        default=2  # Cambiado a un ID de empleado válido
    )
    num_pedidos_procesados = models.IntegerField(default=0)
    kg_ropa_procesada = models.IntegerField(default=0)
    tiempo_inactividad_maquinas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones_turno = models.TextField(blank=True, null=True)
    consumo_agua_litros = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.empleado.nombre} {self.empleado.apellido} ({self.fecha_reporte})"
