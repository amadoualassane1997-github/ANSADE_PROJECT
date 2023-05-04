from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='icc-save'),
    path('view',views.view,name='icc-view'),
    path('delete/<str:trimestre>/',views.delete,name='icc-delete'),
    path('update/<str:trimestre>/',views.update,name='icc-update'),
    path('import',views.import_excel,name='icc-import'),
    path('export',views.export_excel,name='icc-export'),
    path('tb',views.tableau_bord,name='icc-tb'),

]