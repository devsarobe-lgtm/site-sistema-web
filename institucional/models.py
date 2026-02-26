import os
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name='Nome da Tag')
    slug = models.SlugField(max_length=80, unique=True, verbose_name='Slug', blank=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title_page = models.CharField(max_length=255, verbose_name='Título da Página')
    description_page = models.TextField(verbose_name='Descrição da Página')
    title = models.CharField(max_length=255, verbose_name='Título')
    cover_image = models.ImageField(upload_to='blog_cover_images/', verbose_name='Imagem de Capa')
    summary_content = models.CharField(max_length=140, verbose_name='Resumo do Conteúdo')
    content = models.TextField(verbose_name='Conteúdo')

    tags = models.ManyToManyField(
        Tag,
        related_name='blog_posts',
        verbose_name='Tags',
        blank=True,
    )

    slug = models.SlugField(max_length=60, unique=True, verbose_name='URL Amigável')
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT, verbose_name='Criado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Editado em')
    is_active = models.BooleanField(default=True, verbose_name='Está ativo')

    class Meta:
        verbose_name = 'Postagem de Blog'
        verbose_name_plural = 'Postagens de Blog'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})

    def clean(self):
        super().clean()
        if self.cover_image and self.cover_image.size > 2 * 1024 * 1024:
            raise ValidationError({'cover_image': 'A imagem não pode ter mais que 2 MB.'})

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk:
            try:
                old = BlogPost.objects.get(pk=self.pk)
                if old.cover_image and self.cover_image and old.cover_image != self.cover_image:
                    old_path = old.cover_image.path
                    if os.path.isfile(old_path):
                        os.remove(old_path)
            except BlogPost.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.cover_image:
            image_path = self.cover_image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)
