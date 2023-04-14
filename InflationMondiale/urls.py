from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='inflamdle-save'),
    path('view',views.view,name='inflamdle-view'),
    path('delete/<str:date>/',views.delete,name='inflamdle-delete'),
    path('update/<str:date>/',views.update,name='inflamdle-update'),
    path('import',views.import_excel,name='inflamdle-import'),
    path('export',views.export_excel,name='inflamdle-export'),

]