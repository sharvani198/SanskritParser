from morph import morph
def idVN(d):
    v=[];n=[]
    for i in d:
        att=d[i]
        for j in att:
            if j>10000:
                v.append((i,j))
            else:
                n.append((i,j))
    return v,n

def pickVerb(verb):
    #not for sentences with many verbs
    if len(verb)==1:
        return verb[0]

def relation(s):
    rel=[]
    k=1
    res=morph(s)
    #print(res)
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
                elif vibi==1 and vibj==1 and geni==genj:
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
                      
    return res,rel

