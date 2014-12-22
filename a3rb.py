__author__ = 'd7eame'
# -*- coding: utf-8 -*-
import re

def createRegex(identifiers):
    expression = ''
    for i in range(len(identifiers)):
        if i < (len(identifiers) - 1):
            expression += identifiers[i]+'|'
        else:
            expression += identifiers[i]
    return expression

def cleanword(word):
    word = re.sub('\u0640','',word) #removes tatweel(kashidah)
    word = re.sub('\u064b','',word) #removes FATHATAN
    word = re.sub('\u064c','',word) #removes DAMMATAN
    word = re.sub('\u064d','',word) #removes KASRATAN
    word = re.sub('\u064e','',word) #removes FATHA
    word = re.sub('\u064f','',word) #removes DAMMA
    word = re.sub('\u0650','',word) #removes KASRA
    word = re.sub('\u0651','',word) #removes SHADDA
    word = re.sub('\u0652','',word) #removes SUKUN
    if len(word) > 5:
        if word.startswith('ال') or word.startswith('لل'): 
            word = word[2:] #istrp not appropriate here
        elif word.startswith('كال') or word.startswith('بال') or word.startswith('وال') or word.startswith('فال'): 
            word = word[3:]
    return word

def sortwords(words):
    words = list(set(words)) #removes duplicate words
    print(len(words))
    for i in range(len(words)):
        words[i] = cleanword(words[i])
    words = list(set(words))
    print(len(words))
    return words

def ennafunc(enna, kind):
    num = 0
    output = open('Arabic/outputs/'+kind+'.txt', 'w')
    for i in range(len(enna)):
        enna[i] = enna[i].replace('\n', ' ') # discard this line
        ennasplit = enna[i].split()
        output.write('قبل: '+enna[i]+'\n')
        output.write('بعد: ')
        ennasplit[1] = 'إ'+ennasplit[1].lstrip('أ')
        output.write(ennasplit[0]+' '+ennasplit[1]+'\n')
        num += 1
    output.write('عدد الأخطاء التي صححت: '+str(num))
    print('Number of corrections:', num)
    print('percentage:', num*100/len(enna))

yenSmall = [] #stores words that have both forms.
def yenfunc(matches, kind):
    num = 0 #number of corrected mistakes
    x = 0
    output = open('Arabic/outputs/'+kind+'.txt', 'w')
    for i in range(len(matches)):
        matches[i] = matches[i].replace('\n', ' ') #discard this line
        checkword = cleanword(matches[i].rsplit(None, 1)[-1])
        if (checkword in anexcep) or (checkword in wonexcep):
            x=x+1
            continue
        checkword = checkword[0:-2]+'ين' #stores the other form of the word
        if checkword in yenexcep:
            x=x+1
            continue
        if (checkword in yenSmall) or (checkword in yenBig): #checkes if the other form of the word is in yenSmall or in yenBig
            if checkword not in yenSmall:
                yenSmall.append(checkword) #creates a list of words to check out later instead of searching the whole string every time, it makes the code faster
            output.write('قبل: '+ matches[i]+'\n')
            output.write('بعد: ')
            if matches[i].endswith('ان'):
                output.write(matches[i][0:-2]+'َين'+'\n')
            else:
                output.write(matches[i][0:-2]+'ين'+'\n')
            num += 1

    output.write('عدد الأخطاء التي صححت: '+str(num))
    print('Number of corrections:', num)
    print(x)
    print(len(matches))
    print('percentage:', num*100/len(matches))

