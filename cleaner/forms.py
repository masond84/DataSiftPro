from django import forms
from .models import File, EmployeeCountScoring

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['upload', 'file_type']
        
    employee_range_file = forms.ModelChoiceField(queryset=EmployeeCountScoring.objects.all(), required=False)

# Display a dropdown list of all files in the "file" model
class FileForm(forms.Form):
    ### Specify a source file ###
    filepath = forms.ModelChoiceField(queryset=File.objects.all())
    ### Edit To Allow User's To Specify Keywords ###
    keyword_file = forms.ModelChoiceField(queryset=File.objects.all())
    name_keyword_file = forms.ModelChoiceField(queryset=File.objects.all())
    ### Employee Ranges ###
    employee_range_file = forms.ModelChoiceField(queryset=File.objects.all(), required=False)
    
    # Employee Count Thresholds #
    low_threshold = forms.IntegerField(initial=200, label="Employee Count Threshold 1")
    mid_threshold = forms.IntegerField(initial=50, label="Employee Count Threshold 2")
    high_threshold = forms.IntegerField(initial=0, label="Employee Count Threshold 3")
    
    # Scoring Using Sliders
    low_score = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':0, 'max':100}), initial=100, label="Score for Threshold 1")
    mid_score = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':0, 'max':100}), initial=50, label="Score for Threshold 2")
    high_score = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':0, 'max':100}), initial=25, label="Score for Threshold 3")
    
# Create a form for keyword uploading
class KeywordWeightForm(forms.Form):
    keyword = forms.CharField(label='Keyword', max_length=100)
    weight = forms.FloatField(label='Weight')