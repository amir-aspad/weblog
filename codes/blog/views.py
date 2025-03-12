from django.shortcuts import render
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