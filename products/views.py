from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

# Create your views here.
def my_products(request):
    obj = Product.objects.all()
    product_form = ProductForm(request.POST or None)
    context = {
        'obj': obj,
        'product_form': product_form,
    }
    return render(request, 'products/main.html',context)

def edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('products:my_products')  # Adjust the URL pattern name if needed
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/edit.html', context)
