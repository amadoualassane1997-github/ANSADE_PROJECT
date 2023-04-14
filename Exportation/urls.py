from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='exp-save'),
    path('view',views.view,name='exp-view'),
    path('delete/<str:trimestre>/',views.delete,name='exp-delete'),
    path('update/<str:trimestre>/',views.update,name='exp-update'),
    path('import',views.import_excel,name='exp-import'),
    path('export',views.export_excel,name='exp-export'),

]