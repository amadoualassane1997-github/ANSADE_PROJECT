from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='ipi-save'),
    path('view',views.view,name='ipi-view'),
    path('delete/<str:trimestre>/',views.delete,name='ipi-delete'),
    path('update/<str:trimestre>/',views.update,name='ipi-update'),
    path('import',views.import_excel,name='ipi-import'),
    path('export',views.export_excel,name='ipi-export'),
    path('tb',views.tableau_bord,name='ipi-tb'),

]