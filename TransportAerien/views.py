from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from TransportAerien.forms import TransportAerienForm
from TransportAerien.models import TransportAerien
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
        if TransportAerien.objects.filter(date=date).exists():
            form=TransportAerienForm(request.POST,instance=TransportAerien.objects.get(date=date))
        else:
            form=TransportAerienForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('transaerien-view')
            except:
                pass
    else:
        form=TransportAerienForm()
    return render(request,'TransportAerien/form.html',{'form':form})


@login_required(login_url='login')
def view(request):
    tas=TransportAerien.objects.all()
    return render(request,'TransportAerien/view.html',{'tas':tas})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    ta=TransportAerien.objects.get(date=date)
    ta.delete()
    return redirect('transaerien-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=TransportAerienForm(request.POST,instance=TransportAerien.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('transaerien-view')
            except:
                pass
   
    else:
        form=TransportAerienForm(instance=TransportAerien.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'TransportAerien/update.html',{'context':context})


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
            obj = TransportAerien.objects.update_or_create(date=l[0],passagers_arrives=l[1],
    passagers_depart=l[2],total_passagers=l[3],mvmt_avion_arriv=l[4])
        return redirect('transaerien-view')   
    return render(request,'TransportAerien/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="transport_aerien.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Transport Aerien')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
    

        columns=['Date','Passagers Arrivés','Passagers Depart','Total Passagers','Mouvement Avion Arrivés']


        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        
        rows=TransportAerien.objects.filter(date__range=(d1, d2)).values_list('date','passagers_arrives','passagers_depart','total_passagers','mvmt_avion_arriv')
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
        return render(request,'TransportAerien/export.html')
