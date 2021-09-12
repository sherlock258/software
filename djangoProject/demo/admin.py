from django.contrib import admin
from .models import User,Article,Like,Attention,Comment

@admin.register(User)
class DemoAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','phone','email','avatarurl')
    ordering = ('id',)
    list_display_links = ('id','username','password','phone','email','avatarurl')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('id','title','content','author','time','count','kind','html','status')
    ordering = ('id',)
    list_display_links = ('id','title','content','author','time','count','kind','html','status')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id','userid','articleid')
    ordering = ('id',)
    list_display_links = ('id','userid','articleid')

@admin.register(Attention)
class AttentionAdmin(admin.ModelAdmin):
    list_display = ('id','liking','liked')
    ordering = ('id',)
    list_display_links = ('id','liking','liked')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','userid','articleid','value','status','time')
    ordering = ('id',)
    list_display_links = ('id','userid','articleid','value','status','time')