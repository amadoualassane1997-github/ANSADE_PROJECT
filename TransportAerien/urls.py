from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='transaerien-save'),
    path('view',views.view,name='transaerien-view'),
    path('delete/<str:date>/',views.delete,name='transaerien-delete'),
    path('update/<str:date>/',views.update,name='transaerien-update'),
    path('import',views.import_excel,name='transaerien-import'),
    path('export',views.export_excel,name='transaerien-export'),
]