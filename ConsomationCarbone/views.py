from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from ConsomationCarbone.forms import ConsomationCarboneForm
from ConsomationCarbone.models import ConsomationCarbone
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
        if ConsomationCarbone.objects.filter(date=date).exists():
            form=ConsomationCarboneForm(request.POST,instance=ConsomationCarbone.objects.get(date=date))
        else:
            form=ConsomationCarboneForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('consco2-view')
            except:
                pass
    else:
        form=ConsomationCarboneForm()
    return render(request,'ConsomationCarbone/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    ccs=ConsomationCarbone.objects.all()
    return render(request,'ConsomationCarbone/view.html',{'ccs':ccs})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    cc=ConsomationCarbone.objects.get(date=date)
    cc.delete()
    return redirect('consco2-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=ConsomationCarboneForm(request.POST,instance=ConsomationCarbone.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('consco2-view')
            except:
                pass
   
    else:
        form=ConsomationCarboneForm(instance=ConsomationCarbone.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'ConsomationCarbone/update.html',{'context':context})


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
            obj = ConsomationCarbone.objects.update_or_create(date=l[0],essence=l[1],
    kerosene=l[2],gas_oil=l[3],fuel_oil=l[4])
        return redirect('consco2-view')   
    return render(request,'ConsomationCarbone/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="consommation_carbone.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Consommation Carbone')

        row_num = 0
        
        

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
        
        columns=['Date','Essence','Kérosene','GasOil','FuelOil']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=ConsomationCarbone.objects.filter(date__range=(d1,d2)).values_list('date','essence','kerosene','gas_oil',
    'fuel_oil')
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
        return render(request,'ConsomationCarbone/export.html')
