# una vez creado las urls de esta app se agrega este archivo a urls del proyecto
from django.urls import path
from . import views
from .feeds import LatestPostsFeed

# organizamos las usls por aplicaciones
app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    
    # agregando un listado de posts usando ListView de Django
    # esto simplifica la vista y permite usar el template_name y context_object_name que se encuentran en settings.py
    # esto es más eficiente y permite personalizar el template según sea necesario
    # path('', views.PostListView.as_view(), name='post_list'),

    # agregando un listado de posts por tag
    path(
        'tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'
    ),
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
    path('feed/', LatestPostsFeed(), name='post_feed'), # agregando el feed de la aplicacion   
    path('search/', views.post_search, name='post_search'), # agregando la busqueda de la aplicacion
]