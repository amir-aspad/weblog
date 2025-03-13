from django.shortcuts import render, get_object_or_404
from django.views import View

# import from blog app
from .models import Blog

class AllPostView(View):
    template_name = 'blog/show_all.html'
    
    def get(self, request):
        blogs = Blog.config.all()
        
        data = {
            'blogs':blogs
        }
        return render(request, self.template_name, data)
    

class DetailBlogView(View):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_active=True)
        return render(request, 'blog/detail.html', {'blog':blog})