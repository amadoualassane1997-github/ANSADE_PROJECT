
from django.http import HttpResponse
from django.shortcuts import render, redirect
from MonnaieChange.forms import MonnaieChangeForm
from MonnaieChange.models import MonnaieChange
from django.core.files.storage import FileSystemStorage
import pandas as pd
import xlwt
from django import forms
import datetime
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
        if MonnaieChange.objects.filter(date=date).exists():
            form=MonnaieChangeForm(request.POST,instance=MonnaieChange.objects.get(date=date))
        else:
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


@login_required(login_url='login')
def view(request):
    mcs=MonnaieChange.objects.all()
    return render(request,'monnaichange/view.html',{'mcs':mcs})


@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def delete(request,date):
    mc=MonnaieChange.objects.get(date=date)
    mc.delete()
    return redirect('monnaiechange-view')

@login_required(login_url='login')
@allowed_users(allowed_roles=['modifieur'])
def update(request,date):
    if request.method=='POST':
        form=MonnaieChangeForm(request.POST,instance=MonnaieChange.objects.get(date=date))
        if form.is_valid():
            try:
                form.save()
                return redirect('monnaiechange-view')
            except:
                pass
    else:
        form=MonnaieChangeForm(instance=MonnaieChange.objects.get(date=date))
        form.fields['date'].widget=forms.HiddenInput()
        context={
        'form':form,
        'date':date
       }
        
    
    return render(request,'monnaichange/update.html',{'context':context})

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
            print(l[0])
            MonnaieChange.objects.update_or_create(date=date,dollar_des_u_e=l[1],
    euro=l[2],sterling=l[3],yen=l[4],
    dirham_marocain=l[5],dinar_tunisien=l[6],dinar_algerien=l[7],
    franc_cfa=l[8],dts=l[9])
        return redirect('monnaiechange-view')   
    return render(request,'monnaichange/import.html')


@login_required(login_url='login')
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
    




@login_required(login_url='login')
def tableau_bord(request):
    date,dollar_des_u_e,euro,sterling,yen,dirham_marocain,dinar_tunisien,dinar_algerien,franc_cfa,dts=[],[],[],[],[],[],[],[],[],[]
    rows=MonnaieChange.objects.all().values_list('date','dollar_des_u_e','euro','sterling','yen',
    'dirham_marocain','dinar_tunisien','dinar_algerien','franc_cfa','dts')
    for row in rows:
            for col_num in range(len(row)):
                if col_num==0:
                    date.append(str(row[col_num]))
                elif col_num==1:
                    dollar_des_u_e.append(row[col_num])
                elif col_num==2:
                    euro.append(row[col_num])
                elif col_num==3:
                    sterling.append(row[col_num])
                elif col_num==4:
                    yen.append(row[col_num])
                elif col_num==5:
                    dirham_marocain.append(row[col_num])
                elif col_num==6:
                    dinar_tunisien.append(row[col_num])
                elif col_num==7:
                    dinar_algerien.append(row[col_num])
                elif col_num==8:
                    franc_cfa.append(row[col_num])
                else:
                    dts.append(row[col_num])
      
    return render(request,'monnaichange/chartjs.html',{'date':date,'dollar_des_u_e':dollar_des_u_e,'euro':euro,
                                                       'sterling':sterling,'yen':yen,'dirham_marocain':dirham_marocain,'dinar_tunisien':dinar_tunisien,
                                                       'dinar_algerien':dinar_algerien,'franc_cfa':franc_cfa,'dts':dts})


