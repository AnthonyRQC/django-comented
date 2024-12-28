# una vez creado las urls de esta app se agrega este archivo a urls del proyecto
from django.urls import path
from . import views

# organizamos las usls por aplicaciones
app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    # todos los valores capturados en <> son string entonces los cambiamos
    # otro ejemplo <slug:post> que se identico al modelo
    path('<int:id>', views.post_detail, name='post_detail'),   
]