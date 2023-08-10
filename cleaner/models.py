from django.db import models
from django.core.files.storage import default_storage
import os

# Create your models here.
''' File: Store files within the system '''

# custom function
def get_upload_to(instance, filename):
    return 'uploads/' + filename

class File(models.Model):
    TYPE_CHOICES = [
        ('keyword', 'Keyword'),
        ('source', 'Source'),
    ]
    
    name = models.CharField(max_length=255, null=True, blank=True, help_text="User-defined name for the file")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to=get_upload_to, max_length=500)
    file_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='source')
    
    ''' Handle Renaming'''
    def rename_file(self, new_name):
        # get the old file path
        old_file_path = self.upload.path
        # get the extension also
        _, extension = os.path.splitext(old_file_path)
        # get the new file path
        new_file_path = os.path.join(os.path.dirname(old_file_path), new_name + extension)
        
        # use django's default storage backend to rename the file
        default_storage.save(new_file_path, default_storage.open(old_file_path))
        default_storage.delete(old_file_path)
        
        # update the file field to the new path
        self.upload.name = os.path.join('uploads/', new_name + extension)
        self.save()
        
    def __str__(self):
        #return os.path.splitext(self.upload.name)[0]
        return os.path.basename(os.path.splitext(self.upload.name)[0])
   
''' Employee Range: Store employee range values'''
class EmployeeCountScoring(models.Model):
    low_threshold = models.IntegerField()
    low_score = models.IntegerField(help_text="Score for companies Low employee count threshold or greater")
    
    mid_threshold = models.IntegerField()
    mid_score = models.IntegerField(help_text="Score for companies matching Mid employee count threshold or greater")
    
    high_threshold = models.IntegerField()
    high_score = models.IntegerField(help_text="Score for companies matching High employee count or greater")
    
''' Downloadable files'''
class FileDownload(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="file-downloads/")
    
    def __str__(self):
        return self.title