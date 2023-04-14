from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='comext-save'),
    path('view',views.view,name='comext-view'),
    path('delete/<str:trimestre>/',views.delete,name='comext-delete'),
    path('update/<str:trimestre>/',views.update,name='comext-update'),
    path('import',views.import_excel,name='comext-import'),
    path('export',views.export_excel,name='comext-export'),

]