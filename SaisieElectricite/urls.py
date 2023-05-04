from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='saisieelec-save'),
    path('view',views.view,name='saisieelec-view'),
    path('delete/<str:date>/',views.delete,name='saisieelec-delete'),
    path('update/<str:date>/',views.update,name='saisieelec-update'),
    path('import',views.import_excel,name='saisieelec-import'),
    path('export',views.export_excel,name='saisieelec-export'),
    path('tb',views.tableau_bord,name='saisieelec-tb'),

]