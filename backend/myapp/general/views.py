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
from django.http import JsonResponse
import os
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

    # v2
    # data = json.loads(request.body)
    # schemas = json.loads(data['schemas'])
    # array_pdf = json.loads(data['pdfs'])
    # csv_file_name, data_with_accuracy = main_v1(schemas,array_pdf)
    # # print(type(schemas))
    # # pprint(schemas)
    # # pprint(schemas[0]['Name'])
    # # pprint(pdf)
    # # print(type(pdf))
    # print("done")

    # csv_file = open(csv_file_name, 'rb')
    # response = FileResponse(csv_file, content_type='text/csv')
    # response['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'
    # return response
    # return Response("DOG",status=status.HTTP_201_CREATED)

    #v3 
    data = json.loads(request.body)
    schemas = json.loads(data['schemas'])
    array_pdf = json.loads(data['pdfs'])
    csv_file_name, data_with_accuracy = main_v1(schemas,array_pdf)
    print("done")

    # Read the CSV file and convert it to a base64 string
    with open(csv_file_name, 'rb') as csv_file:
        base64_csv = base64.b64encode(csv_file.read()).decode()

    # Create a dictionary that contains both data_with_accuracy and the base64 CSV string
    response_data = {
        'data_with_accuracy': data_with_accuracy,
        'csv_file': base64_csv,
        'csv_file_name': os.path.basename(csv_file_name)
    }

    # Convert the dictionary to a JSON response
    return JsonResponse(response_data)

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