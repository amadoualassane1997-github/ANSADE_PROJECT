import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from MonnaieChange.forms import MonnaieChangeForm
from MonnaieChange.models import MonnaieChange
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .models import *
import xlwt
import datetime

# Create your views here.

def save(request):
    if request.method=='POST':
        form=MonnaieChangeForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('monnaiechange-view')
            except:
                pass
    else:
        form=MonnaieChangeForm()
    return render(request,'monnaichange/form.html',{'form':form})

def view(request):
    mcs=MonnaieChange.objects.all()
    return render(request,'monnaichange/view.html',{'mcs':mcs})

def delete(request,id):
    mc=MonnaieChange.objects.get(id=id)
    mc.delete()
    return redirect('monnaiechange-view')


def update(request,id):
    if request.method=='POST':
        form=MonnaieChangeForm(request.POST,instance=MonnaieChange.objects.get(id=id))
        if form.is_valid():
            try:
                form.save()
                return redirect('monnaiechange-view')
            except:
                pass
   
    else:
        form=MonnaieChangeForm(instance=MonnaieChange.objects.get(id=id))
    context={
        'form':form,
        'id':id
    }
    return render(request,'monnaichange/update.html',{'context':context})

    
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
            obj = MonnaieChange.objects.create(date=l[0],dollar_des_u_e=l[1],
    euro=l[2],sterling=l[3],yen=l[4],
    dirham_marocain=l[5],dinar_tunisien=l[6],dinar_algerien=l[7],
    franc_cfa=l[8],dts=l[9])
            if obj !=None :
                obj.save()
        return redirect('monnaiechange-view')   
    return render(request,'monnaichange/import.html')

def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="monnaie_change.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Monnaie Change')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
    

        columns=['Date','Dollar Des U E','Euro','Sterling','Yen','Dirham Marocain','Dinar Tunisien','Dinar Algerien','Franc CFA','DTS']


        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        

        
        

        
        rows=MonnaieChange.objects.filter(date__range=(d1, d2)).values_list('date','dollar_des_u_e','euro','sterling','yen',
    'dirham_marocain','dinar_tunisien','dinar_algerien','franc_cfa','dts')
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
        return render(request,'monnaichange/export.html')


