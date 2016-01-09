from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import load_workbook
from django.conf import  settings
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
print settings.PROJECT_ROOT
import copy

wb2 = load_workbook(os.path.join(settings.PROJECT_ROOT, 'temp.xlsx'))

cond_r = unichr(8835)
top = unichr(8868)
bottom = unichr(8869)
neg = unichr(172)
alpha = unichr(945)
beta = unichr(946)
iff = unichr(8801)
mini_c = unichr(8658)
mini_e = unichr(8703)
implies = unichr(8866)
conditional = unichr(8594)
nonsequitur = unichr(8876)
xorr = unichr(8891)
idisj = unichr(8744)
cj = unichr(8896)
implication = False
impl = ""


def remove_outer_paren(str1):
    j = 0
    for i in range(0, len(str1)):
        str2 = str1[i:i + 1]
        if str2 == "(":
            j += 1
        elif str2 == ")":
            j -= 1
        if j == 0 and i + 1 != len(str1):
            break
        elif j == 0 and i + 1 == len(str1):
            str1 = str1[1:len(str1) - 1]
    return str1


def remove_redundant_paren(str1):
    j = 0
    str2 = str1[:2]
    str3 = str1[2:]
    if str2 == '((' and str3 == '))':

        for i in range(0, len(str1)):
            str2 = str1[i:i + 1]
            if str2 == "(":
                j += 1
            elif str2 == ")":
                j -= 1
            if j == 1 and i + 1 != len(str1):
                break
            elif j == 0 and i + 1 == len(str1):
                str1 = str1[1:len(str1) - 1]
    return str1


def mainconn(str1):
    # str_main = str_main.replace(implies,"&")
    # str_main = str_main.replace(nonsequitur, "&")
    # str_main = str_main.replace("~","")
    # str_main = str_main.replace(" ", "")

    if os(str1):
        return ["", 0]

    if str1.find("&") < -1 and str1.find(idisj) < -1 and str1.find(iff) < -1 and str1.find(conditional) < -1 and \
            str1.find(implies) < -1 and str1.find(nonsequitur) < -1 and str1.find(xorr) < -1:
        return

    # arr1 = [ 0 for row in range(6)]
    # arr2 = [ 0 for row in range(6)]

    str3 = str1
    j = 0
    # zzz
    for i in range(0, len(str1)):
        str2 = str1[i:i + 1]
        if str2 == "(":
            j += 1
        elif str2 == ")":
            j -= 1

        if j == 0 and i + 1 != len(str1):
            break
        elif j == 0 and i + 1 == len(str1):
            str1 = str1[1:len(str1) - 1]

    j = -1

    for i in range(0, len(str1)):
        str2 = str1[i:i + 1]
        if str2 == conditional:
            f = -1
        if str2 == idisj or str2 == "&" or str2 == iff or str2 == implies or \
                str2 == nonsequitur or str2 == conditional or str2 == xorr:
            if str3 != str2 and str3 != "":
                j = j + 1

            str3 = str2

    if j == -1:
        mainconn = [str3, i]
        return mainconn
    k = -1
    j = -1
    while True:
        k += 1
        if k > 150:
            break
        for i in range(0, len(str1)):
            str2 = str1[i:i + 1]

            if str2 == "(":
                j += 1
            elif str2 == ")":
                j -= 1

            if j == -1 and (str2 == idisj or str2 == "&" or str2 == iff or str2 == implies
                            or str2 == nonsequitur or str2 == conditional or str2 == xorr):
                list1 = [str2, i]
                mainconn = [str2, i]
                return mainconn


def isvariable(str3):

    if str3 != "":
        str3 = str3.replace("'", "")
        str3 = str3.replace(neg, "")
        if len(str3) == 1:
            bool2 = True
        else:
            bool2 = False
    isvariable = bool2
    return isvariable


def os(str):
    cnx = [xorr, iff, idisj, conditional, implies, nonsequitur, "&"]
    for i in range(0, len(cnx)):
        if str.find(cnx[i]) > -1:
            os = False
            return os
    os = True
    return os


