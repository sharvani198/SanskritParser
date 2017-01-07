import sys
from os.path import dirname,abspath 

def searchnoun(st):
    #file structure: nounstem endLetter gender
    f=open(dirname(abspath(__file__))+"/nouns")
    for line in f:
        attr=line.strip().split(" ")
        if st==attr[0]:
            return (int(attr[1])+1)*1000+int(attr[2])*100
    return 0

def searchverb(st):
    #file structure: verbstem
    f=open(dirname(abspath(__file__))+"/verbs")
    for line in f:
        v=line.strip().split(" ")
        if st==v[0]:
            return 100000*1
    return 0

def encoder(w):
    s=""
    #w=w.decode("utf-8")
    for x in w:
        e="{:03}".format(ord(x)-2304)
        s+=e
    return s

def encode(end,stem):
    #end=end.decode("utf-8")
    endcode=["{:03}".format(ord(x)-2304) for x in end]
    endstr=""
    for x in endcode:
        endstr+=x
    #stem=stem.decode("utf-8")
    stemcode=["{:03}".format(ord(x)-2304) for x in stem]
    stemstr=""
    for x in stemcode:
        stemstr+=x
    #print(endcode,stemcode)
    return(stemstr,endstr)

def searchnounend(e,att):
    #file structure: nounEnding endLetter gender vibhaktiCase number
    f=open(dirname(abspath(__file__))+"/nounend")
    form=[]
    for line in f:
        l=line.strip().split(" ")
        if l[0]==e :
            if att>=21000:
                ending=int(att/20000)-1;gen=(att/100)%10
            else:
                ending=int(att/1000) - 1;gen=(att/100)%10
            if (int(l[1])==ending and int(l[2])==gen):
                form.append(att+int(l[3])*10+int(l[4]))
    return form

def searchverbend(e,att):
    #file structure: verbEnding pada tense person number
    f=open(dirname(abspath(__file__))+"/verbend")
    form=[]
    for line in f:
        l=line.strip().split(" ")
        if l[0]==e :
            form.append(att+int(l[1])*1000+int(l[2])*100+int(l[3])*10+int(l[4]))
    return form

def searchpronoun(w):
    f=open(dirname(abspath(__file__))+"/pronouns")
    form=[]
    for line in f:
        l=line.strip().split(" ")
        if l[0]==w:
            form.append(int(l[1])*100+int(l[2])*10+int(l[3]))
    return form

def searchadj(w):
    f=open(dirname(abspath(__file__))+"/adjectives")
    form=[]
    for line in f:
        l=line.strip().split(" ")
        if l[0]==w:
            form.append(21000+(10000*int(l[1])+100*int(l[2])))
    return form

def morph(words):
    d={}
    no=[]
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
            att2=searchadj(stemstr)
            ind=words.index(w)+1
            if att2!=0:
                for each in att2:
                    att3=searchnounend(endstr,each)
                    if len(att3)!=0:
                        d[ind]=att3
            
            if att!=0:
                att1=searchnounend(endstr,att)
                try:
                    if d[ind]:
                        d[ind].extend(att1)
                except KeyError:
                    d[ind]=att1
                break
            elif (searchverb(stemstr)) or searchverb(stemstr[3:]):               
                att=searchverb(stemstr)
                if att==0 and stemstr[0:3]=='005' and searchverb(stemstr[3:]):
                    att=(2,1)
                att1=searchverbend(endstr,att)
                d[ind]=att1
                break        
    if len(d)!= len(words):
        for i in range(len(words)):
            if i+1 not in d.keys():
                no.append(i)
    
    return d,no


def idVN(d):
    v=[];n=[]
    for i in d:
        att=d[i]
        for j in att:
            if j>100000:
                v.append((i,j))
            else:
                n.append((i,j))
    return v,n

def pickVerb(verb):
    #not for sentences with many verbs
    if len(verb)==1:
        return verb[0]

def relation(res):
    rel=[]
    k=1
    (verb,noun)=idVN(res)
    #print(verb,noun,pro)
    v=pickVerb(verb)[1]
    num=v%10
    for i in noun:
        n=i[1]
        vib=int(n/10)%10
        if n%10 ==num and vib==1 :
            rel.append((k,'sv',n,v))
            k+=1
    for i in noun:
        for j in noun:
            wi=i[1];wj=j[1]
            vibi=int(wi/10)%10
            vibj=int(wj/10)%10
            geni=int(wi/100)%10
            genj=int(wj/100)%10
            if j[0]!=i[0]:
                if vibi==2 and vibj==1 :
                    rel.append((k,'so',wj,wi));k+=1
                    rel.append((k,'ov',wi,v));k+=1
                elif vibi==1 and vibj==1 and geni==genj:
                    if wj>21000 and wi<21000:
                        rel.append((k,'smod',wi,wj));k+=1
                elif vibi==1 and vibj==3:
                    if geni==genj:
                        rel.append((k,'sby',wi,wj));k+=1
                    else:
                        rel.append((k,'swith',wi,wj));k+=1 
                elif vibi==1 and vibj==4:
                    if geni==genj:
                        rel.append((k,'sto',wi,wj));k+=1
                    else:
                        rel.append((k,'sfor',wi,wj));k+=1
                elif vibi==1 and vibj==5:
                    rel.append((k,'sfrom',wi,wj));k+=1
                elif vibi==2 and vibj==5:
                    rel.append((k,'ofrom',wi,wj));k+=1
                elif vibi==1 and vibj==6:
                    rel.append((k,'sof',wi,wj));k+=1
                elif vibi==1 and vibj==7:
                    rel.append((k,'sin',wi,wj));k+=1
                    rel.append((k,'oloc',wj,v));k+=1
                      
    return rel

