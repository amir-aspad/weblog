from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.views import View

# import from blog app
from .models import Blog, Category, Comment
from .forms import CreateCommentForm


class AllPostView(View):
    template_name = 'blog/show_all.html'

    def setup(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.search = request.GET.get('q', None)
        self.category = request.GET.get('category', None)

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
            'search': self.search,
            'category': self.category,
            'result_count': paginate.count,
        }
        return render(request, self.template_name, data)
    

class DetailBlogView(View):
    form_class = CreateCommentForm

    def get(self, request, slug):
        form = self.form_class()
        blog = get_object_or_404(Blog, slug=slug, is_active=True)
        categories = Category.objects.all()
        comments = Comment.config.filter(blog=blog)

        context = {
            'blog':blog,
            'categories':categories,
            'comments':comments,
            'form':form,
            'can_like': blog.can_like(request)
        }
        return render(request, 'blog/detail.html', context=context)
    

class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, blog_slug):
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            blog = get_object_or_404(Blog, slug=blog_slug)
            
            Comment.objects.create(
                user = request.user,
                blog = blog,
                text = form.cleaned_data['text'],
            )
            messages.success(request, 'comment send successfully after check it will be show in the template')
        else:
            messages.error(request, 'something went wrong')
        return redirect(reverse('blog:detail', kwargs={'slug':blog_slug}))
    

class CreateCommentReplyView(LoginRequiredMixin, View):
    def post(self, request, blog_slug, comment_id):
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            blog = get_object_or_404(Blog, slug=blog_slug)
            comment = get_object_or_404(Comment, pk=comment_id)

            Comment.objects.craete(
                user=request.user,
                blog=blog,
                reply=comment,
                is_reply=True,
                text=form.cleaned_data['text']
            )
            messages.success(request, 'your comment create successfully. after admin check it will show')
        else:
            messages.error(request, 'something went happen')
        return redirect(reverse('blog:detail', kwargs={'slug':blog_slug}))

