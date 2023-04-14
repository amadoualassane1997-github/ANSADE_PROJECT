from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='consco2-save'),
    path('view',views.view,name='consco2-view'),
    path('delete/<str:date>/',views.delete,name='consco2-delete'),
    path('update/<str:date>/',views.update,name='consco2-update'),
    path('import',views.import_excel,name='consco2-import'),
    path('export',views.export_excel,name='consco2-export'),

]