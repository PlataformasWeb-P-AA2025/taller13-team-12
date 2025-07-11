from django.db import models

# Create your models here.
class Edificio(models.Model):
	
    Tipo_Opciones = [
        ('Residencial', 'residencial'),
        ('Comercial', 'comercial'),
    ]

    nombre = models.CharField(max_length=70)
    direccion = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=30)
    tipo = models.CharField(max_length=20, choices=Tipo_Opciones)

    def __str__(self):
        return "%s %s %s %s" % (self.nombre,
                self.direccion,
                self.ciudad,
                self.tipo)

class Departamento(models.Model):
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    num_cuartos = models.IntegerField()
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE,
            related_name="departamentos")

    def __str__(self):
        return "Propietario: (%s %s),Costo: %.2f,Cuartos: %d" % (self.nombres, self.apellidos, self.costo, self.num_cuartos)


