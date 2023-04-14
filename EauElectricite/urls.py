from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='eelec-save'),
    path('view',views.view,name='eelec-view'),
    path('delete/<str:date>/',views.delete,name='eelec-delete'),
    path('update/<str:date>/',views.update,name='eelec-update'),
    path('import',views.import_excel,name='eelec-import'),
    path('export',views.export_excel,name='eelec-export'),

]