def find_sentences(instring):

    str2 = ""
    marker = False
    n = -1
    il = -1
    total = -1
    c = -1
    neg_value = []
    str1 = ""
    sent1 = []
    sent_type2 = []
    wneg = []
    output = [0, 1, 2, 3, 4, 5, 6]
    # the skel name list names each single sentence after a greek letter, even if
    # the same sentence appears twice it obtains a different name on the second
    # appearance
    skel_nam = []
    skel_nam2 = {}
    q = []
    skel_string = instring
    bool1 = False
    bool2 = False
    p = 947
    res = ""
    temp_string = ""
    connectives = ["&", idisj, iff, conditional, nonsequitur, implies]
    arr1 = []
    cond_r2 = cond_r + neg
    instring2 = copy.copy(instring)
    instring = instring.strip()
    grandparent_type = mainconn(instring)

    if instring.find("~(") > -1:
        instring = instring.replace("~(", "(!")
    if instring.find(implies) > -1:
        str2 = implies
    elif instring.find(nonsequitur) > -1:
        str2 = nonsequitur

    if os(instring) == False:
        temp_string = mainconn(instring)

        if instring.find(implies) > -1:
            str1 = implies
        elif instring.find(nonsequitur) > -1:
            str1 = nonsequitur
        else:
            if temp_string == iff:
                str1 = "bicond"
            elif temp_string == conditional:
                str1 = "cond"
            elif temp_string == "&":
                str1 = "cj"

        sent1.append(instring)
        neg_value.append("")
        sent_type2.append(str1)
        wneg.append(instring)

    # elif os(instring):
        # otemp_sent = instring
        #
        # sent1 = [0 for row in range(3)]
        # neg_value = [0 for row in range(3)]
        # sent_type2 = [0 for row in range(3)]
        # sent_type2[2] = "cj"
        # wneg = [0 for row in range(3)]
        #
        # if instring.find("~") > -1 or instring.find(cond_r2) > -1:
        #     instring = instring.replace("~", "")
        #     instring = instring.replace(cond_r2, cond_r)
        #     neg_value[2] = "~"
        # else:
        #     neg_value[2] = ""
        #
        # sent1[2] = instring
        #
        #
        # wneg[2] = otemp_sent
        # output[1] = sent1
        # output[2] = neg_value
        # output[3] = sent_type2
        # output[4] = wneg
        # find_sentences_complex = output
        # return find_sentences_complex

    #children = [[[ 0 for row in range(3)] for row1 in range(11)] for row2 in range(11)]

    j = -1
    for i in range(0, len(instring)):
        str1 = instring[i:(i + 1)]
        for o in connectives:
            if str1 == o:
                j += 1

    while n <= j + 1:

        il += 1
        if il > 15:
            break

        no_conn = True
        e = 0
        l = len(instring)
        x = -1
        while x < l - 1:
            x += 1
            temp_string = instring[x: x + 1]
            if instring[x: x + 1] == "(":

                if marker == False:
                    z = x
                    marker = True

                total += 1
            elif instring[x: x + 1] == ")":
                total -= 1
                if total == -1:
                    marker = False
                    e += 1
                    c += 1

                    temp_sent = instring[z: x + 1]
                    #temp_sent = remove_outer_paren(temp_sent)
                    otemp_sent = copy.copy(temp_sent)

                    if (len(instring) - len(temp_sent)) > 2:

                        if os(temp_sent):
                            if temp_sent.find("~") > -1:
                                neg_value.append("~")
                                temp_sent = temp_sent.replace("~", "")

                            elif temp_sent.find(cond_r2) > -1:
                                neg_value.append("~")
                                temp_sent = temp_sent.replace(cond_r2, cond_r)

                            elif temp_sent.find(cond_r2) == -1 and temp_sent.find(cond_r) > -1:
                                neg_value.append("")
                            elif temp_sent.find("~") == -1:
                                neg_value.append("")
                            else:
                                break  # stop

                        result = mainconn(temp_sent)
                        temp_mc = result[0]
                        result = mainconn(instring)
                        parent_type = result[0]

                        if z > instring2.find(str2) and str2 != "":
                            n = n + 1
                            res = "consq"

                        elif grandparent_type == "&" and parent_type == "&":
                            if temp_mc == "":
                                res = "cj"
                                n = n + 1

                            elif temp_mc == conditional:
                                res = "cond"

                            elif temp_mc == iff:
                                res = "bicond"
                            elif temp_mc == idisj:
                                res = "disj"

                        elif parent_type == conditional or parent_type == iff or grandparent_type == conditional or grandparent_type == iff:
                            if temp_mc == "":
                                n = n + 1
                                if parent_type == iff:
                                    if bool1:
                                        res = "bic2"
                                    else:
                                        res = "bic1"

                                    bool1 = True
                                elif parent_type == idisj:
                                    if bool1:
                                        res = "disjc2"
                                    else:
                                        res = "disjc1"

                                    bool1 = True

                                elif instring2.find(otemp_sent) < instring2.find(conditional):
                                    if bool1:
                                        res = "ant2"
                                    else:
                                        res = "ant"

                                    bool1 = True
                                else:
                                    if bool2:
                                        res = "cons2"
                                    else:
                                        res = "cons"

                                    bool2 = True

                            elif temp_mc == conditional:
                                res = "cond"
                            elif temp_mc == iff:
                                res = "bicond"

                        elif z < instring2.find(str2) and str2 != "":
                            res = "ncj"
                            n = n + 1
                        else:
                            res = "ncj"
                            n = n + 1

                        # if temp_sent == "(z'Ax')":
                        #     pp = 7
                        sent1.append(temp_sent)
                        sent_type2.append(res)
                        wneg.append(otemp_sent)

                        if os(otemp_sent):
                            p += 1
                            skel_string = skel_string.replace(
                                otemp_sent, unichr(p))
                            q = [otemp_sent, unichr(p)]
                            skel_nam.append(q)
                            # skel_nam2[otemp_sent] = unichr(p)
                        else:
                            skel_nam.append("")

                        # if k > 0:
                        #     m += 1
                            # children[k][m][0] = temp_sent
                            # children[k][m][1] = neg_value[c]

                    else:
                        instring = instring[1:len(instring) - 1]
                        l = len(instring)
                        x = -1
                        c -= - 1
                        e -= - 1

        total = -1
        marker = False
        w = -1

        if n < j + 1:
            if len(sent1) > w and parent_type != implies and parent_type != nonsequitur:
                while w < len(sent1):
                    w += 1
                    str21 = sent1[w]
                    if not os(str21) and w != 0:
                        if str21 not in arr1:
                            bool1 = False
                            bool2 = False
                            instring = str21
                            k = w
                            arr1.append(instring)
                            break

            main_sent = False

    for i in range(0, len(sent1)):
        # if os(sent1(i)) == False:
        #     str1 = wneg[i]
        #     str2 = str1.replace("~", "")
        #     str2 = str2.repalce(cond_r2, cond_r)
        #     wneg[i] = str2

        temp_string = sent1[i]
        if temp_string.find("!") > -1:
            sent1[i] = sent1[i].replace("(!", "~(")
            wneg[i] = wneg[i].replace("(!", "~(")

    output[0] = sent1
    output[1] = neg_value
    output[2] = sent_type2
    output[3] = wneg
    # output[4] = children
    output[5] = skel_string
    output[6] = skel_nam

    find_sentences = output
    return find_sentences


