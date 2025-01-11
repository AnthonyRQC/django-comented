from django.contrib.sitemaps import Sitemap
from .models import Post

# Sitemap class for the Post model
# This class inherits from Sitemap, a class included in Django that allows you to create sitemaps for your models.
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish