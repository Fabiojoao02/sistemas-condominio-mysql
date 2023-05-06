"""sistemacondominio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from condominio.views import index, listacondominio, listaconblomov, listaconblomorador, listaconta, listaleitura, GerarPDF, geradorPDFgeral
from emailer.views import sendemail
# from movimentacao.views import ListaCalculo
# from emailer.views import SendFormEmail

urlpatterns = [
    # path('', include('movimentacao.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='Login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Logout.html'), name='logout'),

    path('gerarPDF/<str:ma>/<int:id_morador>/',
         GerarPDF.as_view(), name='gerarPDF'),

    path('', index, name='index'),
    path('listacondominio/<int:id>/', listacondominio, name='listacondominio'),
    path('listaconblomov/<int:id>/',
         listaconblomov, name='listaconblomov'),
    path('listaconblomorador/<int:idb>/<str:ma>/',
         listaconblomorador, name='listaconblomorador'),
    path('geradorPDFgeral/<int:idb>/<str:ma>/',
         geradorPDFgeral, name='geradorPDFgeral'),
    path('listaconta/<int:idb>/<str:ma>/<int:id_morador>/',
         listaconta, name='listaconta'),
    path('listaleitura/<int:idb>/<str:ma>/<int:id_morador>/',
         listaleitura, name='listaleitura'),
    path('sendemail/',
         sendemail, name='sendemail'),
    path('sendemail/<int:idb>/<str:ma>/<int:id_morador>/',
         sendemail, name='sendemail'),


    path('admin/', admin.site.urls),

    # path('', TemplateView.as_view(template_name="home.html"), name='home'),
    # path('send-form-email/', SendFormEmail.as_view(), name='send_email'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.AdminSite.site_header = 'Sistemas de Condomínios'
admin.AdminSite.site_title = 'Condomínios'
admin.AdminSite.index_title = 'Condomínios'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