#أداؤها ضعيف
def yenmutaselfunc(matches, kind):
    yenSmall = [] #stores words that have both forms. remove it once I have a final function. use the same list above yenfunc
    num = 0 #number of corrected mistakes
    x = 0
    output = open('Arabic/outputs/'+kind+'.txt', 'w')
    for i in range(len(matches)):
        matches[i] = matches[i].replace('\n', ' ') #discard this line
        checkword = cleanword(matches[i].rsplit(None, 1)[-1])
        if (checkword.startswith('ب') or checkword.startswith('ل') or checkword.startswith('ك')) and (checkword[1:] in anexcep or checkword[1:] in wonexcep):
            x+=1
            continue
        if not (checkword[1:] in anBig or checkword[1:] in wonBig):
            x += 1
            continue
        checkword = checkword[0:-2]+'ين' #stores the other form of the word
        if (checkword.startswith('ب') or checkword.startswith('ل') or checkword.startswith('ك')) and (checkword[1:] in yenexcep):
            x+=1
            continue
        if checkword[1:] in yenSmall or checkword[1:] in yenBig: #checkes if the other form of the word is in yenSmall or in yenBig
                if checkword not in yenSmall:
                    yenSmall.append(checkword) #creates a list of words to check out later instead of searching the whole string every time, it makes the code faster
                output.write('قبل: '+ matches[i]+'\n')
                output.write('بعد: ')
                if matches[i].endswith('ان'):
                    output.write(matches[i][0:-2]+'َين'+'\n')
                else:
                    output.write(matches[i][0:-2]+'ين'+'\n')
                num += 1

    output.write('عدد الأخطاء التي صححت: '+str(num))
    print('Number of corrections:', num)
    print(x)
    print(len(matches))
    print('percentage:', num*100/len(matches))

wonSmall = []
anSmall = []
def anfunc(matches, kind):
    secondWord = ''
    num = 0
    x = 0
    output = open('Arabic/outputs/'+kind+'.txt', 'w')
    for i in range(len(matches)):
        matches[i] = matches[i].replace('\n', ' ') #discard this line
        if len(matches[i].split()) == 3:
            secondWord = matches[i].split()[1]
        word = matches[i].rsplit(None, 1)[-1]
        checkword = cleanword(word)[0:-2]+'ون'
        if secondWord in Khafdh_first_identifiers or secondWord in Nasb_kanaSisters_first_identifiers or word.startswith('كال') or word.startswith('بال')  or word.startswith('لل') or checkword in wonexcep or checkword[0:-2]+'ين' in yenexcep or checkword[0:-2]+'ان' in anexcep or checkword in wonSmall or checkword in wonBig:
            x+=1
            if checkword not in wonSmall:
                wonSmall.append(checkword)
            continue
        checkword = checkword[0:-2]+'ان' #stores the other form of the word
        if (checkword in anSmall) or (checkword in anBig): #checkes if the other form of the word is in yenSmall or in yenBig
            if checkword not in anSmall:
                anSmall.append(checkword) #creates a list of words to check out later instead of searching the whole string every time, it makes the code faster
            output.write('قبل: '+ matches[i]+'\n')
            output.write('بعد: ' + matches[i][0:-2]+'ان'+'\n')
            num += 1
    output.write('عدد الأخطاء التي صححت: '+str(num))
    print('Number of corrections:', num)
    print(x)
    print(len(matches))
    print('percentage:', num*100/len(matches))

def af3al5func(af3al5, kind):
    num = 0
    x = 0
    output = open('Arabic/outputs/'+kind+'.txt', 'w')
    for i in range(len(af3al5)):
        af3al5[i] = af3al5[i].replace('\n', ' ') # discard this line
        af3al5[i] = re.sub('\u0640','',af3al5[i]) #removes tatweel(kashidah)
        if any(n in af3al5[i] for n in af3al5excep):
            x += 1
            continue
        output.write('قبل: '+af3al5[i]+'\n')
        output.write('بعد: ')
        if af3al5[i].endswith('ان') or af3al5[i].endswith('ين'):
            output.write(af3al5[i].rstrip('ن')+'\n')
        elif af3al5[i].endswith('ون'):
            output.write(af3al5[i].rstrip('ن')+'ا'+'\n')
        num += 1

    output.write('عدد الأخطاء التي صححت: '+str(num))
    print('Number of corrections:', num)
    print(x)
    print(len(af3al5))
    print('percentage:', num*100/len(af3al5))

