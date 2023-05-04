from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from ICC.forms import IccForm
from ICC.models import Icc


# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def save(request):
    if request.method=='POST':
        trimestre=request.POST['trimestre']
        if Icc.objects.filter(trimestre=trimestre).exists():
            form=IccForm(request.POST,instance=Icc.objects.get(trimestre=trimestre))
        else:
            form=IccForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('icc-view')
            except:
                pass
    else:
        form=IccForm()
    return render(request,'ICC/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    iccs=Icc.objects.all()
    return render(request,'ICC/view.html',{'iccs':iccs})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,trimestre):
    icc=Icc.objects.get(trimestre=trimestre)
    icc.delete()
    return redirect('icc-view')


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,trimestre):
    if request.method=='POST':
        form=IccForm(request.POST,instance=Icc.objects.get(trimestre=trimestre))
        if form.is_valid():
            try:
                form.save()
                return redirect('icc-view')
            except:
                pass
   
    else:
        form=IccForm(instance=Icc.objects.get(trimestre=trimestre))
        form.fields['trimestre'].widget=forms.HiddenInput()
    context={
        'form':form,
        'trimestre':trimestre
    }
    return render(request,'ICC/update.html',{'context':context})


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
            Icc.objects.update_or_create(trimestre=l[0],icc_global=l[1],
    materiaux_de_construction=l[2],biens_et_service_de_gestion_du_chantier=l[3],location_de_materiels=l[4],main_oeuvre=l[5],materiaux_de_base=l[6],materiaux_pour_couverture=l[7]
    ,materiaux_de_menuiserie=l[8],materiaux_de_plomberie_et_sanitaire=l[9],materiaux_pour_travaux_electricite=l[10],revetement_des_murs_et_sols=l[11],peinture_vernis_chaux=l[12],materiaux_pour_etancheite=l[13])
        return redirect('icc-view')   
    return render(request,'ICC/import.html')


@login_required(login_url='login')     
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('trimestre1')
        d2=request.POST.get('trimestre2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="icc.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('ICC')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        columns=['Trimestre','ICC global','Matériaux de construction',' Biens et service de gestion du chantier','Location de matériels',
    ' Main d\'œuvre','Matériaux de base','Matériaux pour couverture','Matériaux de menuiserie','Matériaux de plomberie et sanitaire','Matériaux pour travaux d\'électricité','Revetement des murs et sols',
    'Peinture, vernis, chaux','Matériaux pour étanchèite']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=Icc.objects.values_list('trimestre','icc_global','materiaux_de_construction','biens_et_service_de_gestion_du_chantier',
    'location_de_materiels','main_oeuvre','materiaux_de_base','materiaux_pour_couverture','materiaux_de_menuiserie','materiaux_de_plomberie_et_sanitaire',
    'materiaux_pour_travaux_electricite','revetement_des_murs_et_sols','peinture_vernis_chaux','materiaux_pour_etancheite')
        l=[]
        for row in rows:
            for col_num in range(len(row)):
                col_0=row[0].split('-')
                d1_annee=d1.split('-')
                d2_annee=d2.split('-')
                if int(col_0[1])>=int(d1_annee[1]) and int(col_0[1])<=int(d2_annee[1]):
                    l.append(row)
        v=[]
        for e in l:
            s=e[0].split('-')
            y=s[1]
            n=list(s[0])[1]
            if (y==d1.split('-')[1] and int(n)<int(list(d1.split('-')[0])[1])) or (y==d2.split('-')[1] and int(n)>int(list(d2.split('-')[0])[1])):
                pass
            else:
                v.append(e)

        for row in v:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    
        wb.save(response)
        return response
    else:
        icc_col=Icc.objects.all().values('trimestre')
        return render(request,'ICC/export.html',{'icc_col':icc_col})



@login_required(login_url='login')
def tableau_bord(request):
    trimestre,icc_global,materiaux_de_construction,biens_et_service_de_gestion_du_chantier,location_de_materiels,main_oeuvre,materiaux_de_base,materiaux_pour_couverture,materiaux_de_menuiserie,materiaux_de_plomberie_et_sanitaire,materiaux_pour_travaux_electricite,revetement_des_murs_et_sols,peinture_vernis_chaux,materiaux_pour_etancheite=[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    rows=Icc.objects.values_list('trimestre','icc_global','materiaux_de_construction','biens_et_service_de_gestion_du_chantier',
    'location_de_materiels','main_oeuvre','materiaux_de_base','materiaux_pour_couverture','materiaux_de_menuiserie','materiaux_de_plomberie_et_sanitaire',
    'materiaux_pour_travaux_electricite','revetement_des_murs_et_sols','peinture_vernis_chaux','materiaux_pour_etancheite')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    trimestre.append(str(row[col_num]))
                elif col_num==1:
                    icc_global.append(row[col_num])
                elif col_num==2:
                    materiaux_de_construction.append(row[col_num])
                elif col_num==3:
                    biens_et_service_de_gestion_du_chantier.append(row[col_num])
                elif col_num==4:
                    location_de_materiels.append(row[col_num])
                elif col_num==5:
                    main_oeuvre.append(row[col_num])
                elif col_num==6:
                    materiaux_de_base.append(row[col_num])
                elif col_num==7:
                    materiaux_pour_couverture.append(row[col_num])
                elif col_num==8:
                    materiaux_de_menuiserie.append(row[col_num])
                elif col_num==9:
                    materiaux_de_plomberie_et_sanitaire.append(row[col_num])
                elif col_num==10:
                    materiaux_pour_travaux_electricite.append(row[col_num])
                elif col_num==11:
                    revetement_des_murs_et_sols.append(row[col_num])
                elif col_num==12:
                    peinture_vernis_chaux.append(row[col_num])
                else:
                    materiaux_pour_etancheite.append(row[col_num])
    
    return render(request,'ICC/chartjs.html',{'trimestre':trimestre,'icc_global':icc_global,'materiaux_de_construction':materiaux_de_construction,'biens_et_service_de_gestion_du_chantier':biens_et_service_de_gestion_du_chantier,'location_de_materiels':location_de_materiels,'main_oeuvre':main_oeuvre,'materiaux_de_base':materiaux_de_base,'materiaux_pour_couverture':materiaux_pour_couverture,'materiaux_de_menuiserie':materiaux_de_menuiserie,'materiaux_de_plomberie_et_sanitaire':materiaux_de_plomberie_et_sanitaire,'materiaux_pour_travaux_electricite':materiaux_pour_travaux_electricite,'revetement_des_murs_et_sols':revetement_des_murs_et_sols,'peinture_vernis_chaux':peinture_vernis_chaux,'materiaux_pour_etancheite':materiaux_pour_etancheite})


