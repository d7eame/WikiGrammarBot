__author__ = 'd7eame'
# -*- coding: utf-8 -*-
import re
def createRegex(identifiers):
    return '|'.join(identifiers)

def cleanword(word):
    chars = [
        '\u0640', # tatweel(kashidah)
        '\u064b', # FATHATAN
        '\u064c', # DAMMATAN
        '\u064d', # KASRATAN
        '\u064e', # FATHA
        '\u064f', # DAMMA
        '\u0650', # KASRA
        '\u0651', # SHADDA
        '\u0652'  # SUKUN
    ]
    for c in chars:
        word = re.sub(c, '', word) 
    if len(word) >4 and word.startswith('ال'):
        word = word[2:]
    return word

def textoutput(matches, operation, name): #for printing  testing results in a text file
    output = ''
    num = 0
    for phrase in matches:
        phrase =  phrase.replace('\n', ' ') #ignore this line
        returned = operation(phrase)
        if returned is not None:
            output += 'قبل: %s\n' % phrase
            output += 'بعد: %s\n' % returned
            num += 1
    output += 'عدد الأخطاء: %d' % num
    with open('Arabic/outputs/'+name+'.txt', 'w') as f:
        f.write(output)
    print('Number of corrections:', num)
    print('persentage:', num*100/len(matches))

def noonfunc(phrase):
    checkword = cleanword(phrase.split()[0])
    phrase = phrase.split()
    if  checkword.endswith('ان') and checkword not in MuthanaExcep:
        if checkword[:-2] in Muthana or (checkword[:-2].endswith('ت') and checkword[:-3] in Muthana):
            phrase[0] = phrase[0][:-1]
            return(' '.join(phrase))
    elif checkword.endswith('ون') and checkword not in MuthakarExcep and checkword[:-2] in MuthakarSalem:
        phrase[0] = phrase[0][:-1]
        return(' '.join(phrase))
    elif checkword.endswith('ين'):
        if checkword[:-2] in MuthakarSalem or (checkword[:-2] in Muthana or (checkword[:-2].endswith('ت') and checkword[:-3] in Muthana)):
            phrase[0] = phrase[0][:-1]
            return(' '.join(phrase))
    return(None)

def yenfunc(phrase):
    checkword = cleanword(phrase.rsplit(None, 1)[-1])
    phrase = list(phrase)
    prefixes = ('لل','بال','كال','ولل','فلل','وبال','فبال','وكال''فكال','كبال','كلل')
    if len(checkword) >5:
        for p in prefixes:
                if checkword.startswith(p):
                    checkword = checkword[len(p):]
    if checkword[-2] == 'ا' and checkword not in MuthanaExcep:
        if checkword[:-2] in Muthana or (checkword[:-2].endswith('ت') and checkword[:-3] in Muthana):
            phrase[-2] = 'يَ'
            return(''.join(phrase))
    elif checkword[-2] == 'و' and checkword not in MuthakarExcep and checkword[:-2] in MuthakarSalem:
        phrase[-2] = 'ي'
        return(''.join(phrase))
    return(None)

def yenmutasl(phrase): #experimental
    checkword = cleanword(phrase)
    phrase = list(phrase)
    if checkword in MuthanaMutaslExcep: return(None)
    prefixes = ('ل','ك','ب','ول','فل','كل','وك','فك','وب','فب','لب','كب')
    if len(checkword) >3:
        for p in prefixes:
            if checkword.startswith(p):
                checkword = checkword[len(p):]
    if checkword in MuthanaMutaslExcep: return(None)
    if checkword[-2] == 'ا' and checkword not in MuthanaExcep:
        if checkword[:-2] in Muthana or (checkword[:-2].endswith('ت') and checkword[:-3] in Muthana):
            phrase[-2] = 'يَ'
            return(''.join(phrase))
    elif checkword[-2] == 'و' and checkword not in MuthakarExcep and checkword[:-2] in MuthakarSalem:
        phrase[-2] = 'ي'
        return(''.join(phrase))
    return(None)

