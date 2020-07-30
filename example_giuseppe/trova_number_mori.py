import re
str = open('job.out', 'r').read()
a=re.findall(r'QHGK conductivity:  (\d+\.\d+)',str)
b=re.findall(r'Temperature:  (\d+)',str)
risultati=open('risultati_mori.out','a')
#temp=input()
#print("QHGK ", temp," Threshold", sep=" " ,file=risultati)
print(len(a))
print(len(b))
#print(a[0],file=risultati)#gli indici partono da 0
for x in range(len(a)):#nota che gli indici sono sfasati di 1    
 print(a[x],b[x],sep="  ",file=risultati)
risultati.close()

