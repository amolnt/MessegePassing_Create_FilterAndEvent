def f1(a,ns):
    a2=[]
    s=0
    for n in ns:
        a3=[]
        s=s+n
        for k in range(n):
            a3.append(a[s+k])
        a2.append(a3)
    return a2


a="computersciencedepartmentsppuneuniversity"
ns=[1,4,1,5,6]

print f1(a,ns)
