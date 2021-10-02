from os import name
from django.shortcuts import render,get_object_or_404
from django.utils import dateparse
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView,DetailView,TemplateView

#for generating pdf
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#for working with csvs
from sales.models import Sale,Position,CSV
from customers.models import Customer
import csv
from django.utils.dateparse import parse_date
from products.models import Product

#for authentication #IN CASE FOR  CLASS VIEWS WE USE LoginRequiredMixin AND FOR FUNCTION VIEWS @login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class ReportListView(LoginRequiredMixin,ListView):
    model = Report
    template_name = 'reports/main.html'
    
class ReportDetailtView(LoginRequiredMixin,DetailView):
    model = Report
    template_name = 'reports/detail.html'

class UploadTemplateview(LoginRequiredMixin,TemplateView): #for csv
    template_name = 'reports/from_file.html'

@login_required
def csv_upload_view(request): #for csv
    print('file is being send')
    
    if request.method =='POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)
        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path,'r') as f:
                reader = csv.reader(f)
                reader.__next__() #basically to remove column titles from csv
                for row in reader :
                    data = " ".join(row) #to convert rows ino strings
                    data = data.split()
                    print(data)
                    # data.pop()#it removes empty list or column
                
                    transaction_id = data[1]
                    product = data[2]
                    quantity = int(data[3])
                    customer = data[4]
                    date = parse_date(data[5])
                    
                    try:
                        product_obj = Product.objects.get( name__iexact = product)
                    except Product.DoesNotExist:
                        product_obj =None
                        
                    if product_obj is not None:
                        customer_obj, _= Customer.objects.get_or_create(name = customer)
                        salesman_obj = Profile.objects.get(user = request.user)
                        position_obj = Position.objects.create(product=product_obj,quantity=quantity,created = date)
                        
                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id,customer =customer_obj,salesman= salesman_obj,created = date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
             
    return HttpResponse()

#these functions are automatically generated
def new_func1(data):
    data = new_func(data)
    return data

def new_func(data):
    data = data.split(';')
    return data
        
    
@login_required
def create_report_view(request): #for giving the report to reports section 
    if request.is_ajax():
        name = request.POST.get('name')
        remarks  = request.POST.get('remarks')
        image  = request.POST.get('image')
        
        img = get_report_image(image)
        
        author = Profile.objects.get(user = request.user)
        Report.objects.create(name = name,remarks = remarks, image=img,author= author)
        return JsonResponse({'msg':'send'})
    return JsonResponse({})

@login_required
def render_pdf_view(request,pk): #for generating pdf we are coping this function from  https://xhtml2pdf.readthedocs.io/en/latest/usage.html
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    #to download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #to display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
        