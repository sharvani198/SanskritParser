def searchnoun(st):
    #file structure: nounstem endLetter gender
    f=open("nouns");
    for line in f:
        attr=line.strip().split(" ")
        if st==attr[0]:
            return (int(attr[1])+1)*1000+int(attr[2])*100
    return 0

def searchverb(st):
    #file structure: verbstem
    f=open("verbs")
    for line in f:
        v=line.strip().split(" ")
        if st==v[0]:
            return 100000*1
    return 0

def encoder(w):
    s=""
    for x in w:
        e="{:03}".format(ord(x)-2304)
        s+=e
    return s

def encode(end,stem):
    endcode=["{:03}".format(ord(x)-2304) for x in end]
    endstr=""
    for x in endcode:
        endstr+=x
    stemcode=["{:03}".format(ord(x)-2304) for x in stem]
    stemstr=""
    for x in stemcode:
        stemstr+=x
    #print(endcode,stemcode)
    return(stemstr,endstr)

def searchnounend(e,att):
    #file structure: nounEnding endLetter gender vibhaktiCase number
    f=open("nounend")
    form=[]
    for line in f:
        l=line.strip().split(" ")
        if l[0]==e :
            ending=int(att/1000) - 1;gen=(att/100)%10
            if (int(l[1])==ending and int(l[2])==gen):
                form.append(att+int(l[3])*10+int(l[4]))
    return form

def searchverbend(e,att):
    #file structure: verbEnding pada tense person number
    f=open("verbend")
    form=[]
    for line in f:
        l=line.strip().split(" ")
        if l[0]==e :
            form.append(att+int(l[1])*1000+int(l[2])*100+int(l[3])*10+int(l[4]))
    return form

def searchpronoun(w):
    f=open("pronouns")
    form=[]
    for line in f:
        l=line.strip().split(" ")
        if l[0]==w:
            form.append(int(l[1])*100+int(l[2])*10+int(l[3]))
    return form

def morph(s):
   words=s.split(" ")
   d={}
   for w in words:
       end="";stem=""
       if searchpronoun(encoder(w)):
                att1=searchpronoun(encoder(w))
                d[words.index(w)+1]=att1
                continue
       for i in range(len(w)-1,-1,-1):
            end=w[i]+end
            stem=w[0:i]
            (stemstr,endstr)=encode(end,stem)
            att=searchnoun(stemstr)
            if att!=0:
                att1=searchnounend(endstr,att)
               	d[words.index(w)+1]=att1
                break
            elif (searchverb(stemstr)) or searchverb(stemstr[3:]):               
                
                att=searchverb(stemstr)
                if att==0 and stemstr[0:3]=='005' and searchverb(stemstr[3:]):
                    att=(2,1)
                att1=searchverbend(endstr,att)
                d[words.index(w)+1]=att1
                break
            
   return d
