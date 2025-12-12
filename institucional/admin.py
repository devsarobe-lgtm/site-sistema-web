from django.contrib import admin
from .models import Tag, BlogPost


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'tags')
    search_fields = (
        'title',
        'title_page',
        'description_page',
        'summary_content',
        'content',
    )
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ('SEO / Página', {
            'fields': ('title_page', 'description_page', 'slug')
        }),
        ('Conteúdo', {
            'fields': ('title', 'summary_content', 'content', 'tags')
        }),
        ('Imagens', {
            'fields': ('image', 'cover_image')
        }),
        ('Controle', {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at')
        }),
    )
