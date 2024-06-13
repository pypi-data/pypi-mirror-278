# from .models import UploadedFile
from django import forms
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile
#         fields = ('title', 'uploaded_file',)


from .models import ChatSession

class QnAForm(forms.ModelForm):
    class Meta:
        model = ChatSession
        fields = ['question', 'answer']