def asma5func(asma5, kind):
    num = 0
    output = open('Arabic/outputs/'+kind+'.txt', 'w')
    nonraf3letters = ['ا', 'ي']
    nonnasbletters = ['ي', 'و']
    nonjarrletters = ['ا', 'و']
    for i in range(len(asma5)):
        asma5[i] = asma5[i].replace('\n', ' ') # discard this line
        asma5[i] = re.sub('\u0640','',asma5[i]) #removes tatweel(kashidah)
        asma5split = asma5[i].split()
        if len(asma5split) == 2:
            asma5splitword2 = list(asma5split[1]) #makes the second word a list
            if (asma5split[0] in Raf3_first_identifiers or asma5split[0][1:] in Raf3_first_identifiers) and (asma5splitword2[1] in nonraf3letters or (len(asma5splitword2) > 2 and asma5splitword2[2] in nonraf3letters)):
                output.write('قبل: '+asma5[i]+'\n')
                output.write('بعد: ')
                if asma5split[1].startswith('ف') or asma5split[1].startswith('ذ'):
                    asma5splitword2[1] = 'و'
                else:
                    asma5splitword2[2] = 'و'
                asma5split[1] = ''.join(asma5splitword2)
                output.write(asma5split[0]+' '+asma5split[1]+'\n')
                num += 1
            elif (asma5split[0] in Nasb_first_identifiers or asma5split[0][1:] in Nasb_first_identifiers or asma5split[0] in Nasb_kanaSisters_first_identifiers or asma5split[0][1:] in Nasb_kanaSisters_first_identifiers) and (asma5splitword2[1] in nonnasbletters or (len(asma5splitword2) > 2 and asma5splitword2[2] in nonnasbletters)):
                output.write('قبل: '+asma5[i]+'\n')
                output.write('بعد: ')
                if asma5split[1].startswith('ف') or asma5split[1].startswith('ذ'):
                    asma5splitword2[1] = 'ا'
                else:
                    asma5splitword2[2] = 'ا'
                asma5split[1] = ''.join(asma5splitword2)
                output.write(asma5split[0]+' '+asma5split[1]+'\n')
                num += 1
            elif (asma5split[0] in Jarr_first_identifiers or asma5split[0][1:] in Jarr_first_identifiers) and (asma5splitword2[1] in nonjarrletters or (len(asma5splitword2) > 2 and asma5splitword2[2] in nonjarrletters)):
                output.write('قبل: '+asma5[i]+'\n')
                output.write('بعد: ')
                if asma5split[1].startswith('ف') or asma5split[1].startswith('ذ'):
                    asma5splitword2[1] = 'ي'
                else:
                    asma5splitword2[2] = 'ي'
                asma5split[1] = ''.join(asma5splitword2)
                output.write(asma5split[0]+' '+asma5split[1]+'\n')
                num += 1
        elif len(asma5split) == 3:
            asma5splitword3 = list(asma5split[2]) #makes the second word a list
            if (asma5split[0] in Raf3_second_identifiers or asma5split[0][1:] in Raf3_second_identifiers) and (asma5splitword3[1] in nonraf3letters  or (len(asma5splitword3) > 2 and  asma5splitword3[2] in nonraf3letters)):
                output.write('قبل: '+asma5[i]+'\n')
                output.write('بعد: ')
                if asma5split[2].startswith('ف') or asma5split[2].startswith('ذ'):
                    asma5splitword3[1] = 'و'
                else:
                    asma5splitword3[2] = 'و'
                asma5split[2] = ''.join(asma5splitword3)
                output.write(asma5split[0]+' '+asma5split[1]+' '+asma5split[2]+'\n')
                num += 1
            elif (asma5split[0] in Nasb_second_identifiers or asma5split[0][1:] in Nasb_second_identifiers) and (asma5splitword3[1] in nonnasbletters or (len(asma5splitword3) > 2 and  asma5splitword3[2] in nonnasbletters)):
                output.write('قبل: '+asma5[i]+'\n')
                output.write('بعد: ')
                if asma5split[2].startswith('ف') or asma5split[2].startswith('ذ'):
                    asma5splitword3[1] = 'ا'
                else:
                    asma5splitword3[2] = 'ا'
                asma5split[2] = ''.join(asma5splitword3)
                output.write(asma5split[0]+' '+asma5split[1]+' '+asma5split[2]+'\n')
                num += 1
    output.write('عدد الأخطاء التي صححت: '+str(num))
    print('Number of corrections:', num)
    print(len(asma5))
    print('percentage:', num*100/len(asma5))

