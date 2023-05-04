from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from Exportation.forms import ExportationForm
from Exportation.models import Exportation


# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def save(request):
    if request.method=='POST':
        trimestre=request.POST['trimestre']
        if Exportation.objects.filter(trimestre=trimestre).exists():
            form=ExportationForm(request.POST,instance=Exportation.objects.get(trimestre=trimestre))
        else:
            form=ExportationForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('exp-view')
            except:
                pass
    else:
        form=ExportationForm()
    return render(request,'Exportation/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    exps=Exportation.objects.all()
    return render(request,'Exportation/view.html',{'exps':exps})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,trimestre):
    exp=Exportation.objects.get(trimestre=trimestre)
    exp.delete()
    return redirect('exp-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,trimestre):
    if request.method=='POST':
        form=ExportationForm(request.POST,instance=Exportation.objects.get(trimestre=trimestre))
        if form.is_valid():
            try:
                form.save()
                return redirect('exp-view')
            except:
                pass
   
    else:
        form=ExportationForm(instance=Exportation.objects.get(trimestre=trimestre))
        form.fields['trimestre'].widget=forms.HiddenInput()
    context={
        'form':form,
        'trimestre':trimestre
    }
    return render(request,'Exportation/update.html',{'context':context})


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
            Exportation.objects.update_or_create(trimestre=l[0],total=l[1],
    minerai_de_fer=l[2],poisson=l[3],petrole_brut=l[4],Or=l[5],cuivre=l[6],autres=l[7])
        return redirect('exp-view')   
    return render(request,'Exportation/import.html')


@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('trimestre1')
        d2=request.POST.get('trimestre2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="exportation.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Exportation')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        columns=['Trimestre','Total','Minerai de fer','Poisson','Pétrole brut',
    'Or','Cuivre','Autres']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=Exportation.objects.values_list('trimestre','total','minerai_de_fer','poisson',
    'petrole_brut','Or','cuivre','autres')
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
        icc_col=Exportation.objects.all().values('trimestre')
        return render(request,'Exportation/export.html',{'icc_col':icc_col})


@login_required(login_url='login')
def tableau_bord(request):
    trimestre,total,minerai_de_fer,poisson,petrole_brut,Or,cuivre,autres=[],[],[],[],[],[],[],[]
    rows=Exportation.objects.values_list('trimestre','total','minerai_de_fer','poisson',
    'petrole_brut','Or','cuivre','autres')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    trimestre.append(str(row[col_num]))
                elif col_num==1:
                    total.append(row[col_num])
                elif col_num==2:
                    minerai_de_fer.append(row[col_num])
                elif col_num==3:
                    poisson.append(row[col_num])
                elif col_num==4:
                    petrole_brut.append(row[col_num])
                elif col_num==5:
                    Or.append(row[col_num])
                elif col_num==6:
                    cuivre.append(row[col_num])
                else:
                    autres.append(row[col_num])
      
    return render(request,'Exportation/chartjs.html',{'trimestre':trimestre,'total':total,'minerai_de_fer':minerai_de_fer,'poisson':poisson,'petrole_brut':petrole_brut,'Or':Or,'cuivre':cuivre,'autres':autres})