def anfunc(phrase):
    checkword = cleanword(phrase.rsplit(None, 1)[-1])
    if (len(phrase.split()) == 3 and phrase.split()[1] in Khafdh_first_identifiers) or (checkword in yenexcep):#add Khafdh_first_identifiers to the regex
        return(None)
    phrase = list(phrase)
    if checkword[:-2] not in MuthakarSalem and (checkword[:-2] in Muthana or (checkword[:-2].endswith('ت') and checkword[:-3] in Muthana)):
        phrase[-2] = 'ا'
        return(''.join(phrase))
    return(None)

def af3al5func(phrase):
    checkword = cleanword(phrase.rsplit(None, 1)[-1])
    if checkword in af3al5excep:
        return(None)
    elif phrase.endswith(('ان', 'ين')):
        return(phrase.rstrip('ن'))
    elif phrase.endswith('ون'):
        return(phrase.rstrip('ن') + 'ا')

def asma5func(phrase):
    nonraf3letters = ('ا', 'ي')
    nonnasbletters = ('ي', 'و')
    nonjarrletters = ('ا', 'و')
    phraseSplit = phrase.split()
    esm5 = list(cleanword(phrase.rsplit(None, 1)[-1]))
    if phraseSplit[-1].startswith(('ف', 'ذ')): t = 1
    else: t = 2
    if len(phraseSplit) == 2:
        if phraseSplit[0] in Raf3_first_identifiers or phraseSplit[0][1:] in Raf3_first_identifiers:
            if esm5[1] in nonraf3letters or (len(esm5) > 2 and esm5[2] in nonraf3letters): #instead of in nonraf3letters, you can say !=و
                esm5[t] = 'و'
                phraseSplit[1] = ''.join(esm5)
                return(' '.join(phraseSplit))
        elif phraseSplit[0] in Nasb_first_identifiers or phraseSplit[0][1:] in Nasb_first_identifiers:
            if esm5[1] in nonnasbletters or (len(esm5) > 2 and esm5[2] in nonnasbletters):
                esm5[t] = 'ا'
                phraseSplit[1] = ''.join(esm5)
                return(' '.join(phraseSplit))
        elif phraseSplit[0] in Jarr_first_identifiers or phraseSplit[0][1:] in Jarr_first_identifiers:
            if esm5[1] in nonjarrletters or (len(esm5) > 2 and esm5[2] in nonjarrletters):
                esm5[t] = 'ي'
                phraseSplit[1] = ''.join(esm5)
                return(' '.join(phraseSplit))
    elif len(phraseSplit) == 3 and phraseSplit[1] not in  Jarr_first_identifiers:
        if phraseSplit[0] in Raf3_second_identifiers or phraseSplit[0][1:] in Raf3_second_identifiers:
            if esm5[1] in nonraf3letters  or (len(esm5) > 2 and  esm5[2] in nonraf3letters):
                esm5[t] = 'و'
                phraseSplit[2] = ''.join(esm5)
                return(' '.join(phraseSplit))
        elif phraseSplit[0] in Nasb_second_identifiers or phraseSplit[0][1:] in Nasb_second_identifiers:
            if esm5[1] in nonnasbletters or (len(esm5) > 2 and  esm5[2] in nonnasbletters):
                esm5[t] = 'ا'
                phraseSplit[2] = ''.join(esm5)
                return(' '.join(phraseSplit))

def mu3talfunc(phrase):
    checkword = cleanword(phrase.rsplit(None, 1)[-1])[1:]
    if checkword in mu3tal:
        return(phrase[:-1])

def ennafunc(phrase):
    phrase = phrase.split()
    phrase[1] = 'إ'+phrase[1][1:]
    return(' '.join(phrase))

