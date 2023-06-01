from django.shortcuts import render
from .models import Breed, Uploads
from django.core.files.storage import FileSystemStorage
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from CowBreedClassifier.settings import BASE_DIR, TESTING_MODEL
from .serializers import BreedSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib import messages
from .run_model import predict_image
from django.template.defaulttags import register

breeds = {'GIR':3, 'RATHI':6, 'SHAIWAL':2, 'RED SINDHI': 1}

@register.filter(name='split')
def split(value, key):
    return value.split(key)


def home(request):
    breeds = Breed.objects.all()[:6]
    return render(request, 'index.html', {'breeds':breeds})

def search_list(request, **kwargs):
    context = {}
    breed = Breed.objects.all()
    context['search_for'] = ''
    if request.GET.get('search'):
        breed = Breed.objects.filter(name__istartswith = request.GET.get('search'))
        context['search_for'] = request.GET.get('search')

    try:
        p = Paginator(breed, 3)
        try:
            context['page_obj'] = p.get_page(kwargs.get('page_number'))
        except PageNotAnInteger:
            context['page_obj'] = p.page(1)
        except EmptyPage:
            context['page_obj'] = p.page(p.num_pages)
    except:
        context['page_obj'] = {'object_list':[]}
    return render(request, 'search-list.html', context)

@csrf_exempt
def upload_details(request, **kwargs):
    context = {}
    if request.POST:
        img = request.FILES.get('select-image')
        img_name = img.name.split('.')
        if len(img_name) < 2 or (img_name[-1] not in ['jpeg','png','jpg']):
            messages.error(request,"Please upload image with extension JPG, JPEG or PNG!")
            return render(request, 'upload-details.html', context)
            
        # fs = FileSystemStorage()
        # file = fs.save(img.name, img)
        # fileurl = fs.url(file)

        fileurl = Uploads.objects.create(photo=img)
        breed_name = predict_image(str(BASE_DIR)+fileurl.photo.url, TESTING_MODEL)
        print(breed_name)
        # print(fileurl.photo.url)
        context['breed'] = Breed.objects.get(id=breeds[breed_name])
        context['image_url'] = fileurl
        # print(context['image_url'])
        messages.success(request, "Breed classification successful")
    else:
        if kwargs.get('detail'):
            try:
                context['breed'] = Breed.objects.get(id=kwargs.get('detail'))
                messages.success(request, "Breed details are listed below!")
            except:
                messages.error(request,"Unable identify the breed!")
            
    return render(request, 'upload-details.html', context)

def about(request):
    return render(request, 'about.html')

@api_view(['GET'])
def list_api(request):
    breeds = Breed.objects.all()
    serializer = BreedSerializer(breeds, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def retrieve_api(request, **kwargs):
    try:
        breed = Breed.objects.get(id=kwargs.get('breed_id'))
    except Breed.DoesNotExist:
        return Response({"message":"No data found with the given ID: "+str(kwargs.get('breed_id'))})

    serializer = BreedSerializer(breed)    
    return Response(serializer.data)