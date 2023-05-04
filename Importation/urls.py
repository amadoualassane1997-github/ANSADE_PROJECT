from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='imp-save'),
    path('view',views.view,name='imp-view'),
    path('delete/<str:trimestre>/',views.delete,name='imp-delete'),
    path('update/<str:trimestre>/',views.update,name='imp-update'),
    path('import',views.import_excel,name='imp-import'),
    path('export',views.export_excel,name='imp-export'),
    path('tb',views.tableau_bord,name='imp-tb'),

]