"""ASNADE_PROJECT URL Configuration

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
from django.urls import include, re_path,path
from authentification import views



urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('',views.loginPage,name='login'),
    re_path(r'^blog/', include('blog.urls')),
    re_path(r'^monnaiechange/', include('MonnaieChange.urls')),
    re_path(r'^CoursMatPrem/', include('CoursMatPrem.urls')),
    re_path(r'^CoursProdAliment/', include('CoursProdAliment.urls')),
    re_path(r'^Budget/', include('Budget.urls')),
    re_path(r'^authentification/', include('authentification.urls')),
    re_path(r'^InflationMondiale/', include('InflationMondiale.urls')),
    re_path(r'^INPC/', include('INPC.urls')),
    re_path(r'^TraficTotalMaritime/', include('TraficTotalMaritime.urls')),
    re_path(r'^SaisieElectricite/', include('SaisieElectricite.urls')),
    re_path(r'^TransportAerien/', include('TransportAerien.urls')),
    re_path(r'^ConsomationCarbone/', include('ConsomationCarbone.urls')),
    re_path(r'^CapturePoisson/', include('CapturePoisson.urls')),
    re_path(r'^EauElectricite/', include('EauElectricite.urls')),
    re_path(r'ICC/', include('ICC.urls')),
    re_path(r'CroissanceMondiale/', include('CroissanceMondiale.urls')),
    re_path(r'ProductionCuivreOr/', include('ProductionCuivreOr.urls')),
    re_path(r'Importation/', include('Importation.urls')),
    re_path(r'Exportation/', include('Exportation.urls')),
    re_path(r'CommerceExterieur/', include('CommerceExterieur.urls')),
    re_path(r'IPI/', include('IPI.urls')),
    

]
