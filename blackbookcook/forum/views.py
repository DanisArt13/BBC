from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Rating
from .forms import PostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    
    def get_queryset(self):
        posts = Post.objects.all()
        print(f'Количество постов: {posts.count()}')  # Печатаем количество постов
        for post in posts:
            print(f'Пост: {post.title}, ID: {post.id}')  # Печатаем заголовок и ID каждого поста
        return posts
        
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()  # Добавляем форму комментария
        context['comments'] = self.object.comments.all()  # Получаем комментарии для поста
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')  # Путь, куда перейти после успешного создания

    def form_valid(self, form):
        form.instance.author = self.request.user  # Устанавливаем автора поста
        response = super().form_valid(form)  # Сначала создаем пост
        # Создаем рейтинг с нулевым значением для поста
        Rating.objects.create(post=self.object, user=self.request.user, score=0)
        return response

class CommentCreateView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)  # Получаем пост по ID
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Привязываем комментарий к посту
            comment.author = request.user  # Устанавливаем автора комментария
            comment.save()
            return redirect('forum:post_list', post_id=post.id)  # Перенаправляем на страницу списка постов
        else:
            return redirect(request.META.get('HTTP_REFERER'))
            
class PostRatingView(View):
    def post(self, request):

        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        
        rating, created = Rating.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={'score': 0}
        )
        if 'rate_up' in request.POST:
            if rating.score == 1:  # Если уже стоит лайк
                rating.delete()  # Удаляем оценку
                post.total_rating -= 1
                post.rating_count -= 1  # Уменьшаем количество рейтингов
            else:
                if rating.score == -1:  # Если была дизлайк
                    post.total_rating += 2  # Убираем -1, добавляем +1
                else:
                    post.total_rating += 1  # Просто добавляем 1
                    post.rating_count += 1  # Увеличиваем количество рейтингов

                rating.score = 1  # Устанавливаем лайк
                rating.save()

        elif 'rate_down' in request.POST:
            if rating.score == -1:  # Если уже стоит дизлайк
                rating.delete()  # Удаляем оценку
                post.total_rating += 1  # Увеличиваем общий рейтинг
                post.rating_count -= 1  # Уменьшаем количество рейтингов
            else:
                if rating.score == 1:  # Если была лайк
                    post.total_rating -= 2  # Убираем +1, добавляем -1
                else:
                    post.total_rating -= 1  # Уменьшаем общий рейтинг
                    post.rating_count += 1  # Увеличиваем количество рейтингов

                rating.score = -1  # Устанавливаем дизлайк
                rating.save()
        post.save()
        # Перенаправление на список постов
        return redirect('forum:post_list')