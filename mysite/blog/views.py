from django.shortcuts import render, get_object_or_404
# importando el modelo
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
# importamos search de postgres
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector
)
# esto se puede editando el archivo de migraciones
from django.contrib.postgres.search import TrigramSimilarity # importamos TrigramSimilarity para buscar posts similares
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
# uso de decoradores
from django.views.decorators.http import require_POST
from taggit.models import Tag # importamos el modelo Tag
from django.db.models import Count # importamos Count para contar los tags

# from django.http import Http404




class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    # nombre del contexto que se pasara a la plantilla
    # por defecto es object_list
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    # pasa las paginas al template como page=page_obj


# Create your views here.

# objeto request es requerido en todas las vistas
def post_list(request, tag_slug=None):
    # obteniendo una lista de posts
    post_list = Post.published.all()
    # objeto numero de posts por pagina
    tag = None
    # si se pasa un tag_slug se filtra por tag
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    # obteniendo el numero de la pagina el (,1) es por defecto
    page_number = request.GET.get('page', 1)
    try:
        # retornamos los posts de la pagina
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # si no es un numero entero retornamos la primera pagina
        posts = paginator.page(1)
    except EmptyPage:
        # si la pagina no existe retornamos la ultima
        # paginator.num_pages el numero de paginas es el mismo que la ultima pagina
        posts = paginator.page(paginator.num_pages)

    # renderizar la plantilla con los posts
    return render(
        request, 
        'blog/post/list.html', 
        {
            'posts': posts,
            'tag': tag
         }
    )

def post_detail(request, year, month, day, post):
    # retorna el post si cumple los parametros, publicado e id
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,  # solo mostramos posts publicados
        # obtenemos el objeto si este cumnple con lo siguiente 
        slug=post,  # slug es el nombre en minuscula con guiones intermedios
        # esto es posible por unique_for_date='publish' en el modelo
        publish__year=year,
        publish__month=month,
        publish__day=day  # fecha publicada en el post
    )

    # lista de comentarios activos para este post
    # acceedemos a los comentarios por post.comments ya que se relacionaron en el modelo
    comments = post.comments.filter(active=True)
    # inicializamos el formulario
    form = CommentForm()

    # lista de tags del post
    # flat=True para obtener una lista de valores en lugar de objetos
    post_tags_ids = post.tags.values_list('id', flat=True)
    # obtenemos los posts que contienen los mismos tags
    # excluimos el post actual
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    # contamos los tags en comun y ordenamos por tags y fecha de publicacion
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    # ubicacion del template y tambien mandamos el objeto post
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    # variable que enviaremos si es que se envio el formulario
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            # obtenemos la url absoluta del post
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you reading {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            # enviamos el email en la forma del objeto de la libreria de django
            send_mail(
                subject,
                message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True


    else:
        # renderizamos el formulario vacio
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )

# decorador para que solo se pueda acceder por POST
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    # variable que enviaremos si es que se envio el formulario
    comment = None
    # si se envio el formulario
    form = CommentForm(request.POST)
    if form.is_valid():
        # se crea un objeto de tipo comment pero no se guarda en la base de datos
        comment = form.save(commit=False)
        # asignamos el post al comentario
        comment.post = post
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'comment': comment,
            'form': form
        }
    )

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    # si se envio el formulario de busqueda y es valido se realiza la busqueda
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector(
                'title', weight='A' # titulo con peso A y cuerpo con peso B (1 y 0.4) respectivamente
            ) + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = (
                # anotamos el campo search con el vector de busqueda
                Post.published.annotate(
                    similarity = TrigramSimilarity('title', query) # calculamos la similitud con el titulo
                )
                .filter(similarity__gt=0.1) # filtramos los resultados con una similitud mayor a 0.1
                .order_by('-similarity') # ordenamos por rank de mayor a menor
            )
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )