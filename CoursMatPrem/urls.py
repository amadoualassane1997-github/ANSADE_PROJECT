from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='coursmatprem-save'),
    path('view',views.view,name='coursmatprem-view'),
    path('delete/<str:date>/',views.delete,name='coursmatprem-delete'),
    path('update/<str:date>/',views.update,name='coursmatprem-update'),
    path('import',views.import_excel,name='coursmatprem-import'),
    path('export',views.export_excel,name='coursmatprem-export'),
    path('export',views.export_excel,name='coursmatprem-export'),
    path('tb',views.tableau_bord,name='coursmatprem-tb')

]