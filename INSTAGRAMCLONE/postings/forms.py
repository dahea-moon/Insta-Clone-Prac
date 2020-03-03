from django import forms
from .models import Posting, Image, Comment

class PostingForm(forms.ModelForm):
    class Meta:
        model = Posting
        fields = ('contents',)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('file', )
        widgets = {
            'file': forms.FileInput(attrs={'multiple': True})
        }

ImageFormset = forms.inlineformset_factory(Posting, Image, form=ImageForm, extra=5)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)