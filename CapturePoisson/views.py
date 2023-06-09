from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from CapturePoisson.forms import CapturePoissonForm
from CapturePoisson.models import CapturePoisson
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
        if CapturePoisson.objects.filter(date=date).exists():
            form=CapturePoissonForm(request.POST,instance=CapturePoisson.objects.get(date=date))
        else:
            form=CapturePoissonForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('capp-view')
            except:
                pass
    else:
        form=CapturePoissonForm()
    return render(request,'CapturePoisson/form.html',{'form':form})


@login_required(login_url='login')
def view(request):
    cps=CapturePoisson.objects.all()
    return render(request,'CapturePoisson/view.html',{'cps':cps})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    cp=CapturePoisson.objects.get(date=date)
    cp.delete()
    return redirect('capp-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=CapturePoissonForm(request.POST,instance=CapturePoisson.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('capp-view')
            except:
                pass
   
    else:
        form=CapturePoissonForm(instance=CapturePoisson.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'CapturePoisson/update.html',{'context':context})

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
            obj = CapturePoisson.objects.update_or_create(date=l[0],pelagiques=l[1],
    demersaux=l[2],cephalopodes=l[3],crustaces=l[4],capture_total=l[5])
        return redirect('capp-view')   
    return render(request,'CapturePoisson/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="capture_poisson.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Capture Poisson')

        row_num = 0
        
        

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
        
        columns=['Date','PELAGIQUES','DEMERSAUX','CEPHALOPODES','CRUSTACES','CAPTURES TOTALES']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=CapturePoisson.objects.filter(date__range=(d1,d2)).values_list('date','pelagiques','demersaux','cephalopodes',
    'crustaces','capture_total')
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
        return render(request,'CapturePoisson/export.html')


@login_required(login_url='login')
def tableau_bord(request):
    date,pelagiques,demersaux,cephalopodes,crustaces,capture_total=[],[],[],[],[],[]
    rows=CapturePoisson.objects.values_list('date','pelagiques','demersaux','cephalopodes',
    'crustaces','capture_total')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    date.append(str(row[col_num]))
                elif col_num==1:
                    pelagiques.append(row[col_num])
                elif col_num==2:
                    demersaux.append(row[col_num])
                elif col_num==3:
                    cephalopodes.append(row[col_num])
                elif col_num==4:
                    crustaces.append(row[col_num])
                else:
                    capture_total.append(row[col_num])
      
    return render(request,'CapturePoisson/chartjs.html',{'date':date,"pelagiques":pelagiques,"demersaux":demersaux,"cephalopodes":cephalopodes,"crustaces":crustaces,"capture_total":capture_total})


