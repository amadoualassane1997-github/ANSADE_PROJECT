from django.shortcuts import render,redirect
from django.http import HttpResponse
from Budget.forms import BudgetForm
from Budget.models import Budget
from django import forms
from django.core.files.storage import FileSystemStorage
import pandas as pd
import xlwt
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
import calendar
import json
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
        if Budget.objects.filter(date=date).exists():
            form=BudgetForm(request.POST,instance=Budget.objects.get(date=date))
        else:
            form=BudgetForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('budget-view')
            except:
                pass
    else:
        form=BudgetForm()
    return render(request,'Budget/form.html',{'form':form})


@login_required(login_url='login')
def view(request):
    bgs=Budget.objects.all()
    return render(request,'Budget/view.html',{'bgs':bgs})

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    bg=Budget.objects.get(date=date)
    bg.delete()
    return redirect('budget-view')


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=BudgetForm(request.POST,instance=Budget.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('budget-view')
            except:
                pass
   
    else:
        form=BudgetForm(instance=Budget.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
    context={
        'form':form,
        'date':date
    }
    return render(request,'Budget/update.html',{'context':context})

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
            Budget.objects.update_or_create(date=l[0],rectettes_totales=l[1],
    recettes_fiscales=l[2],recettes_non_fiscales=l[3],recettes_petro_net=l[4],
    dont=l[5],depences_et_prets_net=l[6],depences_courant=l[7],
    depences_equipe_et_prets_net=l[8],restructurations_equipe_et_prets_net=l[9],solde_globale_dons_compris=l[10])
        return redirect('budget-view')   
    return render(request,'Budget/import.html')


@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('date1')
        d2=request.POST.get('date2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="budget.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Budget')

        row_num = 0
        
        

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        style=xlwt.XFStyle()
        style.num_format_str='DD/MM/YYYY'
        style.font.bold=True
        
        columns=['Date','Recettes Totales','Recettes Fiscales','Recettes Non Fiscales','Recettes Petro Net',
    'Dons','Dépenses Et Prets Nets','Dépenses Courantes','Dépenses Equip Et Pret Net','Restructuration Et Prets Nets','Solde Global dons Compris']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=Budget.objects.filter(date__range=(d1,d2)).values_list('date','rectettes_totales','recettes_fiscales','recettes_non_fiscales','recettes_petro_net',
    'dont','depences_et_prets_net','depences_courant','depences_equipe_et_prets_net','restructurations_equipe_et_prets_net','solde_globale_dons_compris')
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
        return render(request,'Budget/export.html')