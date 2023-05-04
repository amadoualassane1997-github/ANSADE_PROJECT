from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from CommerceExterieur.forms import CommerceExterieurForm
from CommerceExterieur.models import CommerceExterieur


# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def save(request):
    if request.method=='POST':
        trimestre=request.POST['trimestre']
        if CommerceExterieur.objects.filter(trimestre=trimestre).exists():
            form=CommerceExterieurForm(request.POST,instance=CommerceExterieur.objects.get(trimestre=trimestre))
        else:
            form=CommerceExterieurForm(request.POST)
        if form.is_valid():
            try:   
                form.save()
                return redirect('comext-view')
            except:
                pass
    else:
        form=CommerceExterieurForm()
    return render(request,'CommerceExterieur/form.html',{'form':form})


@login_required(login_url='login')
def view(request):
    comexts=CommerceExterieur.objects.all()
    return render(request,'CommerceExterieur/view.html',{'comexts':comexts})



@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,trimestre):
    comext=CommerceExterieur.objects.get(trimestre=trimestre)
    comext.delete()
    return redirect('comext-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,trimestre):
    if request.method=='POST':
        form=CommerceExterieurForm(request.POST,instance=CommerceExterieur.objects.get(trimestre=trimestre))
        if form.is_valid():
            try:
                form.save()
                return redirect('comext-view')
            except:
                pass
   
    else:
        form=CommerceExterieurForm(instance=CommerceExterieur.objects.get(trimestre=trimestre))
        form.fields['trimestre'].widget=forms.HiddenInput()
    context={
        'form':form,
        'trimestre':trimestre
    }
    return render(request,'CommerceExterieur/update.html',{'context':context})

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
            CommerceExterieur.objects.update_or_create(trimestre=l[0],exportations=l[1],
    importation=l[2],solde_commercial=l[3],tx_couv=l[4])
        return redirect('comext-view')   
    return render(request,'CommerceExterieur/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('trimestre1')
        d2=request.POST.get('trimestre2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="commerce_exterieur.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Commerce Exterieur')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        columns=['Trimestre','Exportations','Importations','Solde commercial','Tax couvert']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=CommerceExterieur.objects.values_list('trimestre','exportations','importation','solde_commercial',
    'tx_couv')
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
        icc_col=CommerceExterieur.objects.all().values('trimestre')
        return render(request,'CommerceExterieur/export.html',{'icc_col':icc_col})

@login_required(login_url='login')
def tableau_bord(request):
    trimestre,exportations,importation,solde_commercial,tx_couv=[],[],[],[],[]
    rows=CommerceExterieur.objects.values_list('trimestre','exportations','importation','solde_commercial',
    'tx_couv')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    trimestre.append(str(row[col_num]))
                elif col_num==1:
                    exportations.append(row[col_num])
                elif col_num==2:
                    importation.append(row[col_num])
                elif col_num==3:
                    solde_commercial.append(row[col_num])
                else:
                    tx_couv.append(row[col_num])
      
    return render(request,'CommerceExterieur/chartjs.html',{'trimestre':trimestre,'exportations':exportations,'importation':importation,'solde_commercial':solde_commercial,'tx_couv':tx_couv})


