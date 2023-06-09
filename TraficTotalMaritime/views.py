from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from TraficTotalMaritime.forms import TraficTotalMaritimeForm
from TraficTotalMaritime.models import TraficTotalMaritime
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
        if TraficTotalMaritime.objects.filter(date=date).exists():
            form=TraficTotalMaritimeForm(request.POST,instance=TraficTotalMaritime.objects.get(date=date))
        else:
            form=TraficTotalMaritimeForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('trafictotalmaritime-view')
            except:
                pass
    else:
        form=TraficTotalMaritimeForm()
    return render(request,'TraficTotalMaritime/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    ttms=TraficTotalMaritime.objects.all()
    return render(request,'TraficTotalMaritime/view.html',{'ttms':ttms})


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    ttm=TraficTotalMaritime.objects.get(date=date)
    ttm.delete()
    return redirect('trafictotalmaritime-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=TraficTotalMaritimeForm(request.POST,instance=TraficTotalMaritime.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('trafictotalmaritime-view')
            except:
                pass
   
    else:
        form=TraficTotalMaritimeForm(instance=TraficTotalMaritime.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'TraficTotalMaritime/update.html',{'context':context})

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
            obj = TraficTotalMaritime.objects.update_or_create(date=l[0],trafic_total_tonnes=l[1],
    total_nombre=l[2],port_ndb_trafic_total=l[3],port_ndb_arrive_navires_nombre=l[4],trafic_total=l[5],nombre_total_navires=l[6])
        return redirect('trafictotalmaritime-view')   
    return render(request,'TraficTotalMaritime/import.html')

@login_required(login_url='login')   
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="trafic_total_maritime.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('TraficTotalMaritime')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
    

        columns=['Date','Trafic Total(Milliers tonnes)','Total(nombre)','Port NDB Trafic Total(1000tonnes)','Port NDB Arrivée Navires(nombre)','Trafic Total','Nombre Total Navires']


        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        
        rows=TraficTotalMaritime.objects.filter(date__range=(d1, d2)).values_list('date','trafic_total_tonnes','total_nombre','port_ndb_trafic_total','port_ndb_arrive_navires_nombre',
    'trafic_total','nombre_total_navires')
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
        return render(request,'TraficTotalMaritime/export.html')
    


@login_required(login_url='login')
def tableau_bord(request):
    date,trafic_total_tonnes,total_nombre,port_ndb_trafic_total,port_ndb_arrive_navires_nombre,trafic_total,nombre_total_navires=[],[],[],[],[],[],[]
    rows=TraficTotalMaritime.objects.values_list('date','trafic_total_tonnes','total_nombre','port_ndb_trafic_total','port_ndb_arrive_navires_nombre',
    'trafic_total','nombre_total_navires')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    date.append(str(row[col_num]))
                elif col_num==1:
                    trafic_total_tonnes.append(row[col_num])
                elif col_num==2:
                    total_nombre.append(row[col_num])
                elif col_num==3:
                    port_ndb_trafic_total.append(row[col_num])
                elif col_num==4:
                    port_ndb_arrive_navires_nombre.append(row[col_num])
                elif col_num==5:
                    trafic_total.append(row[col_num])
                else:
                    nombre_total_navires.append(row[col_num])
    return render(request,'TraficTotalMaritime/chartjs.html',{'date':date,'trafic_total_tonnes':trafic_total_tonnes,'total_nombre':total_nombre,'port_ndb_trafic_total':port_ndb_trafic_total,'port_ndb_arrive_navires_nombre':port_ndb_arrive_navires_nombre,'trafic_total':trafic_total,'nombre_total_navires':nombre_total_navires})
