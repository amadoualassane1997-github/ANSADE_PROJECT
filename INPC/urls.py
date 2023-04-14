from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='inpc-save'),
    path('view',views.view,name='inpc-view'),
    path('delete/<str:date>/',views.delete,name='inpc-delete'),
    path('update/<str:date>/',views.update,name='inpc-update'),
    path('import',views.import_excel,name='inpc-import'),
    path('export',views.export_excel,name='inpc-export'),

]