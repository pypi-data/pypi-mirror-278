from django.urls import path
from . import views


app_name = 'postds'


urlpatterns = [
    path('portfolio_details/<int:id>', views.portfolio_details, name='portfolio_details'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog_details/<slug>', views.BlogDetailView.as_view(), name='blog_details'),
    path('blog_category/<str:category_filter>', views.BlogCategoryListView.as_view(), name='blog_category'),
    path('blog_search_word/', views.BlogSearchWordListView.as_view(), name='blog_search_word'),
    path('blog_tag/<str:tag>', views.BlogTagListView.as_view(), name='blog_tag'),
]
