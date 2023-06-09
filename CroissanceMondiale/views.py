from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from CroissanceMondiale.forms import CroissanceMondialeForm
from CroissanceMondiale.models import CroissanceMondiale

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def save(request):
    if request.method=='POST':
        trimestre=request.POST['trimestre']
        if CroissanceMondiale.objects.filter(trimestre=trimestre).exists():
            form=CroissanceMondialeForm(request.POST,instance=CroissanceMondiale.objects.get(trimestre=trimestre))
        else:
            form=CroissanceMondialeForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('croismdle-view')
            except:
                pass
    else:
        form=CroissanceMondialeForm()
    return render(request,'CroissanceMondiale/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    cms=CroissanceMondiale.objects.all()
    return render(request,'CroissanceMondiale/view.html',{'cms':cms})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,trimestre):
    cm=CroissanceMondiale.objects.get(trimestre=trimestre)
    cm.delete()
    return redirect('croismdle-view')


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,trimestre):
    if request.method=='POST':
        form=CroissanceMondialeForm(request.POST,instance=CroissanceMondiale.objects.get(trimestre=trimestre))
        if form.is_valid():
            try:
                form.save()
                return redirect('croismdle-view')
            except:
                pass
   
    else:
        form=CroissanceMondialeForm(instance=CroissanceMondiale.objects.get(trimestre=trimestre))
        form.fields['trimestre'].widget=forms.HiddenInput()
    context={
        'form':form,
        'trimestre':trimestre
    }
    return render(request,'CroissanceMondiale/update.html',{'context':context})

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
            CroissanceMondiale.objects.update_or_create(trimestre=l[0],usa=l[1],
    france=l[2],allemagne=l[3],japon=l[4],royaume_uni=l[5],italie=l[6],canada=l[7])
        return redirect('croismdle-view')   
    return render(request,'CroissanceMondiale/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('trimestre1')
        d2=request.POST.get('trimestre2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="croissance_mondiale.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Croissance Mondiale')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        columns=['Trimestre','USA','France','Allemagne','Japon','Royaume-Uni','Canada']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=CroissanceMondiale.objects.values_list('trimestre','usa','france','allemagne',
    'japon','royaume_uni','italie','canada')
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
        icc_col=CroissanceMondiale.objects.all().values('trimestre')
        return render(request,'CroissanceMondiale/export.html',{'icc_col':icc_col})

@login_required(login_url='login')
def tableau_bord(request):
    trimestre,usa,france,allemagne,japon,royaume_uni,italie,canada=[],[],[],[],[],[],[],[]
    rows=CroissanceMondiale.objects.values_list('trimestre','usa','france','allemagne',
    'japon','royaume_uni','italie','canada')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    trimestre.append(str(row[col_num]))
                elif col_num==1:
                    usa.append(row[col_num])
                elif col_num==2:
                    france.append(row[col_num])
                elif col_num==3:
                    allemagne.append(row[col_num])
                elif col_num==4:
                    japon.append(row[col_num])
                elif col_num==5:
                    royaume_uni.append(row[col_num])
                elif col_num==6:
                    italie.append(row[col_num])
                else:
                    canada.append(row[col_num])
      
    return render(request,'CroissanceMondiale/chartjs.html',{'trimestre':trimestre,'usa':usa,'france':france,'allemagne':allemagne,'japon':japon,'royaume_uni':royaume_uni,'italie':italie,'canada':canada})


