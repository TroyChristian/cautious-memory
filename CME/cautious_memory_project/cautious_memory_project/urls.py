"""cautious_memory_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, reverse_lazy
import CMApp.urls #imports views
from django.contrib.auth import views as auth_views
import CMApp.views as views #! imports views again
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='CMApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='CMApp/logout.html'), name='logout'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='CMApp/change-password.html'), name='password'),
    path('password-changed/', views.PasswordsChangeDoneView.as_view(template_name="CMApp/password_change_done.html", success_url = reverse_lazy('IndexView')), name="password_change_done"),
    path('admin/', admin.site.urls),
    path('', include(CMApp.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
