from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from EauElectricite.forms import EauElectriciteForm
from EauElectricite.models import EauElectricite
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
        if EauElectricite.objects.filter(date=date).exists():
            form=EauElectriciteForm(request.POST,instance=EauElectricite.objects.get(date=date))
        else:
            form=EauElectriciteForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('eelec-view')
            except:
                pass
    else:
        form=EauElectriciteForm()
    return render(request,'EauElectricite/form.html',{'form':form})


@login_required(login_url='login')
def view(request):
    ees=EauElectricite.objects.all()
    return render(request,'EauElectricite/view.html',{'ees':ees})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    ee=EauElectricite.objects.get(date=date)
    ee.delete()
    return redirect('eelec-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=EauElectriciteForm(request.POST,instance=EauElectricite.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('eelec-view')
            except:
                pass
   
    else:
        form=EauElectriciteForm(instance=EauElectricite.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'EauElectricite/update.html',{'context':context})

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
            obj = EauElectricite.objects.update_or_create(date=l[0],eau_brute=l[1],
    eau_nette=l[2],elect_brute=l[3],elect_nette=l[4])
        return redirect('eelec-view')   
    return render(request,'EauElectricite/import.html')


@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="eau_electricite.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Eau Electricite')

        row_num = 0
        
        

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
        
        columns=['Date','Eau Brute','Eau Nette','Elect Brute','Elect Nette']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=EauElectricite.objects.filter(date__range=(d1,d2)).values_list('date','eau_brute','eau_nette','elect_brute',
    'elect_nette')
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
        return render(request,'EauElectricite/export.html')

@login_required(login_url='login')
def tableau_bord(request):
    date,eau_brute,eau_nette,elect_brute,elect_nette=[],[],[],[],[]
    rows=EauElectricite.objects.values_list('date','eau_brute','eau_nette','elect_brute',
    'elect_nette')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    date.append(str(row[col_num]))
                elif col_num==1:
                    eau_brute.append(row[col_num])
                elif col_num==2:
                    eau_nette.append(row[col_num])
                elif col_num==3:
                    elect_brute.append(row[col_num])
                else:
                   elect_nette.append(row[col_num])
    return render(request,'EauElectricite/chartjs.html',{'date':date,"eau_brute":eau_brute,"eau_nette":eau_nette,"elect_brute":elect_brute,"elect_nette":elect_nette})

