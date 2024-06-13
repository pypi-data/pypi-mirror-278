from django.db import models
from mdeditor.fields import MDTextField
from _data import postds
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation


class PortfolioCategory(models.Model):
    filter = models.CharField('포트폴리오 카테고리', max_length=20)

    def __str__(self):
        return self.filter


class Portfolio(models.Model):
    title = models.CharField('제목', max_length=20)
    subtitle = models.CharField('부제목', max_length=40)
    filter = models.ForeignKey(PortfolioCategory, related_name='portfolio_category', on_delete=models.PROTECT)
    description = models.TextField('세부 설명', null=True, blank=True)
    image1 = models.ImageField(upload_to=f'images/portfolio/', null=True,
                               help_text="각 이미지 비율이(3x5) 동일한 것이 보기 좋습니다.")
    image2 = models.ImageField(upload_to=f'images/portfolio/', null=True, blank=True)
    image3 = models.ImageField(upload_to=f'images/portfolio/', null=True, blank=True)
    image4 = models.ImageField(upload_to=f'images/portfolio/', null=True, blank=True)
    image5 = models.ImageField(upload_to=f'images/portfolio/', null=True, blank=True)
    client = models.CharField('Client', max_length=20, blank=True)
    reg_time = models.DateTimeField(auto_now_add=True)
    url = models.URLField('참고링크', blank=True, null=True, help_text="공란 가능", max_length=500)

    def __str__(self):
        return self.title


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class BlogCategory(models.Model):
    filter = models.CharField('블로그 카테고리', max_length=20)

    def __str__(self):
        return self.filter


class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', default='default_thumbnail.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_author')
    content = MDTextField("Content {: .img-fluid} ")
    status = models.IntegerField(choices=STATUS, default=0)
    remarkable = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(BlogCategory, related_name='blog_category', on_delete=models.PROTECT)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(postds.context['template_name'] + ':blog_details', kwargs={"slug": str(self.slug)})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Delete profile when user is deleted
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'  # show how we want it to be displayed
