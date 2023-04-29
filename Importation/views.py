from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from Importation.forms import ImportationForm
from Importation.models import Importation



# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def save(request):
    if request.method=='POST':
        trimestre=request.POST['trimestre']
        if Importation.objects.filter(trimestre=trimestre).exists():
            form=ImportationForm(request.POST,instance=Importation.objects.get(trimestre=trimestre))
        else:
            form=ImportationForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('imp-view')
            except:
                pass
    else:
        form=ImportationForm()
    return render(request,'Importation/form.html',{'form':form})


@login_required(login_url='login')
def view(request):
    imps=Importation.objects.all()
    return render(request,'Importation/view.html',{'imps':imps})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,trimestre):
    imp=Importation.objects.get(trimestre=trimestre)
    imp.delete()
    return redirect('imp-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,trimestre):
    if request.method=='POST':
        form=ImportationForm(request.POST,instance=Importation.objects.get(trimestre=trimestre))
        if form.is_valid():
            try:
                form.save()
                return redirect('imp-view')
            except:
                pass
   
    else:
        form=ImportationForm(instance=Importation.objects.get(trimestre=trimestre))
        form.fields['trimestre'].widget=forms.HiddenInput()
    context={
        'form':form,
        'trimestre':trimestre
    }
    return render(request,'Importation/update.html',{'context':context})

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
            Importation.objects.update_or_create(trimestre=l[0],total=l[1],
    produits_alimentaires=l[2],cosmetiques_chimiques=l[3],produits_petroliers=l[4],materiaux_de_construction=l[5],voitures_et_pieces_detachees=l[6],equipements=l[7]
    ,autres_biens_de_consommation=l[8],autres=l[9])
        return redirect('imp-view')   
    return render(request,'Importation/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('trimestre1')
        d2=request.POST.get('trimestre2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="importation.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Importation')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        columns=['Trimestre','Total','Produits alimentaires','Cosmétiques chimiques','Produits pétroliers',
    'Matériaux de construction','Voitures et pièces détachées','Equipements','Autres biens de consommation','Autres']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=Importation.objects.values_list('trimestre','total','produits_alimentaires','cosmetiques_chimiques',
    'produits_petroliers','materiaux_de_construction','voitures_et_pieces_detachees','equipements','autres_biens_de_consommation','autres')
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
        icc_col=Importation.objects.all().values('trimestre')
        return render(request,'Importation/export.html',{'icc_col':icc_col})

