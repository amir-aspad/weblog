from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View

# import from blog app
from .models import Blog, Category, Comment


class AllPostView(View):
    template_name = 'blog/show_all.html'

    def setup(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.search = request.GET.get('q')
        self.category = request.GET.get('category')

        return super().setup(request, *args, **kwargs)
    
    def get(self, request):
        blogs = Blog.config.all()
        
        if self.search:
            blogs = blogs.filter(
                Q(title__contains=self.search)|
                Q(text__contains=self.search)
            )

        if self.category:
            find_category_by_cat = Category.objects.filter(slug=self.category)
            blogs = blogs.filter(
                cates__in=find_category_by_cat
            )
        
        paginate = Paginator(blogs, per_page=6)
        blogs = paginate.get_page(self.page)
        
        data = {
            'blogs': blogs,
        }
        return render(request, self.template_name, data)
    

class DetailBlogView(View):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_active=True)
        categories = Category.objects.all()
        comments = Comment.config.filter(blog=blog)

        context = {
            'blog':blog,
            'categories':categories,
            'comments':comments
        }
        return render(request, 'blog/detail.html', context=context)