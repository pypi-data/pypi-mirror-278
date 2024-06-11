from django.shortcuts import render, get_object_or_404
from _data import postds

from django_postds.models import Portfolio, BlogPost
from django.views import generic
from hitcount.views import HitCountDetailView

num_pagination = 6

c = postds.context


def portfolio_details(request, id: int):
    c.update({
        "obj": get_object_or_404(Portfolio, pk=id),
        "breadcrumb": {
            "title": c['portfolio']['title'],
        },
    })
    return render(request, c["template_name"] + '/' + c['filenames']['portfolio_details'], c)


class BlogListView(generic.ListView):
    template_name = c["template_name"] + '/' + c['filenames']['blog']
    paginate_by = num_pagination

    # 홈페이지에서 다이렉트 링크로 연결하기 위해서 필요하다.
    def get_queryset(self):
        # https://stackoverflow.com/questions/56067365/how-to-filter-posts-by-tags-using-django-taggit-in-django
        return BlogPost.objects.filter(status=1).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(c)
        context.update({
            "breadcrumb": {
                "title": "Blog",
            },
        })
        return context


class BlogDetailView(HitCountDetailView):
    model = BlogPost
    template_name = c["template_name"] + '/' + postds.context['filenames']['blog_details']
    context_object_name = 'object'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(c)
        context.update(
            {
                'breadcrumb': {
                    'title': 'Blog Detail'
                },
            }
        )
        return context
