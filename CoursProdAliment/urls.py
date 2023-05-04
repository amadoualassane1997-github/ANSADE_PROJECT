from django.urls import path
from . import views

urlpatterns = [
    path('save',views.save,name='coursprodaliment-save'),
    path('view',views.view,name='coursprodaliment-view'),
    path('delete/<str:date>/',views.delete,name='coursprodaliment-delete'),
    path('update/<str:date>/',views.update,name='coursprodaliment-update'),
    path('import',views.import_excel,name='coursprodaliment-import'),
    path('export',views.export_excel,name='coursprodaliment-export'),
    path('tb',views.tableau_bord,name='coursprodaliment-tb'),

]