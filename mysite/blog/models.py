from django.conf import settings
from django.db import models
from django.utils import timezone
# para crear get_absolute_url
from django.urls import reverse

# Create your models here.

# definiendo un nuevo manager que hereda de models.Manager
class PublishedManager(models.Manager):
    # sobreescribimos el metodo para cuando realizamos 
    # cualquier consulta queryset esta ya solo obtenga los valores PUBLISHED
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        ) 

class Post(models.Model):
    # similar a enum module
    # Uso Post.Status.values obtenemos valores
    # Post.Status.labels obtenemos los nombres
    class Status(models.TextChoices):
        # DF es el valor y Draft son labels readble
        # DRAFT es el nombre de la propiedad con el cual 
        # es conocido en el lenguaje python
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    # se guarda en str en la base de datos ayuda al SEO
    slug = models.SlugField(
        max_length=250,
        # unique_for_date se utiliza para evitar que un post con el mismo titulo
        # y fecha de publicacion sean iguales
        unique_for_date='publish'
        )

    author = models.ForeignKey(
        # tabla usuarios de la autenticacion de django
        settings.AUTH_USER_MODEL,
        # cuando se borre un usuario sus posts tambien lo hacen
        on_delete=models.CASCADE,
        # nos permite la relacion inversa acceder a los posts desde el usuario
        # user.blog_posts
        related_name='blog_posts'
    )

    body = models.TextField()
    # se guarda com DATETIME en SQL
    # timezon y su funcion son de lo importado de django
    publish = models.DateTimeField(default=timezone.now)
    # este campo se crea automaticamente cuando se crea el post
    created = models.DateTimeField(auto_now_add=True)
    # se usa augo_now para actualizar la fecha cuando se guarda un objeto
    updated = models.DateTimeField(auto_now=True)
    # creamos un nuevo campo si este post es un borrador df o publicado PB
    # por defecto DRAFT y que tiene dos opciones
    # crear la clase Status es una buena practica 
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT,
    )

    # NOTA: en Meta podemos definir un manager por defecto
    # por defecto esta objects manager
    # por buena practica recordamos que el manager obbjects esta disponible
    objects = models.Manager() # the default manager
    # creamos un ojeto de nuestra clase creada PublishedManager
    published = PublishedManager()  # our custom manager

    # meta es una clase dentro del modelo que tiene valores por defecto
    # los cuales actuan como propiedades extra del modelo
    class Meta:
        # se ordena los posts por fecha de publicacion en orden descendiente
        # se utiliza el - para que se ordenen en orden descendiente
        # este orden es por default si al hacer un query no se especifica
        ordering = ['-publish']
        # realizamos un index para mejorar la velocidad del ordenamiento
        indexes = [
            models.Index(fields=['-publish'])
        ]

    # nombre del objeto por titulo
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail', # obtenido de blog.urls.py
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        # relacion inversa para acceder a los comentarios de un post comment.post
        # si no se da un related_name se crea uno por defecto comment_set
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        # se crea un index para mejorar la velocidad de ordenamiento
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'