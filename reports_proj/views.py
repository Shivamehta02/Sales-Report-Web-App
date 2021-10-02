from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User,auth #for register
from django.contrib import messages #for register


def register_view(request):
    if request.method == 'POST':
        
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.warning(request, 'Username taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.warning(request, 'Email already exists')
                    return redirect('register')
                else: 
                    user = User.objects.create_user(first_name = first_name,last_name= last_name,username=username, email=email,password=password1)
                    user.save()
                    messages.success(request,"Account sucessfully created")
                    return redirect('login')  
         
            else:
                messages.info(request, 'password not matching.')
                return redirect('register')

    else:   
     return render(request,'register.html')
            
        

#for authentication
def logout_view(request):
    logout(request)
    return redirect('login')
    
    
def login_view(request):
    error_message= None
    form = AuthenticationForm()
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if(request).GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('sales:home')
        else:
            error_message= 'OOPS!...something went wrong'
            
            
    context={
        'form':form,
        'error_message':error_message,
        
    }
    
    return render(request,'auth/login.html',context)




    
