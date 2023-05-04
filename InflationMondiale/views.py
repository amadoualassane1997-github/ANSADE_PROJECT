from django.shortcuts import render,redirect
from InflationMondiale.forms import InflationMondialeForm
from InflationMondiale.models import InflationMondiale
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
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
        if InflationMondiale.objects.filter(date=date).exists():
            form=InflationMondialeForm(request.POST,instance=InflationMondiale.objects.get(date=date))
        else:
            form=InflationMondialeForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('inflamdle-view')
            except:
                pass
    else:
        form=InflationMondialeForm()
    return render(request,'InflationMondiale/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    infs=InflationMondiale.objects.all()
    return render(request,'InflationMondiale/view.html',{'infs':infs})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    inf=InflationMondiale.objects.get(date=date)
    inf.delete()
    return redirect('inflamdle-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=InflationMondialeForm(request.POST,instance=InflationMondiale.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('inflamdle-view')
            except:
                pass
   
    else:
        form=InflationMondialeForm(instance=InflationMondiale.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'InflationMondiale/update.html',{'context':context})

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
            obj = InflationMondiale.objects.update_or_create(date=l[0],usa=l[1],
    france=l[2],allemagne=l[3],japon=l[4],royaume_uni=l[5],italie=l[6],canada=l[7])
        return redirect('inflamdle-view')   
    return render(request,'InflationMondiale/import.html')


@login_required(login_url='login')   
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="inflation_mondiale.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('InflationMondiale')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
        
        columns=['Date','USA','France','Allemagne','Japon',
    'Royaume Uni','Italie','Canada']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=InflationMondiale.objects.filter(date__range=(d1,d2)).values_list('date','usa','france','allemagne','japon',
    'royaume_uni','italie','canada')
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
        return render(request,'InflationMondiale/export.html')


@login_required(login_url='login')
def tableau_bord(request):
    date,usa,france,allemagne,japon,royaume_uni,italie,canada=[],[],[],[],[],[],[],[]
    rows=InflationMondiale.objects.values_list('date','usa','france','allemagne','japon',
    'royaume_uni','italie','canada')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    date.append(str(row[col_num]))
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
      
    return render(request,'InflationMondiale/chartjs.html',{'date':date,'usa':usa,'france':france,'allemagne':allemagne,'japon':japon,'royaume_uni':royaume_uni,'italie':italie,'canada':canada})