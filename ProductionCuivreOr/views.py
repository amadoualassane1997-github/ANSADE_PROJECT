from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import xlwt
import pandas as pd
from django import forms
from django.contrib.auth.decorators import login_required
from authentification.decorators import allowed_users
from ProductionCuivreOr.forms import ProductionCuivreOrForm
from ProductionCuivreOr.models import ProductionCuivreOr

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def save(request):
    if request.method=='POST':
        form=ProductionCuivreOrForm(request.POST)
        if form.is_valid():
            try:
                
                form.save()
                return redirect('prodcror-view')
            except:
                pass
    else:
        form=ProductionCuivreOrForm()
    return render(request,'ProductionCuivreOr/form.html',{'form':form})

@login_required(login_url='login')
def view(request):
    pcos=ProductionCuivreOr.objects.all()
    return render(request,'ProductionCuivreOr/view.html',{'pcos':pcos})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete(request,trimestre):
    pco=ProductionCuivreOr.objects.get(trimestre=trimestre)
    pco.delete()
    return redirect('prodcror-view')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update(request,trimestre):
    if request.method=='POST':
        form=ProductionCuivreOrForm(request.POST,instance=ProductionCuivreOr.objects.get(trimestre=trimestre))
        if form.is_valid():
            try:
                form.save()
                return redirect('prodcror-view')
            except:
                pass
   
    else:
        form=ProductionCuivreOrForm(instance=ProductionCuivreOr.objects.get(trimestre=trimestre))
        form.fields['trimestre'].widget=forms.HiddenInput()
    context={
        'form':form,
        'trimestre':trimestre
    }
    return render(request,'ProductionCuivreOr/update.html',{'context':context})

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
            obj = ProductionCuivreOr.objects.create(trimestre=l[0],production_cuivre=l[1],
    or_quantite_en_oz_total=l[2])
            if obj !=None :
                obj.save()
        return redirect('prodcror-view')   
    return render(request,'ProductionCuivreOr/import.html')

@login_required(login_url='login')
def export_excel(request):
    if request.method == 'POST':
        d1=request.POST.get('trimestre1')
        d2=request.POST.get('trimestre2')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="production_cuivre_or.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Production Cuivre Or')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        columns=['Trimestre','Production Cuivre','Or Quantité en OZ Totale']
        

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows=ProductionCuivreOr.objects.values_list('trimestre','production_cuivre','or_quantite_en_oz_total')
        l=[]
        for row in rows:
            for col_num in range(len(row)):
                col_0=row[0].split('-')
                d1_annee=d1.split('-')
                d2_annee=d2.split('-')
                if int(col_0[1])>=int(d1_annee[1]) and int(col_0[1])<=int(d2_annee[1]):
                    l.append(row)
        v=[]
        for e in l:
            s=e[0].split('-')
            y=s[1]
            n=list(s[0])[1]
            if (y==d1.split('-')[1] and int(n)<int(list(d1.split('-')[0])[1])) or (y==d2.split('-')[1] and int(n)>int(list(d2.split('-')[0])[1])):
                pass
            else:
                v.append(e)

        for row in v:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    
        wb.save(response)
        return response
    else:
        icc_col=ProductionCuivreOr.objects.all().values('trimestre')
        return render(request,'ProductionCuivreOr/export.html',{'icc_col':icc_col})