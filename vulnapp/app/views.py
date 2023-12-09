import os
import subprocess
import platform
import bleach

# myapp/views.py
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.http import HttpResponse

from .models import BoardPost

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class BoardPostsListView(ListView):
    model = BoardPost
    paginate_by = 100

class BoardPostsCreateView(LoginRequiredMixin, CreateView):
    model = BoardPost
    fields = ["image", "content"]
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        # Set the owner of the model instance to the current user
        form.instance.owner = self.request.user
        form.instance.content = bleach.clean(form.instance.content)
        return super().form_valid(form)

class BoardPostsDeleteView(LoginRequiredMixin, DeleteView):
    model = BoardPost
    success_url = reverse_lazy("main")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise HttpResponse("You are not the owner", status=403)
        return super().dispatch(request, *args, **kwargs)

def run_exiftool(file_path):
    if platform.system() == "Windows":
        # Assuming exiftool.exe is in the same directory as your script
        exiftool_command = ["exiftool.exe", file_path]
    else:
        # Assuming exiftool is in the system's PATH
        exiftool_command = ["exiftool", file_path]

    try:
        result = subprocess.run(
            exiftool_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Error: {e.stderr}"

    return output

def get_exif_data(request, file_name):
    image_found_in_db = BoardPost.objects.filter(image='user_uploads/'+file_name).first()
    if not image_found_in_db:
        return HttpResponse("Filename not allowed", status=403)

    file_path = os.path.abspath(os.path.join('user_uploads/', file_name))
    result_output = run_exiftool(file_path)
    return HttpResponse(result_output, content_type='text/plain')

def read_file_view(request, file_name):
    image_found_in_db = BoardPost.objects.filter(image='user_uploads/'+file_name).first()
    if not image_found_in_db:
        return HttpResponse("Filename not allowed", status=403)

    # Assuming the files are stored in a specific directory, adjust the path accordingly
    file_path = os.path.join('user_uploads/', file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        return HttpResponse("File not found", status=404)

    # Open and read the file content
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # You can customize the response content type based on the file type
    response = HttpResponse(file_content, content_type='text/plain')

    # Optionally, you can set the Content-Disposition header to suggest a filename
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response
