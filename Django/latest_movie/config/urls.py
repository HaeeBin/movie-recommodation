from django.contrib import admin
from django.urls import path, include
from djan import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('movie_search/', views.search, name='search'),  # '/' 에 해당되는 path

    path('ranking/', views.ranking, name='ranking'),

    # / 링크가 오면 djan의 urls로
    path('',include('djan.urls')),
    
    path('common/', include('common.urls')),

]

