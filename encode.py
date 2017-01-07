def encoder(f):
    ff=open(f)
    for i in ff:
        w=i.strip()
        s=""
        for x in w:
            e="{:03}".format(ord(x)-2304)
            s+=e
        print(s)
        


