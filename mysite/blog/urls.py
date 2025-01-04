# una vez creado las urls de esta app se agrega este archivo a urls del proyecto
from django.urls import path
from . import views

# organizamos las usls por aplicaciones
app_name = 'blog'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    # agregando un listado de posts usando ListView de Django
    # esto simplifica la vista y permite usar el template_name y context_object_name que se encuentran en settings.py
    # esto es más eficiente y permite personalizar el template según sea necesario
    path('', views.PostListView.as_view(), name='post_list'),
    # editando los campos para que sean unicos y agregando SEO
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/', 
         views.post_detail, 
         name='post_detail'
    ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path(
        '<int:post_id>/comment/', views.post_comment, name='post_comment'
    ),   
]