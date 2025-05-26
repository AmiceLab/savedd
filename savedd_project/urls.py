from django.contrib import admin
from django.urls import path
from read_analysis.views import ocr_view, upload_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('read_analysis/', ocr_view, name='ocr_view'),
    path('', ocr_view, name='ocr_view'),
    
    # try with chatgpt -- another new upload page 9 Mar 2025
    path("upload_image/", upload_image, name="upload_image"),
]
