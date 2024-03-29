from django.shortcuts import render
from django.views.generic  import ListView, DetailView
from .models import Sale
from .forms import SalesSeachForm
from reports.forms import ReportForm
import pandas as pd
from .utils  import get_customer_from_id ,get_salesman_from_id ,get_chart


#for authentication #IN CASE FOR  CLASS VIEWS WE USE LoginRequiredMixin AND FOR FUNCTION VIEWS @login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here

@login_required
def home_view(request):
    sales_df = None
    styled_table= None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None
    
    
    search_form = SalesSeachForm(request.POST or None)
    report_form = ReportForm()
    
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
    
        
        
        sale_qs = Sale.objects.filter(created__date__lte= date_to, created__date__gte= date_from) #query set
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created']= sales_df['created'].apply(lambda x: x.strftime('%d-%m-%y'))
            sales_df['updated']= sales_df['updated'].apply(lambda x: x.strftime('%d-%m-%y'))
            sales_df.rename({'customer_id': 'customer','salesman_id': 'salesman', 'id': 'sales_id'},axis=1,inplace= True)
            
            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj ={
                        'position_id':pos.id,
                        'product':pos.product.name,
                        'quantity':pos.quantity,
                        'price':pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    positions_data.append(obj)
                    
            positions_df = pd.DataFrame(positions_data)
            #now we are merging both dataframes positions and sales
            merged_df = pd.merge(sales_df,positions_df, on='sales_id')
            
            df= merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum') 
            chart = get_chart(chart_type, sales_df, results_by)
            
            
            sales_df = sales_df.to_html(classes=["table", "table table-striped ", "table-hover","thead-dark"])
            header_styles = """
            th {
                text-align: center;
            }
            """

            data_styles = """
            td {
                text-align: center;
            }
            """

            # combine the CSS styles with the HTML table
            styled_table = f"<style>{header_styles}{data_styles}</style>{sales_df}"   #we have changed sales_df to styled table to apply html classes
            #sales_df = sales_df.to_html()
            # positions_df = positions_df.to_html()
            positions_df = positions_df.to_html(classes=["table", "table table-striped ", "table-hover","thead-dark"])
            merged_df = merged_df.to_html(classes=["table", "table table-striped ", "table-hover","thead-dark"])
            df = df.to_html(classes=["table", "table table-striped ", "table-hover","thead-dark"])
            
        else:
           no_data = 'No data is available in this range of date'
    
        
    context = {
        'search_form':search_form,
        'report_form':report_form,
        'styled_table' : styled_table,
        'sales_df':sales_df,
        'positions_df': positions_df,
        'merged_df':merged_df,
        'df': df,
        'chart': chart,
        'no_data': no_data,
    }
    return render(request, 'sales/home.html',context)

# # class based View
# class SaleListView(LoginRequiredMixin,ListView):
#     model = Sale
#     template_name = 'sales/main.html'
    
# class SaleDetailView(LoginRequiredMixin,DetailView):
#     model = Sale
#     template_name = 'sales/detail.html'
    
@login_required
def sale_List_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/main.html',{'object_list':qs})
@login_required
def sale_detail_view(request,pk):
    obj = Sale.objects.get(pk = pk)
    return render(request, 'sales/detail.html',{'object':obj})