def getRelation(pos,nex,rel):
    edge=[]
    if nex==0:
        return 0
    for i in rel:
        if i[2] in pos and i[3] in nex:
            edge.append((i[0],[i[3]])) 
        elif i[2] in nex and i[3] in pos:
            edge.append((i[0],[i[2]]))
    return edge
    
def parse(d,rel,possible,level,tree):
    edge=getRelation(possible,d[level+1],rel)
    if edge==0:
        return 1
    if len(edge)==0:
        return 0
    print(edge)
    for i in edge:
        tree.append(i[0])
        if parse(d,rel,i[1],level+1,tree)==1:
            return 1
        else:
            tree.pop()          
   
        
def findWord(d,x):
    for i in d:
        if x in d[i]:
            return i 
        
         
def parsetree(d,rel):
    d[len(d)+1]=0
    ptree=[]
    parse(d,rel,d[1],1,ptree)
    wordAtt=set()
    r=[]
    for i in ptree:
        r.append((rel[i-1][1],findWord(d,rel[i-1][2]),findWord(d,rel[i-1][3])))
        wordAtt.add(rel[i-1][2])
        wordAtt.add(rel[i-1][3])
    #print(wordAtt)
    return r,wordAtt

class node:
    def __init__(self,i):
        self.ind=i
    def setpos(self,p):
        self.pos=p
    def setgen(self,g):
        self.gen=g
    def setvib(self,v):
        self.vib=v
    def setnum(self,n):
        self.num=n
    def setpada(self,pa):
        self.pada=pa
    def setten(self,t):
        self.ten=t 
    def setper(self,pe):
        self.per=pe 
    def att(self):
        self.rel=()
        if self.pos=="Verb":
            self.values=(self.pos,self.pada,self.ten,self.per,self.num)
        else:
            self.values=(self.pos,self.gen,self.vib,self.num)
    def setrel(self,r,j):
        self.rel=(r,j)        
    
                      
    
def display(r,a,w,m):
    nodes=[]
    gen={0:"Masc",1:"Fem",2:"Neut"}
    vib={1:"Nom",2:"Acc",3:"Inst",4:"Dat",5:"Abl",6:"Gen",7:"Loc"}
    num={1:"Sing",2:"Dual",3:"Plu"}
    tens={1:"Pres",2:"Past",3:"Fut"}
    pers={1:"Thir",2:"Sec",3:"Firs"}
    pada={1:"Paras"}
    for i in a:
        j=findWord(m, i)
        n=node(j)
        if i<1000:
            n.setpos("Pronoun")
            if int(i/100)==3:
                n.setgen("None")
                n.setper(pers[3])
            else:
                n.setgen(gen[int(i/100)])
            n.setvib(vib[int(i/10)%10])
            n.setnum(num[int(i%10)])
        elif i<100000:
            n.setpos("Noun")
            n.setgen(gen[int(i/100)%10])
            n.setvib(vib[int(i/10)%10])
            n.setnum(num[int(i%10)])
        else:
            n.setpos("Verb")
            n.setpada(pada[int(i/1000)%10])
            n.setten(tens[int(i/100)%10])
            n.setper(pers[int(i/10)%10])
            n.setnum(num[int(i%10)])
        n.att()
        nodes.append(n)
    for k in r:
        i=k[1];j=k[2]
        rel=k[0]
        nodes[i-1].setrel(rel[0],j)
        nodes[j-1].setrel(rel[1:],i)
        
    return nodes    



if __name__=="__main__":
     inputFile=sys.argv[1]
     f=open(inputFile)
     for i in f:
          inputStr=i.strip()
          words=inputStr.split(" ") #tokenization
          morphemes,no=morph(words)
          if no:
               notlist=no
               notfound="The following words were not found in dictionary:\n"
               for i in notlist:
                    notfound+= str(i) +words[i-1] +"\n"
               print( notfound)
          else:
               print(morphemes)
               relations=relation(morphemes)
               print(relations)
               selectrel,selectatt=parsetree(morphemes,relations)
               print(selectrel,selectatt)
               nodes=display(selectrel,selectatt,words,morphemes)
               print(inputStr)
               for n in nodes:
                    print( n.ind,n.values,n.rel)
             
