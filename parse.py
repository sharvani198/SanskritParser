from rel import relation

def getRelation(pos,nex,rel):
    edge=[]
    for i in rel:
        if i[2] in pos and i[3] in nex:
            edge.append((i[0],i[3])) 
        elif i[2] in nex and i[3] in pos:
            edge.append((i[0],i[2]))
    return edge
    
def parse(d,rel,possible,tree):
    edge=getRelation(d[level],d[level+1],rel)
    if len(edge)==0:
        return 0
    for i in edge:
        tree.append(i[0])
        if parse(d,rel,level+1,tree)==0:
            tree.pop()
            continue
        else:
            break
    if len(tree)==len(d)-1:
        return tree
            
    
def main():
    f=open("in")
    for i in f:
        s=i.strip()
        (d,rel)=relation(s)
        print(d,rel)
        possible=d[1]
        next=d[2]
        ptree=[]
        ptree=parse(d,rel,1,ptree)
        print(ptree)

if __name__=='__main__':
    main()
