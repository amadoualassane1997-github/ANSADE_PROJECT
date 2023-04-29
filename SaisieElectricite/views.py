from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
import pandas as pd
import xlwt
from django import forms
import datetime
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from SaisieElectricite.forms import SaisieElectriciteForm
from SaisieElectricite.models import SaisieElectricite
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
        if SaisieElectricite.objects.filter(date=date).exists():
            form=SaisieElectriciteForm(request.POST,instance=SaisieElectricite.objects.get(date=date))
        else:
            form=SaisieElectriciteForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('saisieelec-view')
            except:
                pass
    else:
        form=SaisieElectriciteForm()
    return render(request,'SaisieElectricite/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    ses=SaisieElectricite.objects.all()
    return render(request,'SaisieElectricite/view.html',{'ses':ses})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    se=SaisieElectricite.objects.get(date=date)
    se.delete()
    return redirect('saisieelec-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=SaisieElectriciteForm(request.POST,instance=SaisieElectricite.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('saisieelec-view')
            except:
                pass
    else:
        form=SaisieElectriciteForm(instance=SaisieElectricite.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
        context={
        'form':form,
        'date':date
       }
        
    
    return render(request,'SaisieElectricite/update.html',{'context':context})

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
            obj = SaisieElectricite.objects.update_or_create(date=l[0],millions_de_kw_h=l[1],mm_bt=l[2],mm_mt=l[3])
        return redirect('saisieelec-view')   
    return render(request,'SaisieElectricite/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="saisie_electricite.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Saisie Electricite')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
    

        columns=['Date','Millions de KW-H','MM(BT)','MM(BT)']


        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
    
        
        rows=SaisieElectricite.objects.filter(date__range=(d1, d2)).values_list('date','millions_de_kw_h','mm_bt','mm_mt')
        for row in rows:
            print(row)
            row_num += 1
            for col_num in range(len(row)):
                if isinstance(row[col_num],datetime.date):
                    ws.write(row_num, col_num, row[col_num],style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    else:
        return render(request,'SaisieElectricite/export.html')
