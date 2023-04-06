import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from CoursMatPrem.forms import CoursMatPremForm
from CoursMatPrem.models import CoursMatPrem
from django.core.files.storage import FileSystemStorage
import pandas as pd
import xlwt
import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def save(request):
    if request.method=='POST':
        form=CoursMatPremForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('coursmatprem-view')
            except:
                pass
    else:
        form=CoursMatPremForm()
    return render(request,'CoursMatPrem/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    cmps=CoursMatPrem.objects.all()
    return render(request,'CoursMatPrem/view.html',{'cmps':cmps})
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete(request,date):
    cmp=CoursMatPrem.objects.get(date=date)
    cmp.delete()
    return redirect('coursmatprem-view')
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update(request,date):
    if request.method=='POST':
        form=CoursMatPremForm(request.POST,instance=CoursMatPrem.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('coursmatprem-view')
            except:
                pass
   
    else:
        form=CoursMatPremForm(instance=CoursMatPrem.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'CoursMatPrem/update.html',{'context':context})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
            obj = CoursMatPrem.objects.create(date=l[0],cours_mon_pet=l[1],
    prix_pet_mr=l[2],cours_mon_min_fer_prem_seri=l[3],prix_min_mr=l[4],
    cours_mon_cuivre=l[5],prix_cuivre_mr=l[6],cours_mon_or=l[7],
    prix_or_mr=l[8],cours_mon_poisson=l[9],prix_poisson_mr=l[10])
            if obj !=None :
                obj.save()
        return redirect('coursmatprem-view')   
    return render(request,'CoursMatPrem/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="cours_mat_prem.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('CoursMatPrem')

        row_num = 0
        
        

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
        
        columns=['Date','Cours mondial du pétrole','Prix du pétrole mauritanien','Cours mondial du minerai de fer 1ère série','Prix du minerai mauritanien',
    'Cours mondial du cuivre','Prix du cuivre mauritanien','Cours mondial de l\'or','Prix de l\'or mauritanien','Cours modial du poisson','Prix du poisson mauritanien']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=CoursMatPrem.objects.filter(date__range=(d1,d2)).values_list('date','cours_mon_pet','prix_pet_mr','cours_mon_min_fer_prem_seri','prix_min_mr',
    'cours_mon_cuivre','prix_cuivre_mr','cours_mon_or','prix_or_mr','cours_mon_poisson','prix_poisson_mr')
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
        return render(request,'CoursMatPrem/export.html')