def a3dad(phrase):#تقوم ببعض من التصحيح الإملائي، نظف الدالة
    if len(phrase.split()) == 2:
        adad = phrase.split()[0]
        madoud = phrase.split()[1]
        checkadad = cleanword(adad)
        checkmadoud = cleanword(madoud)
        if madoud.startswith('ال'): return(None)
        if checkadad == 'ثمان': adad = adad+'ي'
        if checkmadoud.endswith('ات') and checkadad.endswith('ة'):
            return(adad[:-1]+' '+madoud)
        elif checkmadoud.endswith(('ين','ون')) and not checkadad.endswith('ة'):
            if checkmadoud.startswith('و') and checkmadoud[1:].startswith(('عشر','ثلاث','اربع','أربع','خمس','ست','سبع','ثمان','تسع')): return(None)#add it to the regex
            return(adad+'ة '+madoud)
        else: return(None)
    elif len(phrase.split()) == 3:
        adad = phrase.split()[0]
        murkab = phrase.split()[1]
        madoud = phrase.split()[2]
        checkadad = cleanword(adad)
        checkmadoud = cleanword(madoud)
        if checkadad == 'ثمان': adad = adad+'ي'            
        if checkmadoud.endswith('ة'):
            if not murkab.startswith('و') and not murkab.endswith('ة'): murkab = murkab+'ة'
            if checkadad.endswith('ة'):
                if murkab.startswith('و') and adad.endswith('ية'): adad = adad[:-1]
                return(adad[:-1]+' '+murkab+' '+madoud)
            elif checkadad in ('أحد','واحد','احد'):
                adad = 'إحدى'
                return(adad+' '+murkab+' '+madoud)
            elif checkadad in ('اثنا','إثنا','اثنان', 'إثنان','اثنتا','إثنتا','إثنتان','اثنتان'):
                if murkab.startswith('و') and checkadad != 'اثنتان':
                    adad = 'اثنتان'
                    return(adad+' '+murkab+' '+madoud) 
                elif murkab.startswith('ع') and checkadad != 'اثنتا':
                    adad = 'اثنتا'
                    return(adad+' '+murkab+' '+madoud) 
        elif not checkmadoud.endswith('ة'):
            if murkab.endswith('ة'): murkab = murkab[:-1]
            if not checkadad.endswith(('ة','د','ا','ن', 'ى')):
                return(adad+'ة '+murkab+' '+madoud)
            elif checkadad in ('إحدى','احدى','واحد') and murkab.startswith('ع'):
                adad = 'أحد'
                return(adad+' '+murkab+' '+madoud) 
            elif checkadad in ('إحدى','احدى','أحد', 'احد') and murkab.startswith('و'):
                adad = 'واحد'
                return(adad+' '+murkab+' '+madoud) 
            elif checkadad in ('اثنا','إثنا','اثنان', 'إثنان','اثنتا','إثنتا','إثنتان','اثنتان'):
                if murkab.startswith('و') and checkadad != 'اثنان':
                    adad = 'اثنان'
                    return(adad+' '+murkab+' '+madoud) 
                elif murkab.startswith('ع') and checkadad != 'اثنا':
                    adad = 'اثنا'
                    return(adad+' '+murkab+' '+madoud) 
        else: return(None)

with open("Arabic/identifiers/Jarr_first_identifiers.txt", "r", encoding='utf-8') as myfile:
    Jarr_first_identifiers = myfile.read().split()
with open("Arabic/identifiers/Nasb_first_identifiers.txt", "r", encoding='utf-8') as myfile:
    Nasb_first_identifiers = myfile.read().split()
with open("Arabic/identifiers/Nasb_second_identifiers.txt", "r", encoding='utf-8') as myfile:
    Nasb_second_identifiers = myfile.read().split()
with open("Arabic/identifiers/Raf3_first_identifiers.txt", "r", encoding='utf-8') as myfile:
    Raf3_first_identifiers = myfile.read().split()
with open("Arabic/identifiers/Raf3_second_identifiers.txt", "r", encoding='utf-8') as myfile:
    Raf3_second_identifiers = myfile.read().split()
