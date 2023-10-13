from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.db.models import Q
from contact.forms import ContactForm


def create (request):
    # Se o método for POST, ou seja, o usuário enviar o formulário no nosso caso ele vai salvar as informações do form
    if request.method == 'POST':
        data = request.POST
        form = ContactForm(data)
    
        context = {
            'form': form
        }
        
        if form.is_valid():
            form.save()
            return redirect('contact:create')
        
        return render (
            request,
            'contact/create.html',
            context
        )
    
    context = {
            'form': ContactForm()
        }
    
    return render (
            request,
            'contact/create.html',
            context
        )