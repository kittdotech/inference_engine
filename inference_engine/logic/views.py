from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import load_workbook
from django.conf import  settings
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
print settings.PROJECT_ROOT
wb2 = load_workbook(os.path.join(settings.PROJECT_ROOT, 'temp.xlsx'))
ws = wb2.worksheets[0]
sent_num2=1
# Create your views here.
def index(request):
    #return HttpResponse('Welcome to Django')
    return render(request,'logic/index.html')

def replace_relations(rule2,sent_num,parsed_str1):
    """Replca Function"""
    parsed_str=""
    for each_word in parsed_str1.split():
        for row in ws.rows:
            val = row[1].value
            if each_word == row[1].value:
                if row[0].value == 'r':
                    parsed_str += row[2].value + " "
                else:
                    parsed_str += row[1].value + " "
    return parsed_str

#def replace_nouns(rule2,sent_num,parsed_str1)


def generate(request):
    print request


    str1=request.GET['basestr']
    parsed_str1= str1.split(' ')
    rule = request.GET['rule']
    print parsed_str1
    rule2 = rule.split(' ')
    sent_num = rule2[1]
    rule2 = rule2[0]

    if rule2 == 'rl':
        resultstr = replace_relations(rule2,sent_num,str1)


    parsed_str1= str1.split(' ')
    print parsed_str1




    #str1 = "(" + str1 + ")"

    parsed_str=""
    #parsed_str_list=[]
    lat_var = [ chr(98+i) for i in range(25)]
    idf_var = [ chr(98+i) + "'" for i in range(25)]

    print parsed_str

    data={'resultstr':resultstr,'status':True}
    data = json.dumps(data,cls=DjangoJSONEncoder)
    return HttpResponse(data,content_type="application/json")