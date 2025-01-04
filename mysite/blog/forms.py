from django import forms
# importamos el modelo Comment para poder usarlo en el formulario
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

# se crea un formulario para los comentarios con el modelo Comment
# se hereda de forms.ModelForm
class CommentForm(forms.ModelForm):
    # se define la clase Meta para el modelo Comment
    class Meta:
        model = Comment
        # se definen los campos que se mostraran en el formulario
        # estos campos se obtienen del modelo Comment
        fields = ('name', 'email', 'body')