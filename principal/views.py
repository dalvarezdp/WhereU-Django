#encoding:utf-8
from principal.models import Personal, Ruta, PersonasRuta, ImagenesRuta, Amigo, Notificacion
from principal.models import Comentario
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import re, datetime
from datetime import datetime
from forms import PersonalForm, UserForm, RutaForm, ComentarioForm, ImagenesRutaForm

from django.core.exceptions import ObjectDoesNotExist

def inicio(request):
    usuario=request.user
    personal=Personal.objects.get(usuario=usuario.id)
    rutas = Ruta.objects.all()
    personasruta = PersonasRuta.objects.all()
    if usuario.is_authenticated():
        return render_to_response('privado.html',{'usuario':usuario,'personal':personal,'datos':rutas,'personasruta':personasruta}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html',{'usuario':usuario,'datos':rutas}, context_instance=RequestContext(request))



def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario,password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def privado(request):
    usuario=request.user
    rutas = Ruta.objects.all()
    return render_to_response('privado.html',{'usuario':usuario,'datos':rutas}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


def registro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            u = formulario.save(commit=False)
            u.save()
            p = Personal.objects.create(
                foto = "default",
                usuario = u,
            )
            p.save()
            usuario = request.POST['username']
            clave = request.POST['password1']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
    return render_to_response('registro.html',{'formulario':formulario}, context_instance=RequestContext(request))


def nueva_ruta(request):
    usuarios=Personal.objects.all()
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
    if request.method=='POST':
        latitud = request.POST['latitud']
        longitud = request.POST['longitud']
        formulario=RutaForm(request.POST, request.FILES)
        if formulario.is_valid():
            f=formulario.save(commit=False)
            f.usuario=usuario
            f.latfinal=latitud
            f.longfinal=longitud
            f.save()
            pr = PersonasRuta.objects.create(
                ruta = f,
                usuario = usuario,
            )
            pr.save()
            lista=f.amigos.split(',')
            
            for dato in usuarios:
                for item in lista:
                    if dato.usuario.username == item:
                        pr = PersonasRuta.objects.create(
                            ruta = f,
                            usuario = dato.usuario,
                        )
                        pr.save()           
            return HttpResponseRedirect('/')
    else:
        formulario = RutaForm()
    return render_to_response('rutanueva.html',{'personal':personal,'formulario':formulario,'usuario':usuario}, context_instance=RequestContext(request))


def lista_eventos(request):
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
        notificaciones=Notificacion.objects.filter(amigo_id=personal.id)
    personasruta= PersonasRuta.objects.filter(usuario=usuario.id)
    eventos = Ruta.objects.all()
      
    if usuario.is_authenticated():
        return render_to_response('privado.html',{'notificaciones':notificaciones,'personal':personal,'usuario':usuario,'eventos':eventos,'personasruta':personasruta}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html',{'usuario':usuario,'eventos':eventos}, context_instance=RequestContext(request))
    

def localizar(request):
    usuario=request.user
    personal=Personal.objects.get(usuario=usuario)
    foto=personal.foto
    if request.method == 'POST':
        latitud = request.POST['latitud']
        longitud = request.POST['longitud']
        
        personal.fecha = datetime.now()
        personal.sexo = personal.sexo
        personal.telefono = personal.telefono
        personal.latitud = latitud
        personal.longitud = longitud
        personal.nacimiento = personal.nacimiento
        personal.profesion = personal.profesion
        personal.foto = foto
        personal.usuario = usuario
        
        personal.save()
        
        return HttpResponseRedirect('/')
    else:
        formulario = PersonalForm(instance=personal)
    return render_to_response('privado.html', {'formulario':formulario}, context_instance=RequestContext(request))


def detalle_evento(request, id_evento):
    usuario=request.user
    personasruta=PersonasRuta.objects.filter(ruta_id=id_evento)
    personal=Personal.objects.get(usuario=usuario)
    ruta = get_object_or_404(Ruta, pk=id_evento)
    comentarios = Comentario.objects.filter(evento=ruta)
    amigos=[]
    
    for dato in personasruta:
            amigos.append(Personal.objects.get(usuario=dato.usuario))
    
    if request.method=='POST':
        formulario=ComentarioForm(request.POST)
        if formulario.is_valid():
            f=formulario.save(commit=False)
            f.evento=ruta        
            f.usuario=usuario
            f.save() 
            return HttpResponseRedirect(reverse('detalle_evento',args=[id_evento]))
            #return HttpResponseRedirect('/')   
    else:
        formulario = ComentarioForm()
        return render_to_response('evento.html',{'comentarios':comentarios,'formulario':formulario,'personasruta':personasruta,'usuario':usuario,'ruta':ruta,'personal':personal, 'personas':amigos}, context_instance=RequestContext(request))



def borrar_comentario(request, id_comentario):
    comentario = Comentario.objects.get(pk=id_comentario)
    id_evento = comentario.evento_id
    comentario.delete()
    return HttpResponseRedirect(reverse('detalle_evento',args=[id_evento]))


def modificar_perfil(request, id_persona):
    usu=request.user
    usuario = User.objects.get(pk=usu.id)
    personal = Personal.objects.get(pk=id_persona)
    if request.method == 'POST':
        formulario = PersonalForm(request.POST, request.FILES, instance=personal)
        formulario2 = UserForm(request.POST, instance=usuario)
        if formulario.is_valid() and formulario2.is_valid():
            formulario.save()
            formulario2.save()
            return HttpResponseRedirect('/')
    else:
        formulario = PersonalForm(instance=personal)
        formulario2 = UserForm(instance=usuario)
    return render_to_response('modificar_perfil.html', {'usuario':usuario, 'personal':personal,'formulario':formulario,'formulario2':formulario2}, context_instance=RequestContext(request))


def quees(request):
    return render_to_response('quees.html', context_instance=RequestContext(request))



def conocenos(request):
    return render_to_response('conocenos.html', context_instance=RequestContext(request))


def imagen_evento(request, id_evento):
    usuario=request.user
    personasruta=PersonasRuta.objects.filter(ruta_id=id_evento)
    personal=Personal.objects.get(usuario=usuario)
    fotos = ImagenesRuta.objects.filter(evento_id=id_evento)
    ruta = get_object_or_404(Ruta, pk=id_evento)
    amigos=[]
    
    for dato in personasruta:
            amigos.append(Personal.objects.get(usuario=dato.usuario))
    
    if request.method=='POST':
        formulario=ImagenesRutaForm(request.POST,request.FILES) 
        if formulario.is_valid():
            f2=formulario.save(commit=False)
            f2.evento=ruta
            f2.save()
            #return HttpResponseRedirect('/')
            return HttpResponseRedirect(reverse('imagen_evento',args=[id_evento]))
        else:
            return HttpResponseRedirect(reverse('imagen_evento',args=[id_evento]))
    else:
        formulario = ImagenesRutaForm()
        return render_to_response('imagenevento.html',{'formulario':formulario,'personasruta':personasruta,'usuario':usuario,'ruta':ruta,'personal':personal, 'personas':amigos,'fotos':fotos}, context_instance=RequestContext(request))
    

def gente(request):
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
    personasruta= PersonasRuta.objects.filter(usuario=usuario.id)
    personas=Personal.objects.all()
    amigos=Amigo.objects.filter(usuario_id=usuario.id)
    var=1
    return render_to_response('gente.html',{'var':var,'amigos':amigos,'personal':personal,'usuario':usuario,'personasruta':personasruta,'personas':personas}, context_instance=RequestContext(request))


def agregar_amigo(request,id_persona):
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
    personasruta= PersonasRuta.objects.filter(usuario=usuario.id)
    personas=Personal.objects.all()
    amigo = Personal.objects.get(usuario_id=id_persona)
    amigos=Amigo.objects.filter(usuario_id=usuario.id)
    
    a = Amigo.objects.create(
            amigo=amigo,
            usuario = usuario,
    )
    a.save()
    
    b = Amigo.objects.create(
            amigo=personal,
            usuario = amigo.usuario,
    )
    b.save()
    eliminar_notificacion(request, id_persona)
    
    return render_to_response('amigos.html',{'amigos':amigos,'personas':personas,'personal':personal,'usuario':usuario,'personasruta':personasruta}, context_instance=RequestContext(request))


def eliminar_amigo(request,id_persona):
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
    personasruta= PersonasRuta.objects.filter(usuario=usuario.id)
    amigos=Amigo.objects.filter(usuario_id=usuario.id)
    
    amigo = Amigo.objects.get(usuario_id=usuario.id,amigo_id=id_persona)
    amigo.delete()
    
    personalamigo1=Personal.objects.get(id=id_persona) 
    personalamigo=Personal.objects.get(usuario_id=usuario.id)        
    amig = Amigo.objects.get(usuario_id=personalamigo1.usuario_id,amigo_id=personalamigo.id)
    amig.delete()        
    
    return render_to_response('amigos.html',{'amigos':amigos,'personal':personal,'usuario':usuario,'personasruta':personasruta}, context_instance=RequestContext(request))


def amigos(request):
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
    personasruta= PersonasRuta.objects.filter(usuario=usuario.id)
    personas=Personal.objects.all()
    amigos=Amigo.objects.filter(usuario_id=usuario.id)
    return render_to_response('amigos.html',{'amigos':amigos,'personal':personal,'usuario':usuario,'personasruta':personasruta,'personas':personas}, context_instance=RequestContext(request))


def agregar_notificacion(request,id_persona):
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
    personasruta= PersonasRuta.objects.filter(usuario=usuario.id)
    personas=Personal.objects.all()
    amigo = Personal.objects.get(id=id_persona)
    
    try:
        existe = Amigo.objects.get(usuario_id=usuario.id,amigo_id=id_persona)
    except ObjectDoesNotExist, e:
        try:
            existe2 = Notificacion.objects.get(usuario_id=usuario.id,amigo_id=id_persona)
        except ObjectDoesNotExist, e2:
            a = Notificacion.objects.create(
                    amigo=amigo,
                    usuario = usuario,
                    notificacion=1,
            )
            a.save()    
    
    return render_to_response('gente.html',{'personas':personas,'personal':personal,'usuario':usuario,'personasruta':personasruta}, context_instance=RequestContext(request))


def eliminar_notificacion(request,id_persona):
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
    personasruta= PersonasRuta.objects.filter(usuario=usuario.id)
    amigos=Notificacion.objects.filter(usuario_id=usuario.id)
    
    amigo = Notificacion.objects.get(usuario_id=id_persona,amigo_id=personal.id)
    amigo.delete()    
            
    return render_to_response('privado.html',{'amigos':amigos,'personal':personal,'usuario':usuario,'personasruta':personasruta}, context_instance=RequestContext(request))



def borrar_imagen(request, id_imagen):
    imagen = ImagenesRuta.objects.get(pk=id_imagen)
    id_imagen2 = imagen.evento_id
    imagen.delete()
    return HttpResponseRedirect(reverse('imagen_evento',args=[id_imagen2]))
