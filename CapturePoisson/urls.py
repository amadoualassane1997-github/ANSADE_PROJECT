from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='capp-save'),
    path('view',views.view,name='capp-view'),
    path('delete/<str:date>/',views.delete,name='capp-delete'),
    path('update/<str:date>/',views.update,name='capp-update'),
    path('import',views.import_excel,name='capp-import'),
    path('export',views.export_excel,name='capp-export'),

]