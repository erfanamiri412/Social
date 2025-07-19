from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateCreateForm, CommentCreateForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

# Create your views here.

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts':posts})
    
    def post(self, request):
        return render(request, 'home/index.html')
    
class PostDetailView(View):
    form_class = CommentCreateForm

    def get(self, request, post_id, post_slug):
        post =get_object_or_404(Post, pk = post_id, slug = post_slug)
        comments = post.pcomments.filter(is_replay = False)
        return render(request, 'home/detail.html', {'post':post, 'comments':comments, 'form':self.form_class()})
    
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully', 'success')
        else:
            messages.error(request, 'You cant delete this post', 'danger')
        return redirect('home:home')
    
class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if self.post_instance.user.id != request.user.id:
            messages.error(request, 'You can’t update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.post_instance)
        return render(request, 'home/update.html', {'form': form, 'post': self.post_instance})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.post_instance)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'You updated this post', 'success')  
            return redirect('home:post_details', new_post.id, new_post.slug)

        return render(request, 'home/update.html', {'form': form, 'post': self.post_instance})
        
class PostCreatedView(LoginRequiredMixin, View):
    form_class = PostUpdateCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form':form})
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'You created a new post', 'success')
            return redirect('home:post_details', new_post.id, new_post.slug)
        
class PostCommentView(View):
    form_class = CommentCreateForm

    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        form = self.form_class()
        comments = post.pcomments.filter(is_replay=False)
        return render(request, 'home/detail.html', {
            'post': post,
            'form': form,
            'comments': comments,
        })

    def post(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('home:post_details', post_id=post.id, post_slug=post.slug)
        comments = post.pcomments.filter(is_replay=False)
        return render(request, 'home/detail.html', {
            'post': post,
            'form': form,
            'comments': comments,
        })