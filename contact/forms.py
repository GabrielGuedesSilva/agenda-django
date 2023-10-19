from django import forms
from django.core.exceptions import ValidationError
from contact import models

class ContactForm(forms.ModelForm):
    
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept' : 'image/*',
            }
        )
    )
    
    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs= {
    #         'class': 'classe-a classe-b',
    #         'placeholder': 'Escreva aqui'
    #         }
    #     ),
    #     label='Primeiro nome',
    #     help_text='Texto de ajuda para o seu usuário'
    # )
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     # self.fields['first_name'].widget = forms.PasswordInput()
        
    #     # self.fields['first_name'].widget.attrs.update({
    #     #     'class': 'classe-a classe-b',
    #     #     'placeholder': 'Aqui veio do init'
    #     # })
    
    class Meta:
        model = models.Contact
        fields = ('first_name', 
                  'last_name',
                  'phone',
                  'email',
                  'description',
                  'category',
                  'picture')
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs= {
        #             'class': 'classe-a classe-b',
        #             'placeholder': 'Escreva aqui'
        #         }
        #     )
        # }
        
    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name == last_name:
            erro = ValidationError(
                    'Primeiro nome não pode ser igual ao segundo',
                    code='invalid'
                )
            
            self.add_error('first_name', erro)
            self.add_error('last_name', erro)
        
        return super().clean()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                'Veio do add_error',
                code='invalid'
            )
        )
        return first_name