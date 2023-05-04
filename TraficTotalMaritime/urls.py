from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='trafictotalmaritime-save'),
    path('view',views.view,name='trafictotalmaritime-view'),
    path('delete/<str:date>/',views.delete,name='trafictotalmaritime-delete'),
    path('update/<str:date>/',views.update,name='trafictotalmaritime-update'),
    path('import',views.import_excel,name='trafictotalmaritime-import'),
    path('export',views.export_excel,name='trafictotalmaritime-export'),
    path('tb',views.tableau_bord,name='trafictotalmaritime-tb'),

]