with open("Arabic/identifiers/Nasb_kanaSisters_first_identifiers.txt", "r", encoding='utf-8') as myfile:
    Nasb_kanaSisters_first_identifiers = myfile.read()
    Nasb_kanaSisters_first_identifiers = Nasb_kanaSisters_first_identifiers.split()
with open("Arabic/identifiers/Jarr_first_identifiers.txt", "r", encoding='utf-8') as myfile:
    Jarr_first_identifiers = myfile.read()
    Jarr_first_identifiers = Jarr_first_identifiers.split()
with open("Arabic/identifiers/Nasb_first_identifiers.txt", "r", encoding='utf-8') as myfile:
    Nasb_first_identifiers = myfile.read()
    Nasb_first_identifiers = Nasb_first_identifiers.split()
with open("Arabic/identifiers/Nasb_second_identifiers.txt", "r", encoding='utf-8') as myfile:
    Nasb_second_identifiers = myfile.read()
    Nasb_second_identifiers = Nasb_second_identifiers.split()
with open("Arabic/identifiers/Raf3_first_identifiers.txt", "r", encoding='utf-8') as myfile:
    Raf3_first_identifiers = myfile.read()
    Raf3_first_identifiers = Raf3_first_identifiers.split()
with open("Arabic/identifiers/Raf3_second_identifiers.txt", "r", encoding='utf-8') as myfile:
    Raf3_second_identifiers = myfile.read()
    Raf3_second_identifiers = Raf3_second_identifiers.split()
with open("Arabic/identifiers/asma5_identifiers.txt", "r", encoding='utf-8') as myfile:
    asma5_identifiers = myfile.read()
    asma5_identifiers = asma5_identifiers.split()
with open("Arabic/identifiers/dhamaer_postfixes.txt", "r", encoding='utf-8') as myfile:
    dhamaer_postfixes = myfile.read()
    dhamaer_postfixes = dhamaer_postfixes.split()
    
Khafdh_first_identifiers = Jarr_first_identifiers + Nasb_first_identifiers
Khafdh_second_identifiers = Nasb_second_identifiers

with open("Arabic/exceps/anexcep.txt", "r", encoding='utf-8') as myfile:
    anexcep = myfile.read()
    anexcep = anexcep.split()
with open("Arabic/exceps/wonexcep.txt", "r", encoding='utf-8') as myfile:
    wonexcep = myfile.read()
    wonexcep = wonexcep.split()
with open("Arabic/exceps/yenexcep.txt", "r", encoding='utf-8') as myfile:
    yenexcep = myfile.read()
    yenexcep = yenexcep.split()
with open("Arabic/exceps/af3al5excep.txt", "r", encoding='utf-8') as myfile:
    af3al5excep = myfile.read()
    af3al5excep = af3al5excep.split()

with open("Arabic/wiki11-23.txt", "r", encoding='utf-8') as myfile:
    wiki = myfile.read()

yenBig = sortwords(re.findall(r'\b\w+ين\b', wiki)) #stores all words ends with ين
wonBig = sortwords(re.findall(r'\b\w+ون\b', wiki)) #stores all words ends with ون
anBig = sortwords(re.findall(r'\b\w+ان\b', wiki)) #stores all words ends with ان

