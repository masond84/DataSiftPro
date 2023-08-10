from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from .models import File, EmployeeCountScoring, FileDownload
from django.views.decorators.csrf import csrf_exempt
from .forms import FileForm, KeywordWeightForm, UploadFileForm
from django.http import FileResponse, Http404, JsonResponse, HttpResponseNotAllowed
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView
from django.core.files.storage import default_storage
from django.utils import timezone
from django.urls import reverse
# import additional modules
import pandas as pd
import os
import json
from os.path import basename
import csv
from datetime import datetime
from io import StringIO, BytesIO
import ast

# import scripts
from .ranking import rank_companies

# Create your views here.
''' Create Comment '''
class FileRenameView(UpdateView):
    model = File
    fields = ['name']
    template_name = 'cleaner/file_rename.html'
    
    def form_valid(self, form):
        # Get the file object
        file_obj = form.instance
        # Get the new name from the form
        new_name = form.cleaned_data['name']
        print(form.cleaned_data)
        # Call a custom method to handle the renaming
        file_obj.rename_file(new_name)
        
        # success message
        messages.success(self.request, "File was correctly renamed and saved.")
        
        url = reverse('cleaner:file_detail', args=[self.object.pk])
        return redirect(url)

#### Upload File ####
''' create comment '''
def upload_and_list_files(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.uploaded_at = timezone.now()
            new_file.upload = request.FILES['upload'] # Manually assign the file
            new_file.save()

            # Open the file and read it's contents
            try: 
                with new_file.upload.open('rb') as f:
                    if new_file.upload.name.endswith('.csv'):
                        df = pd.read_csv(f)
                    elif new_file.upload.name.endswith('.xlsx'):
                        df = pd.read_excel(f)
                    else:
                        return ValueError("Unsupported file format.")        
                # Add a success message after the data processing is done
                messages.success(request, "File uploaded and processed successfully!")
            except Exception as e:
                messages.error(request, f"Error processing file. Please upload a valid .csv or .xlsx file.")
                new_file.delete()
        else:  # Handle the error case if the form is not valid
            messages.error(request, "Error uploading file. Please try again.")
    else:
        form = UploadFileForm()
    
    # Always list the files whether it is a GET request or POST request
    # Get the file type filter from the URL parameters
    file_type_filter = request.GET.get('file_type', 'all')

    if file_type_filter == 'all':
        files_list = File.objects.all().order_by('uploaded_at')
    else:
        files_list = File.objects.filter(file_type=file_type_filter).order_by('uploaded_at')
    
    paginator = Paginator(files_list, 5)
    page = request.GET.get('page')
    files = paginator.get_page(page)
    
    for file in files:
        file.upload.name = basename(file.upload.name)

    return render(request, 'cleaner/uploads_files.html', {'form': form, 'files': files})

''' create comment '''
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save file to temporary location
            handle_uploaded_file(request.FILES['file'])
            # Read the file into a dataframe
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', request.FILES['file'].name)
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Please upload a .csv or .xlsx file.")

            # ADD ALGORITHM CODE TO PROCESS DATA BELOW 
            
            # Add a success message after the data processing is done
            messages.success(request, "File uploaded and processed successfully!")
    else:
        form = UploadFileForm()
    
    return render(request, 'cleaner/upload.html', {'form': form})

#### Upload File #####
''' create comment '''
def handle_uploaded_file(f):
    # Create 'media/temp' directory if not exsistant
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'uploads'), exist_ok=True)
    
    # Define the full file path
    full_path = os.path.join(settings.MEDIA_ROOT, 'uploads', f.name)
    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    # Create a new file object and save it
    new_file = File(upload=f)
    new_file.save()

#### Delete Files ####
def delete_file(request, file_id):
    file = File.objects.get(pk=file_id)
    file.delete()
    
    messages.success(request, "File deleted successfully")
    return redirect('cleaner:file_list')

#### Raname A File ####
def rename_file(request, pk):
    if request.method == "POST":
        new_name = request.POST.get('new_name')
        print(new_name)
        file = get_object_or_404(File, pk=pk)
        
        file.name = new_name
        file.save()
        print('saved file')
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})
    