def categorize_words(list1):
    word_types = []
    for i in list1:
        str9 = i
        dict_cat = ""
        list_cat = words.keys()
        for key, value in words.iteritems():

            if type(value) == type([]):
                if str9 in value:
                    dict_cat = key
                    break
            elif type(value) == type({}):
                if str9 in value.keys():
                    dict_cat = key
                    break

        word_types.append([str9, dict_cat])

    list1_cat = [None] * 12
    relation_type = ' '

    for item in word_types:
        key = item[0]
        value = item[1]
        if value == 'r':
            relation_type = 'r'
            list1_cat[2] = key
        elif value == 'sr':
            relation_type = 'sr'
            list1_cat[5] = key
        elif value == 'tr':
            relation_type = 'tr'
            list1_cat[8] = key
        elif value == 'd' and relation_type == ' ':
            list1_cat[0] = key
        elif value == 'n' and relation_type == ' ':
            list1_cat[1] = key
        elif value == 'd' and relation_type == 'r':
            list1_cat[3] = key
        elif value == 'n' and relation_type == 'r':
            list1_cat[4] = key
        elif value == 'd' and relation_type == 'sr':
            list1_cat[6] = key
        elif value == 'n' and relation_type == 'sr':
            list1_cat[7] = key
        elif value == 'd' and relation_type == 'tr':
            list1_cat[9] = key
        elif value == 'n' and relation_type == 'tr':
            list1_cat[10] = key

    return list1_cat


