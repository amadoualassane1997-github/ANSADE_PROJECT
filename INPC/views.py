from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from INPC.forms import InpcForm
from INPC.models import Inpc

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def save(request):
    if request.method=='POST':
        form=InpcForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('inpc-view')
            except:
                pass
    else:
        form=InpcForm()
    return render(request,'INPC/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    inpcs=Inpc.objects.all()
    return render(request,'INPC/view.html',{'inpcs':inpcs})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete(request,date):
    inpc=Inpc.objects.get(date=date)
    inpc.delete()
    return redirect('inpc-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])   
def update(request,date):
    if request.method=='POST':
        form=InpcForm(request.POST,instance=Inpc.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('inpc-view')
            except:
                pass
   
    else:
        form=InpcForm(instance=Inpc.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'INPC/update.html',{'context':context})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) 
def import_excel(request):
    if request.method == 'POST' and request.FILES['myfile']:      
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)              
        mcexceldata = pd.read_excel(filename)        
        dbframe = mcexceldata
        fs.delete(myfile.name)
        dbframe.fillna(0,inplace=True)
        list_of_excel=[list(row) for row in dbframe.values]
        for l in list_of_excel:
            obj = Inpc.objects.create(date=l[0],inpc_global=l[1],
    prod_alim_et_boiss_non_alcool_fr=l[2],tabac_et_stupefiant=l[3],art_habmnt_et_chauss=l[4],log_eau_gaz_elec_et_autre_combtible=l[5],meub_art_menage_et_entre_courant_du_foyer=l[6],sante=l[7]
    ,transport=l[8],communication=l[9],loisir_et_culture=l[10],enseignement=l[11],restaurant_et_hotel=l[12],bien_et_service_diver=l[13])
            if obj !=None :
                obj.save()
        return redirect('inpc-view')   
    return render(request,'INPC/import.html')


@login_required(login_url='login')   
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="inpc.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('INPC')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
        
        columns=['Date','INPC Global','Produits alimentaires et boissons non alcoolisées','Tabacs et stupéfiants','Articles d\'habillement et chaussures',
    'Logement, eau,gaz, électricité et autres combustibles','Meubles,articles de ménages et entretien courant du foyer','Santé','Transports','Communication','Loisirs et culture','Enseignement',
    'Restaurants et Hôtels','Biens et services divers']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=Inpc.objects.filter(date__range=(d1,d2)).values_list('date','inpc_global','prod_alim_et_boiss_non_alcool_fr','tabac_et_stupefiant','art_habmnt_et_chauss',
    'log_eau_gaz_elec_et_autre_combtible','meub_art_menage_et_entre_courant_du_foyer','sante','transport','communication','loisir_et_culture',
    'enseignement','restaurant_et_hotel','bien_et_service_diver')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                if isinstance(row[col_num],datetime.date):
                    ws.write(row_num, col_num, row[col_num],style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    else:
        return render(request,'INPC/export.html')