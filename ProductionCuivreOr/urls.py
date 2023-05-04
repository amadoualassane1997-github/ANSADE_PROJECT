from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='prodcror-save'),
    path('view',views.view,name='prodcror-view'),
    path('delete/<str:trimestre>/',views.delete,name='prodcror-delete'),
    path('update/<str:trimestre>/',views.update,name='prodcror-update'),
    path('import',views.import_excel,name='prodcror-import'),
    path('export',views.export_excel,name='prodcror-export'),
    path('tb',views.tableau_bord,name='prodcror-tb'),

]