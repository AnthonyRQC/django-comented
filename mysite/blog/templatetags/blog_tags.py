from django import template
from ..models import Post
from django.db.models import Count
# importamos la libreria markdown para poder renderizar el contenido de los posts
import markdown
from django.utils.safestring import mark_safe

# registro de un tag personalizado
register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

# registro de un tag personalizado
# este tag puede ser utilizado en cualquier template para mostrar los ultimos posts
# no es necesario crear una vista y url con la llamada del tag y acepta un argumento
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

# registro de un filtro personalizado
# {% load blog_tags %} {% post.body|markdown %}
# se importa la libreria markdown y se renderiza el contenido del post
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))