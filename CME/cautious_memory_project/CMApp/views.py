from django.shortcuts import render, HttpResponse, redirect
from . forms import EntryForm, CustomUserCreationForm
from django.contrib import messages


# Create your views here.
def index(request):
    new_entry_form = EntryForm()
    context= {"entry_form":new_entry_form}

    return render(request, "CMApp/index.html", context=context)

def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = CustomUserCreationForm()

    return render(request, 'CMApp/register.html', {'form': f})
