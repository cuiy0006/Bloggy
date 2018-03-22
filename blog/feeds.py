from django.contrib.syndication.views import Feed
from blog.models import Post

class AllPostsRssFeed(Feed):
    title = 'Yao Cui Blog'
    link = '/'
    description = 'Yao Cui Articles'

    def items(self):
        return Post.objects.all().order_by('-created_time')

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body