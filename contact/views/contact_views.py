from django.shortcuts import render, get_object_or_404
from contact.models import Contact
from django.http import Http404

def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')[5:10]
    
    print(contacts.query)
    
    context = {
        'contacts': contacts
    }
    
    return render (
        request,
        'contact/index.html',
        context
    )
    
def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    
    single_contact = get_object_or_404(Contact, pk=contact_id)
    
    context = {
        'contact': single_contact
    }
    
    return render (
        request,
        'contact/contact.html',
        context
    )