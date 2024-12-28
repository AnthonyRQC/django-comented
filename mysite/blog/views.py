from django.shortcuts import render, get_object_or_404
# importando el modelo
from .models import Post
# from django.http import Http404

# Create your views here.

# objeto ruquest es requerido en todas las vistas
def post_list(request):
    # obtener los ultimos posts publicados
    # con el manager pulished creado en el modelo
    posts = Post.published.all()
    # renderizar la plantilla con los posts
    return render(
        request, 
        'blog/post/list.html', 
        {'posts': posts}
        )

def post_detail(request, id):
    # retorna el post si cumple los parametros, publicado e id
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED  # solo mostramos posts publicados
    )
    # ubicacion del template y tambien mandamos el obbjeto post
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
