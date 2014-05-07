from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'whereu.views.home', name='home'),
    # url(r'^whereu/', include('whereu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'principal.views.lista_eventos'),
    url(r'^privado','principal.views.privado'),
    url(r'^gente','principal.views.gente'),
    url(r'^amigos','principal.views.amigos'),
    url(r'^registro', 'principal.views.registro'),
    url(r'^imagenevento/(?P<id_evento>\d+)$', 'principal.views.imagen_evento', name='imagen_evento'),
    url(r'^quees', 'principal.views.quees'),
    url(r'^conocenos', 'principal.views.conocenos'),
    url(r'^ingresar', 'principal.views.ingresar'),
    url(r'^ruta/nueva/$', 'principal.views.nueva_ruta'),
    url(r'^localizar','principal.views.localizar'),
    url(r'^evento/(?P<id_evento>\d+)$','principal.views.detalle_evento', name='detalle_evento'),
    url(r'^perfil/(?P<id_persona>\d+)$','principal.views.modificar_perfil'),
    url(r'^borrar/comentario/(?P<id_comentario>\d+)$','principal.views.borrar_comentario'),
    url(r'^borrar/imagen/(?P<id_imagen>\d+)$','principal.views.borrar_imagen'),
    url(r'^agregaramigo/(?P<id_persona>\d+)$','principal.views.agregar_amigo'),
    url(r'^agregarnotificacion/(?P<id_persona>\d+)$','principal.views.agregar_notificacion'),
    url(r'^eliminaramigo/(?P<id_persona>\d+)$','principal.views.eliminar_amigo'),
    url(r'^eliminarnotificacion/(?P<id_persona>\d+)$','principal.views.eliminar_notificacion'),
    url(r'^cerrar','principal.views.cerrar'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
)
