from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from contact.forms import ContactForm
from django.urls import reverse
from contact.models import Contact

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
            contact = form.save()
            return redirect('contact:update', contact_id=contact.id)
        
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
    
def update (request, contact_id):
    
    form_action = reverse('contact:contact_update', args=(contact_id,))
    
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    
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
    
def delete (request, contact_id):
    
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    
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