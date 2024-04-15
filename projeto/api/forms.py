from django import forms

class CSVUploadForm(forms.Form):
    csv_arq = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(CSVUploadForm, self).__init__(*args, **kwargs)
        self.fields['csrfmiddlewaretoken'] = forms.CharField(widget=forms.HiddenInput)