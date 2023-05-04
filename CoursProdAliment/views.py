from django.shortcuts import render,redirect
from CoursProdAliment.forms import CoursProdAlimentForm
from CoursProdAliment.models import CoursProdAliment
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
        if CoursProdAliment.objects.filter(date=date).exists():
            form=CoursProdAlimentForm(request.POST,instance=CoursProdAliment.objects.get(date=date))
        else:
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


@login_required(login_url='login')
def view(request):
    cpas=CoursProdAliment.objects.all()
    return render(request,'CoursProdAliment/view.html',{'cpas':cpas})


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    cpa=CoursProdAliment.objects.get(date=date)
    cpa.delete()
    return redirect('coursprodaliment-view')


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=CoursProdAlimentForm(request.POST,instance=CoursProdAliment.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('coursprodaliment-view')
            except:
                pass
   
    else:
        form=CoursProdAlimentForm(instance=CoursProdAliment.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'CoursProdAliment/update.html',{'context':context})

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
            obj = CoursProdAliment.objects.update_or_create(date=l[0],ble_eu_par_tonne=l[1],
    riz_eu_par_tonne=l[2],sucre_eu_par_tonne=l[3],the_eu_par_tonne=l[4],
    ble_mu_par_tonne=l[5],riz_mu_par_tonne=l[6],sucre_mu_par_tonne=l[7],
    the_mu_par_tonne=l[8])
        return redirect('coursprodaliment-view')   
    return render(request,'CoursProdAliment/import.html')

@login_required(login_url='login')
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

@login_required(login_url='login')
def tableau_bord(request):
    date,ble_eu_par_tonne,riz_eu_par_tonne,sucre_eu_par_tonne,the_eu_par_tonne,ble_mu_par_tonne,riz_mu_par_tonne,sucre_mu_par_tonne,the_mu_par_tonne=[],[],[],[],[],[],[],[],[]
    rows=CoursProdAliment.objects.values_list('date','ble_eu_par_tonne','riz_eu_par_tonne','sucre_eu_par_tonne','the_eu_par_tonne',
    'ble_mu_par_tonne','riz_mu_par_tonne','sucre_mu_par_tonne','the_mu_par_tonne')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    date.append(str(row[col_num]))
                elif col_num==1:
                    ble_eu_par_tonne.append(row[col_num])
                elif col_num==2:
                    riz_eu_par_tonne.append(row[col_num])
                elif col_num==3:
                    sucre_eu_par_tonne.append(row[col_num])
                elif col_num==4:
                    the_eu_par_tonne.append(row[col_num])
                elif col_num==5:
                    ble_mu_par_tonne.append(row[col_num])
                elif col_num==6:
                    riz_mu_par_tonne.append(row[col_num])
                elif col_num==7:
                    sucre_mu_par_tonne.append(row[col_num])
                else:
                    the_mu_par_tonne.append(row[col_num])
      
    return render(request,'CoursProdAliment/chartjs.html',{'date':date,'ble_eu_par_tonne':ble_eu_par_tonne,'riz_eu_par_tonne':riz_eu_par_tonne,'sucre_eu_par_tonne':sucre_eu_par_tonne,'the_eu_par_tonne':the_eu_par_tonne,'ble_mu_par_tonne':ble_mu_par_tonne,'riz_mu_par_tonne':riz_mu_par_tonne,'sucre_mu_par_tonne':sucre_mu_par_tonne,'the_mu_par_tonne':the_mu_par_tonne})


