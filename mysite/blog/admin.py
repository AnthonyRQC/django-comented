from django.contrib import admin
# importando al pagina admin nuestro modle Post
from .models import Post

# Register your models here.

# registramos el modelo post en el admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # se define el contenido que se mostrara en la lista de admin
    # contenido en el view
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    # fitros en el costado derecho
    list_filter = ['status', 'created', 'publish', 'author']
    # buscador por titulo y body
    search_fields = ['title', 'body']
    # autocompletado en tiempo real
    prepopulated_fields = {'slug': ('title',)}
    # habilita una nueva ventana si hay muchos usuarios
    # como buscador y mas detalles
    raw_id_fields = ['author']
    # orden para mostra los posts por defecto
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    # mostrar los numeros en la barra derecha
    show_facets = admin.ShowFacets.ALWAYS