preString = r'\bو?ب?ك?ل?ف?(?:'
khafdh_zero = r'\b(?:بال|كال|لل)\w{3,}(?:ون|ان)\b'
khafdh_first = preString+createRegex(Khafdh_first_identifiers)+'|'+'(?:'+createRegex(Nasb_kanaSisters_first_identifiers)+r')(?!\sت|\sي)'+r')\s(?:ال\w{3,}|(?!ال)\w{3,})(?:ان|ون)\b'
khafdh_second = preString+createRegex(Khafdh_second_identifiers)+r')\s(?!ي)\w+\s(?!ي)(?!ال|وال|فال)\w{3,}(?:ون|ان)\b'
raf3_first = preString+createRegex(Raf3_first_identifiers)+r')\s(?:ال\w{3,}|(?!ال)\w{3,})(?:ين)\b'
raf3_second = preString+createRegex(Raf3_second_identifiers)+r')\s(?!ي)\w+\s(?!ال|وال|فال)\w{3,}(?:ين)\b'
khafdh_af3al5 = r'\b(?:أن|لأن|لئلا|لن|لا(?=\sت)|كي|لكي|لم|لما|مهما|أينما|حيثما)\s(?:ت|ي(?!\w{3,}ين))\w{3,}(?:ون|ين|ان)\b'
asma5_first = preString+createRegex(Raf3_first_identifiers)+'|'+createRegex(Nasb_first_identifiers)+'|'+createRegex(Jarr_first_identifiers)+createRegex(Nasb_kanaSisters_first_identifiers)+r')\s(?:'+createRegex(asma5_identifiers)+r')(?<!ذا|ذو|ذي)(?:'+createRegex(dhamaer_postfixes)+r')?\b'
asma5_second = preString+createRegex(Raf3_second_identifiers)+'|'+createRegex(Nasb_second_identifiers)+r')\s(?!ي)\w+\s(?:'+createRegex(asma5_identifiers)+r')(?<!ذا|ذو|ذي)(?:'+createRegex(dhamaer_postfixes)+r')?\b'
enna = preString+r'حيث|إذ|ألا)\s(?:أن)(?:'+createRegex(dhamaer_postfixes)+r')?\b'

if __name__ == "__main__":
    ennafunc(re.findall(enna, wiki), 'enna') #perfect performance, no need to even check. strict rules
    yenfunc(re.findall(khafdh_zero, wiki), 'Khafdh_zero')
    yenfunc(re.findall(khafdh_first, wiki), 'Khafdh_first')
    yenfunc(re.findall(khafdh_second, wiki), 'Khafdh_second')
    anfunc(re.findall(raf3_first, wiki), 'Raf3_first')
    anfunc(re.findall(raf3_second, wiki), 'Raf3_second')
    af3al5func(re.findall(khafdh_af3al5, wiki), 'af3al5') #لا الناهية، ليست مضبوطة


    #مشكلة: لا تستطيع هذه الدالة أن تميز إن كان هناك ضمير مستتر يقع بين الاسم وعامله
    #مثال: كان محمد يكن العداء لخالد ثم ما لبث أن أضحى أخاه. أخاه هنا خبر أضحى وليست اسمها لأن الاسم ضمير مستتر تقديره هو
    #أيضًا لا تستطيع التفريق بين ياء النسب وياء الخفض. ابن أبي عمر و رأيت أبي.
    asma5func(re.findall(asma5_first, wiki), 'asma5_first')

    asma5func(re.findall(asma5_second, wiki), 'asma5_second')

    #yenmutaselfunc(re.findall(r'\b(?:ب|ل|ك)(?!ل|ال)\w{3,}(?:ون|ان)\b', wiki), 'Khafdh_test') #expeirmental, bad performance

    #شرط
    #yenfunc(re.findall(r'\b(?:)\s(?:ال\w{3,}|(?!ال)\w{3,})(?:ان|ون)\b', wiki), 'exper') #experirmental

    #حروف الجر المتصلة
    #yenfunc(re.findall(r'\b(?:ب|ك|ل)\w{3,}(?:ون|ان)\b', wiki), 'JarrMutasel') #expeirmental