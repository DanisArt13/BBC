from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):  # Или StackedInline в зависимости от предпочтений
    model = Comment
    extra = 0  # Количество дополнительных пустых полей для добавления новых комментариев

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'get_post_title', 'content', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')

    def get_post_title(self, obj):
        return obj.post.title  # Получаем заголовок поста через связь
    get_post_title.short_description = 'Post Title'  # Описание для колонки

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]  # Используем CommentInline здесь

admin.site.register(Post, PostAdmin)