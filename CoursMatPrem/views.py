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
        if CoursMatPrem.objects.filter(date=date).exists():
            form=CoursMatPremForm(request.POST,instance=CoursMatPrem.objects.get(date=date))
        else:
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
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    cmp=CoursMatPrem.objects.get(date=date)
    cmp.delete()
    return redirect('coursmatprem-view')


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
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
            obj = CoursMatPrem.objects.update_or_create(date=l[0],cours_mondiale_du_petrole=l[1],
    prix_du_petrole_mauritanien=l[2],cours_mondiale_du_minerai_fer_du_premier_seri=l[3],prix_du_minerai_mauritanien=l[4],
    cours_mondial_du_cuivre=l[5],prix_du_cuivre_mauritanien=l[6],cours_mondiale_or=l[7],
    prix_or_mauritanien=l[8],cours_mondiale_de_poisson=l[9],prix_du_poisson_mauritanien=l[10])
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

        rows=CoursMatPrem.objects.filter(date__range=(d1,d2)).values_list('date','cours_mondiale_du_petrole','prix_du_petrole_mauritanien','cours_mondiale_du_minerai_fer_du_premier_seri','prix_du_minerai_mauritanien',
    'cours_mondial_du_cuivre','prix_du_cuivre_mauritanien','cours_mondiale_or','prix_or_mauritanien','cours_mondiale_de_poisson','prix_du_poisson_mauritanien')
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
