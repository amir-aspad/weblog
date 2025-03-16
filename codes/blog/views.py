from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import View

# import from blog app
from .models import Blog


class AllPostView(View):
    template_name = 'blog/show_all.html'
    
    def get(self, request):
        page = request.GET.get('page', 1)

        blogs = Blog.config.all()
        paginate = Paginator(blogs, per_page=6)
        blogs = paginate.get_page(page)
        
        data = {
            'blogs': blogs,
        }
        return render(request, self.template_name, data)
    

class DetailBlogView(View):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_active=True)
        return render(request, 'blog/detail.html', {'blog':blog})