#### Display File Contents ####
def file_detail(request, pk):
    # get the file object
    file = get_object_or_404(File, pk=pk)
    
    # open the file and read its contents
    with file.upload.open('rb') as f:
        file_extension = os.path.splitext(file.upload.name)[1].lower()
        # check what type of file
        if file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(f)
        elif file_extension == '.csv':
            df = pd.read_csv(f)
        else:
            raise ValueError("Unsupported file format. Please upload a .csv or .xlsx file.")
            
    # extract the file name
    base_name = os.path.basename(file.upload.name)
    # removed extension
    file_name, _ = os.path.splitext(base_name)
    # extract the file path
    file_path = os.path.join('uploads', os.path.basename(file.upload.name))
    
    # convert dataframe to Json format
    df_json = df.to_json(orient='records')
    return render(request, 'cleaner/file_detail.html', {'file': file, 'df': df_json, 'file_name': file_name, 'file_path': file_path})

## Save Files ##
def save_file_content(request):
    try: 
        data = json.loads(request.body)
        file_pk = data['file_pk']
        file = File.objects.get(pk=file_pk)  # Get the file object first

        updated_data = data['updated_data']
        headers = data['headers']
        
        updated_data = json.loads(updated_data)

        # convert the data to a dataframe
        df = pd.DataFrame(updated_data, columns=headers)
        
        # save the dataframe to the respective file type
        file_extension = os.path.splitext(file.upload.name)[1].lower()
        original_filename = file.upload.name  # Now, get the filename

        if file_extension == ".xlsx":
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False)
            writer.close() # Close the writer to flush the contents to the BytesIO object
            output.seek(0)
            content_file = ContentFile(output.read())
            file.upload.save(original_filename, content_file, save=True)
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif file_extension == ".csv":
            output = df.to_csv(index=False)
            mime_type = "text/csv"
        else:
            raise ValueError("Unsupported File Format")

        # Save the BytesIO object or string content as the file content
        file.upload.save(original_filename, ContentFile(output.getvalue() if file_extension == ".xlsx" else output), save=True)
        
        message = "The file was successfully saved and updated"
        return JsonResponse({'success': True, 'message': message})
    except Exception as e:
        print(str(e))
        message = f"Error saving file: {str(e)}"
        return JsonResponse({'success': False, 'message': message})
    
## Download Files ##
def download_files(request, file_name):
    # Build the file path
    #file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    # check if the file exsists
    if os.path.exists(file_path):
        # return the file as response
        return FileResponse(open(file_path, 'rb'), content_type='application/vnd.ms-excel')
    else:
        raise Http404("File does not exist.")

def download_algorithms(request, file_id):
    algorithm = FileDownload.objects.get(id=file_id)
    file_path = algorithm.file.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{algorithm.file.name}"'
    
    return response    

## Algorithms Page ##
# Display Available Algorithms
def algorithms(request):
    
    return render(request, "cleaner/algorithms.html")

# Run Company Ranking Algorithm
def run_script_1(request):
    print('Run Script function running')
    if request.method == "POST":
        print(f"Recieved POST request: {request.POST} ")
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            filepath = form.cleaned_data['filepath'].upload.path
            keyword_file = form.cleaned_data['keyword_file'].upload.path
            #name_keyword_file = form.cleaned_data['name_keyword_file'].upload.path
            
            # Process Employee Range
            if form.cleaned_data['employee_range_file']:
                employee_range_file_path = form.cleaned_data['employee_range_file'].upload.path
                # Read the file and save values to the EmployeeRange model
                # implement reading the file and extracting values here
            elif form.cleaned_data['low_score'] and form.cleaned_data['mid_score'] and form.cleaned_data['high_score']:
                EmployeeCountScoring.objects.create(
                    low_threshold=form.cleaned_data['low_threshold'],
                    mid_threshold=form.cleaned_data['mid_threshold'],
                    high_threshold=form.cleaned_data['high_threshold'],
                    low_score=form.cleaned_data['low_score'],
                    mid_score=form.cleaned_data['mid_score'],
                    high_score=form.cleaned_data['high_score']
                )
                
            # If the user does not provide the slider values or employee_range_files
            if not all([form.cleaned_data.get('low_threshold'), form.cleaned_data.get('mid_threshold'), form.cleaned_data.get('high_threshold')]):
                # Default logic
                print("Running Default Logic")
                thresholds = [200, 50, 0]
                scores = [100, 50, 25]
            else:
                print("Running User Logic")
                # Extracting thresholds and scores 
                thresholds = [
                    form.cleaned_data['high_threshold'],
                    form.cleaned_data['mid_threshold'],
                    form.cleaned_data['low_threshold'],
                ]
                scores = [
                    form.cleaned_data['high_score'],
                    form.cleaned_data['mid_score'],
                    form.cleaned_data['low_score'],
                ]
                
                thresholds, scores = zip(*sorted(zip(thresholds, scores), reverse=True))
                
            print("Threshold 1:", form.cleaned_data['low_threshold'])
            print("Slider 1 (Score):", form.cleaned_data['low_score'])
            print("Threshold 2:", form.cleaned_data['mid_threshold'])
            print("Slider 2 (Score):", form.cleaned_data['mid_score'])
            print("Threshold 3:", form.cleaned_data['high_threshold'])
            print("Slider 3 (Score):", form.cleaned_data['high_score'])
            #
            rank_companies(filepath, keyword_file, thresholds, scores)
            print("Rank companies function executed")
            # Read the updated Excel File into a pandas dataframe
            df = pd.read_excel(filepath)
            print("Read excel file into dataframe")
            # Convert the dataframe into JSON
            data_json = df.to_json(orient="records")
            
            return render(request, "cleaner/results.html", {'data': data_json, 'file_path': filepath})
        else:
            print(f"Form is not valid: {form.errors}")
    else:
        print("Not a POST request")
        form = FileForm()
    return render(request, 'cleaner/form.html', {'form': form})

