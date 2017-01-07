import unicodedata
i=2304
x=0
d={}
while i<2432:
	u = "0x{:04x}".format(i)
	uc=chr(int(u,16))
	d[x]=uc
	i+=1
	x+=1
dd={}
for i in d:
        dd[d[i]]=i
f=open("in")
s=f.readline().strip()
words=s.split(" ")
let=list(s)
#print(words)
for w in words:
    for l in w:
        print(l,dd[l])

