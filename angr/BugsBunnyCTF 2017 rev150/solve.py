from z3 import *

FLAG_LENGTH = 20


a=Int('a')
b=Int('b')
c=Int('c')
d=Int('d')
e=Int('e')
f=Int('f')
g=Int('g')
h=Int('h')
i=Int('i')
j=Int('j')
k=Int('k')
l=Int('l')
m=Int('m')
n=Int('n')
o=Int('o')
p=Int('p')
q=Int('q')
r=Int('r')
s=Int('s')
t=Int('t')


sol = Solver()

sol.add(p+e==10)
sol.add(b*s==2)
sol.add(p/j==1)
sol.add(j!=0)

sol.add(f-r==-1)
sol.add(p-b==5)
sol.add(b*k==18)
sol.add(i+n==14)
sol.add(s*i==5)
sol.add(e*l==0)
sol.add(i+j==12)
sol.add(m-t==1)
sol.add(j%r==7)
sol.add(r!=0)

sol.add(o*q==40)
sol.add(h-e==1)
sol.add(g+a==6)
sol.add(c-q==0)
sol.add(e-g==1)
sol.add(a%f==4)
sol.add(f!=0)
sol.add(p!=0)

sol.add(f*l==0)
sol.add(k%p==2)
sol.add(l/d==0)
sol.add(d!=0)

sol.add(o-n==-4)
sol.add(s+t==3)

print(sol.check())
print(sol.model())
