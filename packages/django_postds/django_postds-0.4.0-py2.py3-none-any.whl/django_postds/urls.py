from django.urls import path
from . import views


app_name = 'postds'


urlpatterns = [
    path('<int:id>/', views.portfolio_details, name='portfolio_details'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('<slug>/', views.BlogDetailView.as_view(), name='blog_details'),
]
