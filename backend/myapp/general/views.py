from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import FileResponse


from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import base64
from general.util.helper import *
from general.util.constant import *

import csv
from pprint import pprint
# Create your views here.

@api_view([GET,POST])
def method(request):
    if request.method == GET:
        print(request)
        return Response("Hello From Method GET")
    if request.method == POST:
        print(request)
        return Response("Hello From Method POST") 
    return


@api_view(['POST'])
def get_csv(request:Request):

    data = json.loads(request.body)
    schemas = json.loads(data['schemas'])
    array_pdf = json.loads(data['pdfs'])
    csv_file_name = main_v1(schemas,array_pdf)
    # print(type(schemas))
    # pprint(schemas)
    # pprint(schemas[0]['Name'])
    # pprint(pdf)
    # print(type(pdf))
    print("done")

    csv_file = open(csv_file_name, 'rb')
    response = FileResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'
    return response
    # return Response("DOG",status=status.HTTP_201_CREATED)

@api_view(['POST'])
def get_ocr(request:Request):
    return Response("DOG")

@api_view(['GET'])
def health_check(request):
    return Response("Hello, world. You're at the polls index.")

# @api_view(['GET'])
# def export_csv(request):
#     # Your data
#     raw_data = [
#         ['พงศธร อินตะนัย 6310503448', 'วันนึกินอะไรดี', 'กะเพรา'],
#         ['-', '-', 'พริก'],
#         ['-', '-', 'ผักบั้ง']
#     ]
    
#     # Create an HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="data.csv"'
    
#     # Create a csv writer
#     writer = csv.writer(response, csv.excel)
    
#     # Write your data to the CSV writer
#     for row in raw_data:
#         writer.writerow(row)

#     # return Response(data=response,status= status.HTTP_200_OK)
#     return response