def word_sub(list2, def_var, dv_nam):

    num = [1, 4, 7, 10]
    for i in num:
        if list2[i] and isvariable(list2[i]) == False:
            temp_list = [def_var[0], list2[i]]
            list2[i] = def_var[0]
            del def_var[0]
            dv_nam.append(temp_list)
    return list2

def idf_elim(list1, idf_var):

    temp_list = [None] * 10
    num = [0, 3, 6, 9]
    for i in num:
        if list1[i] == 'a' or list1[i] == 'some':
            temp_list[1] = idf_var[0]
            temp_list[2] = 'IG'
            temp_list[4] = list1[i + 1]
            list1[i] = None
            list1[i + 1] = idf_var[0]
            tot_sent.append(temp_list)
            del idf_var[0]
    list2 = [temp_list, list1]

    return list2


def def_elim(list1, def_var):

    temp_list = [None] * 10
    num = [0, 3, 6, 9]
    for i in num:
        if list1[i] == 'the':
            temp_list[1] = def_var[0]
            temp_list[2] = 'IG'
            temp_list[4] = list1[i + 1]
            list1[i] = None
            list1[i + 1] = def_var[0]
            tot_sent.append(temp_list)
            del def_var[0]
    list2 = [temp_list, list1]

    return list2


def insert_space(str, integer):
    return str[0:integer] + ' ' + str[integer:]


def sp_def(str1):
    # this function place a space between variables and relations
    # so as to make it easier to categorize words in a sentence
    str1 = str1.replace("~", " ~ ")
    i = 0
    while i + 1 < len(str1):
        i += 1
        temp_str = str1[i:(i + 1)]
        nxt_str = str1[(i + 1):(i + 2)]
        if nxt_str.isupper() == True and temp_str.islower() == True:
            str1 = insert_space(str1, i + 1)
        elif nxt_str.islower() == True and temp_str.isupper() == True:
            str1 = insert_space(str1, i + 1)
        elif temp_str == "'" and nxt_str.isupper() == True:
            str1 = insert_space(str1, i + 1)
    return str1


def id_def(str1):
    # this function picks out that variables in the id sentences of the
    # definition

    b = str1.find('|')
    str4 = str1[b + 1:]
    str4.lstrip()
    str1 = str1[0:b - 1]
    str1.rstrip()
    id_sent = []
    id_sent2 = []
    beg = 0
    for i in range(0, len(str1)):
        temp_str = str1[i:(i + 1)]
        if temp_str == "," or i == len(str1) - 1:
            str2 = str1[beg:i + 1]
            str2 = str2.replace(",", "")
            beg = i + 1
            id_sent.append(str2)

    for i in range(0, len(id_sent)):
        temp_str = id_sent[i]
        b = temp_str.find('=')
        str2 = temp_str[:b]
        str3 = temp_str[b + 1:]
        temp_list = [str2, str3]
        id_sent2.append(temp_list)

    id_sent2.insert(0, str4)
    return id_sent2

def build_sent(list1):

    str1 = "("
    for i in range(0, len(list1)):
        temp_str = list1[i]
        if temp_str != None:
            str1 = str1 + temp_str + ' '

    return str1 + ")"

def dfn_rn(sent, idf_var, def_var, dv_nam):

    return

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
                if row[0].value == 'r' or row[0].value == 'sr' or row[0].value == 'tr':
                    parsed_str += row[2].value + " "
                else:
                    parsed_str += row[1].value + " "
    return parsed_str