''' Keyword Page '''
# Handle Keyword and Weight Input
def add_keywords_weights(request):
    if 'keywords' not in request.session:
        request.session['keywords'] = {}
    
    if request.method == "POST":
        form = KeywordWeightForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            weight = form.cleaned_data['weight']
            
            # check if the keyword already exsists
            existing_keyword = next((key for key in request.session['keywords'] if key.lower() == keyword.lower()), None)
            
            # If the keyword already exsists delete it
            if existing_keyword:
                del request.session['keywords'][existing_keyword]
                
            request.session['keywords'][keyword] = weight
            request.session.modified = True
            form = KeywordWeightForm()
            
        # Handle updated table data from Handsontable
        table_data_json = request.POST.get('table_data', None)
        if table_data_json:
            table_data = json.loads(table_data_json)
            request.session['keywords'] = {row[0]: float(row[1]) for row in table_data}
            request.session.modified = True
            return JsonResponse({'status': 'success'})
    else:
        form = KeywordWeightForm()
        
    return render(request, 'cleaner/add_keywords.html', {'form': form, 'keywords':request.session['keywords'].items()})

# Save Keyword Table and File
def save_keywords(request):
    # Generate a unique filename using a timestamp
    # Grab the user-provided filename from the POST data, or use a default pattern if not provided
    user_filename = request.POST.get('filename', '') # Added code
    if user_filename:
        filename = user_filename + '.csv' # Modified code
    else:
        filename = 'keywords_' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
    # Grab keywords from the current session
    keywords = request.session['keywords']
    
    # Create CSV content
    response_content = StringIO() # Note the corrected variable name
    writer = csv.writer(response_content)
    writer.writerow(['Keyword', 'Weight'])
    for keyword, weight in keywords.items():
        writer.writerow([keyword, weight])
    
    # Create the file content
    file_content = ContentFile(response_content.getvalue().encode(), filename)
    
    # Save the CSV file to a file object using UploadFileForm
    file_form = UploadFileForm({
        'file_type': 'keyword'
    }, {
        'upload': file_content
    })
    
    # Save the CSV file to a file object using UploadFileForm
    #file_form = UploadFileForm(files={'file': ContentFile(response_content.getvalue().encode(), filename)})
    
    if file_form.is_valid():
        uploaded_file = File(upload=file_form.cleaned_data['upload'], file_type='keyword')
        uploaded_file.save()
        messages.success(request, "File saved successfully")
    else:
        messages.error(request, "There was an error saving the file.")
        
    # Clear the keywords from the session
    request.session['keywords'] = {}
    request.session.modified = True
    
    # Redirect to the file list view
    return redirect('cleaner:file_list')
    
def clear_keywords(request):
    request.session['keywords'] = {}
    request.session.modified = True
    return JsonResponse({'status': 'success'})