with open("Arabic/identifiers/asma5_identifiers.txt", "r", encoding='utf-8') as myfile:
    asma5_identifiers = myfile.read().split()
with open("Arabic/identifiers/dhamaer_postfixes.txt", "r", encoding='utf-8') as myfile:
    dhamaer_postfixes = myfile.read().split()
with open("Arabic/identifiers/Nwasib_alf3l.txt", "r", encoding='utf-8') as myfile:
    Nwasib_alf3l = myfile.read().split()
with open("Arabic/identifiers/Jwazim_alf3l.txt", "r", encoding='utf-8') as myfile:
    Jwazim_alf3l = myfile.read().split()
with open("Arabic/identifiers/three_ten.txt", "r", encoding='utf-8') as myfile:
    three_ten_identifiers = myfile.read().split()
with open("Arabic/identifiers/uqud.txt", "r", encoding='utf-8') as myfile:
    uqud_identifiers = myfile.read().split()
with open("Arabic/identifiers/one_two.txt", "r", encoding='utf-8') as myfile:
    one_two_identifiers = myfile.read().split()
    
Khafdh_first_identifiers = Jarr_first_identifiers + Nasb_first_identifiers
Khafdh_second_identifiers = Nasb_second_identifiers

with open("Arabic/dictionary/MuthakarSalem.txt", "r", encoding='utf-8') as myfile:
    MuthakarSalem = myfile.read().split()
with open("Arabic/dictionary/Muthana.txt", "r", encoding='utf-8') as myfile:
    Muthana = myfile.read().split()
with open("Arabic/dictionary/mu3tal.txt", "r", encoding='utf-8') as myfile:
    mu3tal = myfile.read().split()

with open("Arabic/exceps/yenexcep.txt", "r", encoding='utf-8') as myfile:
    yenexcep = myfile.read().split()
with open("Arabic/exceps/MuthakarExcep.txt", "r", encoding='utf-8') as myfile:
    MuthakarExcep = myfile.read().split()
with open("Arabic/exceps/MuthanaExcep.txt", "r", encoding='utf-8') as myfile:
    MuthanaExcep = myfile.read().split()
with open("Arabic/exceps/MuthanaMutaslExcep.txt", "r", encoding='utf-8') as myfile:
    MuthanaMutaslExcep = myfile.read().split()
with open("Arabic/exceps/af3al5excep.txt", "r", encoding='utf-8') as myfile:
    af3al5excep = myfile.read().split()

with open("Arabic/corpus/wikipedia.txt", "r", encoding='utf-8') as myfile:
    corpus = myfile.read()

