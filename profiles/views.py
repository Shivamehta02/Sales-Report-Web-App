from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm

from django.urls import reverse
from django.shortcuts import redirect

#for authentication #IN CASE FOR  CLASS VIEWS WE USE LoginRequiredMixin AND FOR FUNCTION VIEWS @login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
@login_required
def my_profile_view(request):
    profile=Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None,request.FILES or None,instance=profile)
    confirm = False
    update = True
    if form.is_valid():
        form.save()
        confirm= True
        update = False
        
    context={
        
        'profile':profile,
        'form':form,
        'confirm':confirm,
        'update':update,
        
        
        
    }
    return render(request,'profiles/main.html',context)

def edit(request):
    profile=Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None,request.FILES or None,instance=profile)
    confirm = False
    
    if form.is_valid():
        form.save()
        confirm= True
        
        
    context={
        
        'profile':profile,
        'form':form,
        'confirm':confirm,
        
    }
    return render(request, 'profiles/edit.html',context)

def my_view(request):
    # do some processing here
    return redirect(reverse('my_profile_view'))