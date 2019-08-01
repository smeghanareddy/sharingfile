from pages import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    # Non-Session urls
    path('', views.index, name='login'),
    path('register/', views.signup, name='home'),
    path('my-app/logout/', views.logout_view, name='logout'),
    # Session urls
    path('document_list', views.document_list, name='document_list'),
    path('list_document', views.list_document, name='list_document'),
    path('upload/', views.upload, name='upload_document'),
    path('document/<int:pk>/', views.delete_document, name='delete_document'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
