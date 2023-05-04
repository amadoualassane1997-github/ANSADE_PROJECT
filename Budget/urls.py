from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='budget-save'),
    path('view',views.view,name='budget-view'),
    path('delete/<str:date>/',views.delete,name='budget-delete'),
    path('update/<str:date>/',views.update,name='budget-update'),
    path('import',views.import_excel,name='budget-import'),
    path('export',views.export_excel,name='budget-export'),
    path('tb',views.tableau_bord,name='budget-tb'),

]