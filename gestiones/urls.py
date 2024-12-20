from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Usuarios
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('colaboradores/', views.lista_colaboradores, name='lista_colaboradores'),
    path('colaboradores/editar/<int:pk>/', views.editar_colaborador, name='editar_colaborador'),
    path('colaboradores/eliminar/<int:pk>/', views.eliminar_colaborador, name='eliminar_colaborador'),
    path('colaboradores/exportar_excel/', views.exportar_colaboradores_excel, name='exportar_colaboradores_excel'),
    path('colaboradores/ficha/<int:pk>/', views.ficha_usuario, name='ficha_usuario'),
    path('colaboradores/ficha/<int:pk>/pdf/', views.ficha_usuario_pdf, name='ficha_usuario_pdf'),
    #Cargas Familiares
    path('cargas/registrar/', views.registrar_carga, name='registrar_carga'),
    path('cargas/', views.listar_cargas, name='listar_cargas'),
    path('cargas/editar/<int:pk>/', views.editar_carga, name='editar_carga'),
    path('cargas/eliminar/<int:pk>/', views.eliminar_carga, name='eliminar_carga'),
    #Asistencia
    path('registro_asistencia/', views.registro_asistencia, name='registro_asistencia'),
    path('visualizacion_asistencia/', views.visualizacion_asistencia, name='visualizacion_asistencia'),
    path('exportar-asistencias/', views.exportar_asistencias_excel, name='exportar_asistencias_excel'),
    #Solicitudes
    path('crear_solicitud/', views.crear_solicitud, name='crear_solicitud'),
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('gestionar_solicitud/<int:pk>/', views.gestionar_solicitud, name='gestionar_solicitud'),
    path('solicitudes/<int:pk>/pdf/', views.descargar_comprobante, name='descargar_comprobante'),
    #Vacaciones
    path('vacaciones/crear/', views.crear_solicitud_vacaciones, name='crear_solicitud_vacaciones'),
    path('vacaciones/gestionar/<int:pk>/', views.gestionar_solicitud_vacaciones, name='gestionar_solicitud_vacaciones'),
    path('vacaciones/listar/', views.lista_solicitudes_vacaciones, name='lista_solicitudes_vacaciones'),
    #Cursos
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/crear/', views.crear_curso, name='crear_curso'),
    path('cursos/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('cursos/<int:curso_id>/editar_participantes/', views.editar_participantes, name='editar_participantes'),
    path('cursos/<int:curso_id>/actualizar_progreso/', views.actualizar_progreso, name='actualizar_progreso'),
    path('cursos/<int:curso_id>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    #Beneficios
    path('beneficios/', views.lista_beneficios, name='lista_beneficios'),
    path('beneficios/crear/', views.crear_beneficio, name='crear_beneficio'),
    path('beneficios/<int:id>/editar/', views.editar_beneficio, name='editar_beneficio'),
    path('beneficios/<int:id>/eliminar/', views.eliminar_beneficio, name='eliminar_beneficio'),
    #Denuncias
    path('denuncias/', views.lista_denuncias, name='lista_denuncias'),
    path('denuncias/crear/', views.crear_denuncia, name='crear_denuncia'),
    path('denuncias/<int:pk>/', views.detalle_denuncia, name='detalle_denuncia'),  # Agrega esta línea
    path('denuncia_creada/', views.denuncia_creada, name='denuncia_creada'),  # Nueva URL para la confirmación
    path('denuncias/gestionar/<int:pk>/', views.gestionar_denuncia, name='gestionar_denuncia'),
    #Publicaciones
    path('publicaciones/crear/', views.crear_publicacion, name='crear_publicacion'),
    #Documentos
    path('documentos/', views.lista_documentos_empresa, name='lista_documentos_empresa'),
    path('documentos/subir/', views.subir_documento_empresa, name='subir_documento_empresa'),
    path('documentos/descargar/<int:pk>/', views.descargar_documento_empresa, name='descargar_documento_empresa'),
    path('gestiones/documentos/descargar/<int:pk>/', views.descargar_documento_empresa, name='descargar_documento_empresa'),
    path('gestiones/documentos/<int:documento_id>/ver_descargas/', views.ver_descargas_documento, name='ver_descargas_documento'),
    path('documentos/eliminar/<int:documento_id>/', views.eliminar_documento_empresa, name='eliminar_documento_confirmacion'),

    path('contacto/', views.contacto, name='contacto'),
    path('success/', views.success, name='success'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/photo/', views.edit_profile_photo, name='edit_profile_photo'),
    path('profile/change_password/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('buscar/', views.buscar, name='buscar'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
