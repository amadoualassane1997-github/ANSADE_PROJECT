from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='monnaiechange-save'),
    path('view',views.view,name='monnaiechange-view'),
    path('delete/<int:id>/',views.delete,name='monnaiechange-delete'),
    path('update/<int:id>/',views.update,name='monnaiechange-update'),
    path('import',views.import_excel,name='monnaiechange-import'),
    path('export',views.export_excel,name='monnaiechange-export'),

]