from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.views import View

# import from blog app
from .models import Blog, Category, Comment, Favorite, Like
from .forms import CreateCommentForm


class AllPostView(View):
    template_name = 'blog/show_all.html'
    
    def get(self, request):
        page = request.GET.get('page', 1)
        search = request.GET.get('q', None)
        category = request.GET.get('category', None)
        blogs = Blog.config.all()
        
        if search:
            blogs = blogs.filter(
                Q(title__contains=search)|
                Q(text__contains=search)
            )

        if category:
            find_category_by_cat = Category.objects.filter(slug=category)
            blogs = blogs.filter(
                cates__in=find_category_by_cat
            )
            category = find_category_by_cat[0].title if find_category_by_cat else None
        
        paginate = Paginator(blogs, per_page=6)
        blogs = paginate.get_page(page)
        
        data = {
            'blogs': blogs,
            'search': search,
            'category': category,
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
            'can_like': blog.can_like(request),
            'can_add_to_favorite': blog.can_add_to_favorite(request)
        }
        return render(request, 'blog/detail.html', context=context)
    

class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, blog_id):
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            blog = get_object_or_404(Blog, pk=blog_id)
            
            Comment.objects.create(
                user = request.user,
                blog = blog,
                text = form.cleaned_data['text'],
            )
            messages.success(request, 'comment send successfully after check it will be show in the template')
        else:
            messages.error(request, 'something went wrong')
        return redirect(reverse('blog:detail', kwargs={'slug':blog.slug}))
    

class CreateCommentReplyView(LoginRequiredMixin, View):
    def post(self, request, blog_id, comment_id):
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            blog = get_object_or_404(Blog, pk=blog_id)
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
        return redirect(reverse('blog:detail', kwargs={'slug':blog.slug}))


class WorkOnFavoriteView(LoginRequiredMixin, View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)

        fav, created = Favorite.objects.get_or_create(
            user=request.user, blog=blog
        )

        if not created:
            fav.delete()

        return redirect('blog:detail', slug=blog.slug)


class LikeView(LoginRequiredMixin, View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)

        like, created = Like.objects.get_or_create(
            blog=blog, user=request.user
        )
        
        if not created:
            like.delete()

        return redirect('blog:detail', slug=blog.slug)

