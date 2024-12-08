from django import forms
from .models import Libro, GENEROS_CHOICES

class LibroForm(forms.ModelForm):
    genero = forms.ChoiceField(choices=GENEROS_CHOICES, required=True)
    genero_personalizado = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'genero', 'genero_personalizado', 'cantidad', 'disponible', 'imagen', 'restriccion_edad']

    def clean(self):
        cleaned_data = super().clean()
        genero = cleaned_data.get('genero')
        genero_personalizado = cleaned_data.get('genero_personalizado')

        if genero == 'Otro' and not genero_personalizado:
            raise forms.ValidationError("Por favor, especifique un género personalizado.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.genero == 'Otro':
            instance.genero_personalizado = self.cleaned_data['genero_personalizado']
        else:
            instance.genero_personalizado = None
        if commit:
            instance.save()
        return instance