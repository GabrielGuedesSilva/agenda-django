from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact


def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')
    
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - '
    }
    
    return render (
        request,
        'contact/index.html',
        context
    )
    
def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    
    single_contact = get_object_or_404(Contact, pk=contact_id)
    
    site_title = f'{single_contact.first_name} {single_contact.last_name} -'
    
    context = {
        'contact': single_contact,
        'site_title': site_title
    }
    
    return render (
        request,
        'contact/contact.html',
        context
    )
    
def search (request):
    search_value = request.GET.get('q', '').strip()
    # print('search_value', search_value)
    
    if search_value == '':
        return redirect('contact:index')
    
    contacts = Contact.objects.filter(show=True).filter(
        Q(first_name__icontains=search_value) | 
        Q(last_name__icontains=search_value) |
        Q(phone__icontains=search_value) |
        Q(email__icontains=search_value)
        ).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - ',
        'search_value': search_value
    }

    return render (
        request,
        'contact/index.html',
        context
)

@login_required(login_url='contact:login')
def create (request):
    form_action = reverse('contact:create')
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
    
        context = {
            'form': form,
            'form_action': form_action,
            'contain_image': True
        }
        
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect('contact:contact_update', contact_id=contact.id)
        
        return render (
            request,
            'contact/create.html',
            context
        )
    
    context = {
            'form': ContactForm(),
            'form_action': form_action,
            'contain_image': True
        }
    
    return render (
            request,
            'contact/create.html',
            context
        )
    
@login_required(login_url='contact:login')
def update (request, contact_id):
    
    form_action = reverse('contact:contact_update', args=(contact_id,))
    
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
    
        context = {
            'form': form,
            'form_action': form_action,
            'contain_image': True
        }
        
        if form.is_valid():
            contact = form.save()
            return redirect('contact:contact_update', contact_id=contact.id)
        
        return render (
            request,
            'contact/contact_update.html',
            context
        )
    
    context = {
            'form': ContactForm(instance=contact),
            'form_action': form_action,
            'contain_image': True
        }
    
    return render (
            request,
            'contact/contact_update.html',
            context
        )
    
@login_required(login_url='contact:login')
def delete (request, contact_id):
    
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
    
    confirmation = request.POST.get('confirmation', 'no')
    
    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')
    
    
    context = {
        'contact': contact,
        'confirmation': confirmation
    }
    
    
    return render (
        request,
        'contact/contact.html',
        context
    )