#Regular Expressions
preString = r'\bو?ب?ك?ل?ف?(?:'
khafdh_mutasl = r'\bو?ك?ف?(?:ب|ل|ك)\w{3,}(?:ون|ان)\b'
khafdh_zero = r'\bو?ك?ف?(?:بال|كال|لل)\w{3,}(?:ون|ان)\b'
khafdh_first = preString+createRegex(Khafdh_first_identifiers)+r')\s(?:ال\w{3,}|(?!ال)\w{3,})(?:ان|ون)\b'
khafdh_second = preString+createRegex(Khafdh_second_identifiers)+r')\s(?!ي)\w+\s(?!ي)(?!ال|وال|فال)\w{3,}(?:ون|ان)\b'
raf3_first = preString+createRegex(Raf3_first_identifiers)+r')\s(?:ال\w{3,}|(?!ال|كال|لل|بال)\w{3,})(?:ين)\b'
raf3_second = preString+createRegex(Raf3_second_identifiers)+r')\s(?!ي)\w+\s(?!ال|وال|فال|بال|كال|لل)\w{3,}(?:ين)\b'
af3al5  = preString+createRegex(Nwasib_alf3l+Jwazim_alf3l)+r')\s(?:ت|ي(?!\w{3,}ين))\w{3,}(?:ون|ين|ان)\b'
asma5_first = preString+createRegex(Raf3_first_identifiers+Nasb_first_identifiers+Jarr_first_identifiers)+r')\s(?:'+createRegex(asma5_identifiers)+r')(?<!ذا|ذو|ذي)(?:'+createRegex(dhamaer_postfixes)+r')?\b'
asma5_second = preString+createRegex(Raf3_second_identifiers+Nasb_second_identifiers)+r')\s(?!ي)\w+\s(?:'+createRegex(asma5_identifiers)+r')(?<!ذا|ذو|ذي)(?:'+createRegex(dhamaer_postfixes)+r')?\b'
enna = preString+r'حيث|إذ|ألا)\s(?:أن|ان)(?:'+createRegex(dhamaer_postfixes)+r')?\b'
mu3tall = preString+createRegex(Jwazim_alf3l)+r')\s(?:أ|ن|ي|ت)\w{3,6}(?:ى|و|ي|ا)\b'
noon_delet = r'\b(?!و?ك?ف?لل|و?ب?ك?ف?ال)\w{3,}(?:ان|ون|ين)\sال\w{2,}\b'
three_ten = preString+createRegex(three_ten_identifiers)+r')\s\w{3,}(?:ين|ون|ات)\b'
uqud = preString+createRegex(one_two_identifiers+three_ten_identifiers)+r')\s(?:'+createRegex(uqud_identifiers)+r')\s\w{3,}\b'
#experimental
#khafdh_first = preString+createRegex(Khafdh_first_identifiers)+r')\s(?:(?!ال)\w{3,}(?:ا|و)(?:'+createRegex(dhamaer_postfixes)+r')|(?:ال\w{3,}|(?!ال)\w{3,})(?:ان|ون))\b'

khafdh_mutasl_matches = re.findall(khafdh_mutasl, corpus)
khafdh_zero_matches = re.findall(khafdh_zero, corpus)
khafdh_first_matches = re.findall(khafdh_first, corpus)
khafdh_second_matches = re.findall(khafdh_second, corpus)
raf3_first_matches = re.findall(raf3_first, corpus)
raf3_second_matches = re.findall(raf3_second, corpus)
af3al5_matches = re.findall(af3al5, corpus)
asma5_first_matches = re.findall(asma5_first, corpus)
asma5_second_matches = re.findall(asma5_second, corpus)
enna_matches = re.findall(enna, corpus)
mu3tall_matches = re.findall(mu3tall, corpus)
noon_delet_matches = re.findall(noon_delet, corpus)
three_ten_matches = re.findall(three_ten, corpus)#لا تعمل بشكل حسن عندما يكون جمع تكسير ينتهي ب ات ومفرده مذكر مثل تفجيرات
uqud_matches = re.findall(uqud, corpus)
mu3tall_matches = re.findall(mu3tall, corpus)

if __name__ == "__main__":
    textoutput(three_ten_matches+uqud_matches, a3dad, 'a3dad')
    textoutput(khafdh_mutasl_matches, yenmutasl, 'Khafdh_mutasl')
    textoutput(khafdh_zero_matches, yenfunc, 'Khafdh_zero')
    textoutput(khafdh_first_matches, yenfunc, 'Khafdh_first') #all the yenfunc calls can be added to a single call by summing all the matches, same thing goes with other function calls
    textoutput(khafdh_second_matches, yenfunc, 'Khafdh_second')
    textoutput(raf3_first_matches, anfunc, 'Raf3_first')
    textoutput(raf3_second_matches, anfunc, 'Raf3_second')
    textoutput(af3al5_matches, af3al5func, 'af3al5')
    textoutput(asma5_first_matches, asma5func, 'asma5_first')
    textoutput(asma5_second_matches, asma5func, 'asma5_second')
    textoutput(noon_delet_matches, noonfunc, 'noon_delet')
    textoutput(mu3tall_matches, mu3talfunc, 'mu3tal')
    textoutput(enna_matches, ennafunc, 'enna') #perfect