#def replace_nouns(rule2,sent_num,parsed_str1)




def generate(request):
    print request
    tot_sent = request.session.get('tot_sent',[])
    idf_var = [chr(122 - i) for i in range(25)]
    def_var = [chr(98 + i) + "'" for i in range(25)]
    dv_nam = []
    str1=request.GET['basestr']
    parsed_str1 = str1.split(' ')
    rule = request.GET['rule']
    print parsed_str1
    rule2 = rule.split(' ')
    sent_num = rule2[1]
    rule2 = rule2[0]
    list1 = categorize_words(parsed_str1)
    #tot_sent.append(list1)

    # if request.session.get('sample',0):
    #     sam1= request.session['sample']
    # else:
    #     request.session['sample']=[1,2]


    if rule2 == 'rl':
        resultstr = replace_relations(rule2,sent_num,str1)
        tot_sent.append(resultstr)
        request.session['tot_sent']=tot_sent
    elif rule2 == 'WS':

        temp_list = word_sub(list1,def_var,dv_nam)
        resultstr = build_sent(temp_list)
        tot_sent.append(resultstr)
        request.session['tot_sent']=tot_sent

    elif rule2 == 'dfd a' or 'dfd some':
        temp_list = idf_elim(list1, idf_var)
        str1 = build_sent(temp_list[0])
        str2 = build_sent(temp_list[1])
        resultstr = str1 + ' & ' + str2



    parsed_str1= str1.split(' ')
    print parsed_str1
    parsed_str=""
    print parsed_str
    data={'resultstr':resultstr,'status':True}
    data = json.dumps(data,cls=DjangoJSONEncoder)
    return HttpResponse(data,content_type="application/json")


str1 = 'g'

sent_num2=1
# Create your views here.

idf_var = [chr(122 - i) for i in range(25)]
def_var = [chr(98 + i) + "'" for i in range(25)]

ws = wb2.worksheets[0]
words = {'r': {}, 'n': [], 'd': [], 'sr': {}, 'tr': {}}

temp_list = []
category = ['r', 'sr', 'tr']
for row in ws.rows:
    str1 = row[0].value
    str2 = row[1].value
    str12 = row[2].value
    if row[0].value in category:
        if row[2].value in words[row[0].value].keys():
            words[row[0].value][row[2].value].append(row[1].value)
        else:
            words[row[0].value][row[2].value] = [row[1].value]
    else:
        words[row[0].value].append(row[1].value)


# str1 = "(pOC) " + iff +  " ((z'APy' Tx') & (w'Sv' Tu') & (w'CRSz') & \
# (u'SUTx') & (p-(w'Rt')) & (pAAb Tu') & (~pAAb Tx'))"
#str1 = "(b~IGc) " + iff + " ((z'Ab) & (bAy') & (gIG~b) & (((x'Ay') & (z'Ax')) " + conditional + " (x'=b)))"

str1 = u'''z'=moment, y'=individual | (bIGz') ''' + iff + ''' ((cAb) & (bAd) & (bIGy') & (((eAd) & \
(cAe)) ''' + conditional + ''' (e=b)))'''



new_ids = id_def(str1)
new_def = new_ids[0]
del new_ids[0]


sent_info = find_sentences(str1)


str8 = 'some matter EX IN space'
str9 = 'the moment MV TRG time'

#str8 = word_sub(list2,def_var,dv_nam,tot_sent)

list1 = str8.split(' ')
list1a = str9.split(' ')
list2 = categorize_words(list1)
list2a = categorize_words(list1a)
tot_sent = []
dv_nam = []
tot_sent.append(list2)
tot_sent.append(list2a)
temp_str = copy.copy(tot_sent[1])
tot_sent.append(temp_str)

#tot_sent = word_sub(list2, def_var, dv_nam, tot_sent)

temp_str = copy.copy(tot_sent[2])
tot_sent.append(temp_str)

# tot_sent = def_elim(tot_sent, def_var)

sent_info = dfn_rn(sent_info, idf_var, def_var, dv_nam)


pp = 7

# some d EX IN e