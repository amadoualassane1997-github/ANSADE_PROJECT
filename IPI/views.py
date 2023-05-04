from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from IPI.forms import IpiForm
from IPI.models import Ipi

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def save(request):
    if request.method=='POST':
        trimestre=request.POST['trimestre']
        if Ipi.objects.filter(trimestre=trimestre).exists():
            form=IpiForm(request.POST,instance=Ipi.objects.get(trimestre=trimestre))
        else:
            form=IpiForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('ipi-view')
            except:
                pass
    else:
        form=IpiForm()
    return render(request,'IPI/form.html',{'form':form})


@login_required(login_url='login')
def view(request):
    ipis=Ipi.objects.all()
    return render(request,'IPI/view.html',{'ipis':ipis})


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,trimestre):
    ipi=Ipi.objects.get(trimestre=trimestre)
    ipi.delete()
    return redirect('ipi-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,trimestre):
    if request.method=='POST':
        form=IpiForm(request.POST,instance=Ipi.objects.get(trimestre=trimestre))
        if form.is_valid():
            try:
                form.save()
                return redirect('ipi-view')
            except:
                pass
   
    else:
        form=IpiForm(instance=Ipi.objects.get(trimestre=trimestre))
        form.fields['trimestre'].widget=forms.HiddenInput()
    context={
        'form':form,
        'trimestre':trimestre
    }
    return render(request,'IPI/update.html',{'context':context})

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
            Ipi.objects.update_or_create(trimestre=l[0],indice_general=l[1],
    indice_industries_extractives=l[2],indice_des_industries_manufacturieres=l[3],indice_de_energie=l[4],extraction_de_minerais_metaliques=l[5],fabrication_de_produits_alimentaires=l[6],fabrication_de_boisson=l[7]
    ,travail_de_cuir=l[8],travail_du_bois_et_fabrication_articles_en_bois_hors_meubles=l[9],fabrication_de_papier_cartons_et_articles_en_papier_ou_en_carton=l[10],fabrication_de_produits_chimiques=l[11],
    travail_de_caoutchouc_et_du_plastique=l[12],fabrication_de_materiaux_mineraux=l[13],metalurgie=l[14],fabrication_autres_materiel_de_transport=l[15],
    autres_industries_manufacturieres=l[16],production_et_distribution_electricite=l[17],captage_traitement_et_distribution_eau=l[18])
        return redirect('ipi-view')   
    return render(request,'IPI/import.html')



@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('trimestre1')
        d2=request.POST.get('trimestre2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ipi.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('IPI')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        columns=['Trimestre','Indice Général','Indice Industries Extractives','Indice des Industries Manufacturières','Indice de l\'Energie',
    'Extraction de minerais métaliques','Fabrication de produits alimentaires','Fabrication de boisson','Travail de cuir','Travail du bois et fabrication d\'articles en bois hors  meubles','Fabrication de papier, cartons et d\'articles en papier ou en carton',
    'Fabrication de produits chimiques','Travail de caoutchouc et du plastique','Fabrication de matériaux minéraux','Métalurgie','Fabrication d\'autres matériel de transport','Autres industries manufacturières','Production et distribution d\'électricité','Captage,traitement et distribution d\'eau']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=Ipi.objects.values_list('trimestre','indice_general','indice_industries_extractives','indice_des_industries_manufacturieres',
    'indice_de_energie','extraction_de_minerais_metaliques','fabrication_de_produits_alimentaires','fabrication_de_boisson','travail_de_cuir','travail_du_bois_et_fabrication_articles_en_bois_hors_meubles',
    'fabrication_de_papier_cartons_et_articles_en_papier_ou_en_carton','fabrication_de_produits_chimiques','travail_de_caoutchouc_et_du_plastique','fabrication_de_materiaux_mineraux',
    'metalurgie','fabrication_autres_materiel_de_transport','autres_industries_manufacturieres','production_et_distribution_electricite','captage_traitement_et_distribution_eau')
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
        icc_col=Ipi.objects.all().values('trimestre')
        return render(request,'Ipi/export.html',{'icc_col':icc_col})
    


@login_required(login_url='login')
def tableau_bord(request):
    trimestre,indice_general,indice_industries_extractives,indice_des_industries_manufacturieres,indice_de_energie,extraction_de_minerais_metaliques,fabrication_de_produits_alimentaires,fabrication_de_boisson,travail_de_cuir,travail_du_bois_et_fabrication_articles_en_bois_hors_meubles,fabrication_de_papier_cartons_et_articles_en_papier_ou_en_carton,fabrication_de_produits_chimiques,travail_de_caoutchouc_et_du_plastique,fabrication_de_materiaux_mineraux,metalurgie,fabrication_autres_materiel_de_transport,autres_industries_manufacturieres,production_et_distribution_electricite,captage_traitement_et_distribution_eau=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    rows=Ipi.objects.values_list('trimestre','indice_general','indice_industries_extractives','indice_des_industries_manufacturieres',
    'indice_de_energie','extraction_de_minerais_metaliques','fabrication_de_produits_alimentaires','fabrication_de_boisson','travail_de_cuir','travail_du_bois_et_fabrication_articles_en_bois_hors_meubles',
    'fabrication_de_papier_cartons_et_articles_en_papier_ou_en_carton','fabrication_de_produits_chimiques','travail_de_caoutchouc_et_du_plastique','fabrication_de_materiaux_mineraux',
    'metalurgie','fabrication_autres_materiel_de_transport','autres_industries_manufacturieres','production_et_distribution_electricite','captage_traitement_et_distribution_eau')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    trimestre.append(str(row[col_num]))
                elif col_num==1:
                    indice_general.append(row[col_num])
                elif col_num==2:
                    indice_industries_extractives.append(row[col_num])
                elif col_num==3:
                    indice_des_industries_manufacturieres.append(row[col_num])
                elif col_num==4:
                    indice_de_energie.append(row[col_num])
                elif col_num==5:
                    extraction_de_minerais_metaliques.append(row[col_num])
                elif col_num==6:
                    fabrication_de_produits_alimentaires.append(row[col_num])
                elif col_num==7:
                    fabrication_de_boisson.append(row[col_num])
                elif col_num==8:
                    travail_de_cuir.append(row[col_num])
                elif col_num==9:
                    travail_du_bois_et_fabrication_articles_en_bois_hors_meubles.append(row[col_num])
                elif col_num==10:
                    fabrication_de_papier_cartons_et_articles_en_papier_ou_en_carton.append(row[col_num])
                elif col_num==11:
                    fabrication_de_produits_chimiques.append(row[col_num])
                elif col_num==12:
                    travail_de_caoutchouc_et_du_plastique.append(row[col_num])
                elif col_num==13:
                    fabrication_de_materiaux_mineraux.append(row[col_num])
                elif col_num==14:
                    metalurgie.append(row[col_num])
                elif col_num==15:
                    fabrication_autres_materiel_de_transport.append(row[col_num])
                elif col_num==16:
                    autres_industries_manufacturieres.append(row[col_num])
                elif col_num==17:
                    production_et_distribution_electricite.append(row[col_num])
                else:
                    captage_traitement_et_distribution_eau.append(row[col_num])
      
    return render(request,'Ipi/chartjs.html',{'trimestre':trimestre,'indice_general':indice_general,'indice_industries_extractives':indice_industries_extractives,'indice_des_industries_manufacturieres':indice_des_industries_manufacturieres,'indice_de_energie':indice_de_energie,'extraction_de_minerais_metaliques':extraction_de_minerais_metaliques,'fabrication_de_produits_alimentaires':fabrication_de_produits_alimentaires,'fabrication_de_boisson':fabrication_de_boisson,'travail_de_cuir':travail_de_cuir,'travail_du_bois_et_fabrication_articles_en_bois_hors_meubles':travail_du_bois_et_fabrication_articles_en_bois_hors_meubles,'fabrication_de_papier_cartons_et_articles_en_papier_ou_en_carton':fabrication_de_papier_cartons_et_articles_en_papier_ou_en_carton,'fabrication_de_produits_chimiques':fabrication_de_produits_chimiques,'travail_de_caoutchouc_et_du_plastique':travail_de_caoutchouc_et_du_plastique,'fabrication_de_materiaux_mineraux':fabrication_de_materiaux_mineraux,'metalurgie':metalurgie,'fabrication_autres_materiel_de_transport':fabrication_autres_materiel_de_transport,'autres_industries_manufacturieres':autres_industries_manufacturieres,'production_et_distribution_electricite':production_et_distribution_electricite,'captage_traitement_et_distribution_eau':captage_traitement_et_distribution_eau})



