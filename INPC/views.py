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
import calendar

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def save(request):
    if request.method=='POST':
        request.POST._mutable=True
        date=request.POST['date']
        m=list(date.split("-"))
        n=calendar.monthrange(int(m[0]),int(m[1]))[1]
        date=datetime.date(int(m[0]),int(m[1]),n)
        request.POST['date']=date
        if Inpc.objects.filter(date=date).exists():
            form=InpcForm(request.POST,instance=Inpc.objects.get(date=date))
        else:
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
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    inpc=Inpc.objects.get(date=date)
    inpc.delete()
    return redirect('inpc-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])   
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
@allowed_users(allowed_roles=['modifieur']) 
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
            m=list(str(l[0]).split("-"))
            n=calendar.monthrange(int(m[0]),int(m[1]))[1]
            date=datetime.date(int(m[0]),int(m[1]),n)
            l[0]=date
            obj = Inpc.objects.update_or_create(date=l[0],inpc_global=l[1],
    produits_alimentaires_et_boissons_non_alcolises=l[2],tabac_et_stupefiant=l[3],articles_habillement_et_chaussures=l[4],logement_eau_gaz_electricites_et_autre_combistible=l[5],meubles_articles_de_menages_et_entretient_courant_du_foyer=l[6],sante=l[7]
    ,transport=l[8],communication=l[9],loisir_et_culture=l[10],enseignement=l[11],restaurant_et_hotel=l[12],bien_et_service_diver=l[13])
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

        rows=Inpc.objects.filter(date__range=(d1,d2)).values_list('date','inpc_global','produits_alimentaires_et_boissons_non_alcolises','tabac_et_stupefiant','articles_habillement_et_chaussures',
    'logement_eau_gaz_electricites_et_autre_combistible','meubles_articles_de_menages_et_entretient_courant_du_foyer','sante','transport','communication','loisir_et_culture',
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
    





@login_required(login_url='login')
def tableau_bord(request):
    date,inpc_global,produits_alimentaires_et_boissons_non_alcolises,tabac_et_stupefiant,articles_habillement_et_chaussures,logement_eau_gaz_electricites_et_autre_combistible,meubles_articles_de_menages_et_entretient_courant_du_foyer,sante,transport,communication,loisir_et_culture,enseignement,restaurant_et_hotel,bien_et_service_diver=[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    rows=Inpc.objects.values_list('date','inpc_global','produits_alimentaires_et_boissons_non_alcolises','tabac_et_stupefiant','articles_habillement_et_chaussures',
    'logement_eau_gaz_electricites_et_autre_combistible','meubles_articles_de_menages_et_entretient_courant_du_foyer','sante','transport','communication','loisir_et_culture',
    'enseignement','restaurant_et_hotel','bien_et_service_diver')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    date.append(str(row[col_num]))
                elif col_num==1:
                    inpc_global.append(row[col_num])
                elif col_num==2:
                    produits_alimentaires_et_boissons_non_alcolises.append(row[col_num])
                elif col_num==3:
                    tabac_et_stupefiant.append(row[col_num])
                elif col_num==4:
                    articles_habillement_et_chaussures.append(row[col_num])
                elif col_num==5:
                    logement_eau_gaz_electricites_et_autre_combistible.append(row[col_num])
                elif col_num==6:
                    meubles_articles_de_menages_et_entretient_courant_du_foyer.append(row[col_num])
                elif col_num==7:
                    sante.append(row[col_num])
                elif col_num==8:
                    transport.append(row[col_num])
                elif col_num==9:
                    communication.append(row[col_num])
                elif col_num==10:
                    loisir_et_culture.append(row[col_num])
                elif col_num==11:
                    enseignement.append(row[col_num])
                elif col_num==12:
                    restaurant_et_hotel.append(row[col_num])
                else:
                    bien_et_service_diver.append(row[col_num])


      
    return render(request,'INPC/chartjs.html',{'date':date,'inpc_global':inpc_global,'produits_alimentaires_et_boissons_non_alcolises':produits_alimentaires_et_boissons_non_alcolises,'tabac_et_stupefiant':tabac_et_stupefiant,'articles_habillement_et_chaussures':articles_habillement_et_chaussures,'logement_eau_gaz_electricites_et_autre_combistible':logement_eau_gaz_electricites_et_autre_combistible,'meubles_articles_de_menages_et_entretient_courant_du_foyer':meubles_articles_de_menages_et_entretient_courant_du_foyer,'sante':sante,'transport':transport,'communication':communication,'loisir_et_culture':loisir_et_culture,'enseignement':enseignement,'restaurant_et_hotel':restaurant_et_hotel,'bien_et_service_diver':bien_et_service_diver})
