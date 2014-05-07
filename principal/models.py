#encoding:utf-8
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Personal(models.Model):
    fecha = models.DateTimeField(db_index=True, auto_now_add=True)
    sexo = models.CharField(max_length=100, blank="true", null="true")
    telefono = models.IntegerField(blank="true", null="true")
    latitud = models.CharField(max_length=100, blank="true", null="true")
    longitud = models.CharField(max_length=100, blank="true", null="true")
    nacimiento = models.CharField(max_length=100, blank="true", null="true")
    profesion = models.CharField(max_length=100, blank="true", null="true")
    foto = models.ImageField(upload_to='perfil',verbose_name='Imágen')
    usuario = models.ForeignKey(User)
    def __unicode__(self):
        return str(self.usuario)
    
class Ruta(models.Model):
    fecha = models.CharField(max_length=100)
    nombreRuta = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    fotoRuta = models.ImageField(upload_to='rutas',verbose_name='Imágen')
    latfinal = models.CharField(max_length=100)
    longfinal = models.CharField(max_length=100)
    amigos = models.CharField(max_length=500)
    usuario = models.ForeignKey(User)
    def __unicode__(self):
        return self.nombreRuta


class PersonasRuta(models.Model):
    usuario = models.ForeignKey(User)
    ruta = models.ForeignKey(Ruta)
    def __unicode__(self):
        return self.ruta


class Comentario(models.Model):
    fecha = models.DateTimeField(db_index=True, auto_now_add=True)
    evento = models.ForeignKey(Ruta)
    texto = models.TextField()
    usuario = models.ForeignKey(User)
    def __unicode__(self):
        return self.texto


class ImagenesRuta(models.Model):
    foto = models.ImageField(upload_to='fotos',verbose_name='Imágen')
    evento = models.ForeignKey(Ruta)
    def __unicode__(self):
        return self.ruta
    

class Amigo(models.Model):
    usuario=models.ForeignKey(User)
    amigo=models.ForeignKey(Personal)
    def __unicode__(self):
        return self.usuario
    
    
class Notificacion(models.Model):
    usuario=models.ForeignKey(User)
    amigo=models.ForeignKey(Personal)
    notificacion=models.IntegerField()
    def __unicode__(self):
        return self.usuario

    