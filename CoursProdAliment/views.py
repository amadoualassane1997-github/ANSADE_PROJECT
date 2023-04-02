from django.shortcuts import render,redirect
from CoursProdAliment.forms import CoursProdAlimentForm
from CoursProdAliment.models import CoursProdAliment
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
import datetime

# Create your views here.

def save(request):
    if request.method=='POST':
        form=CoursProdAlimentForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('coursprodaliment-view')
            except:
                pass
    else:
        form=CoursProdAlimentForm()
    return render(request,'CoursProdAliment/form.html',{'form':form})

def view(request):
    cpas=CoursProdAliment.objects.all()
    return render(request,'CoursProdAliment/view.html',{'cpas':cpas})

def delete(request,id):
    cpa=CoursProdAliment.objects.get(id=id)
    cpa.delete()
    return redirect('coursprodaliment-view')

def update(request,id):
    if request.method=='POST':
        form=CoursProdAlimentForm(request.POST,instance=CoursProdAliment.objects.get(id=id))
        if form.is_valid():
            try:
                form.save()
                return redirect('coursprodaliment-view')
            except:
                pass
   
    else:
        form=CoursProdAlimentForm(instance=CoursProdAliment.objects.get(id=id))
    context={
        'form':form,
        'id':id
    }
    return render(request,'CoursProdAliment/update.html',{'context':context})


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
            obj = CoursProdAliment.objects.create(date=l[0],ble_eu_par_tonne=l[1],
    riz_eu_par_tonne=l[2],sucre_eu_par_tonne=l[3],the_eu_par_tonne=l[4],
    ble_mu_par_tonne=l[5],riz_mu_par_tonne=l[6],sucre_mu_par_tonne=l[7],
    the_mu_par_tonne=l[8])
            if obj !=None :
                obj.save()
        return redirect('coursprodaliment-view')   
    return render(request,'CoursProdAliment/import.html')


def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="cours_prod_aliment.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('CoursProdAliment')

        row_num = 0
        
        

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
        
        columns=['Date','Blé($ EU/tonne)','Riz($ EU/tonne)','Sucre($ EU/tonne)','Thé($ EU/tonne)',
    'Blé(UM/tonne)','Riz(UM/tonne)','Sucre(UM/tonne)','Thé(UM/tonne)']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=CoursProdAliment.objects.filter(date__range=(d1,d2)).values_list('date','ble_eu_par_tonne','riz_eu_par_tonne','sucre_eu_par_tonne','the_eu_par_tonne',
    'ble_mu_par_tonne','riz_mu_par_tonne','sucre_mu_par_tonne','the_mu_par_tonne')
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
        return render(request,'CoursProdAliment/export.html')
