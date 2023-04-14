from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='croismdle-save'),
    path('view',views.view,name='croismdle-view'),
    path('delete/<str:trimestre>/',views.delete,name='croismdle-delete'),
    path('update/<str:trimestre>/',views.update,name='croismdle-update'),
    path('import',views.import_excel,name='croismdle-import'),
    path('export',views.export_excel,name='croismdle-export'),

]