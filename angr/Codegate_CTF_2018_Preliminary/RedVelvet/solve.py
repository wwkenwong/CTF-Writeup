from z3 import *


s = Solver()

for i in range(0,26):
    globals()['v%i' % i] = BitVec('v%i' % i,32)

#func1(v0, v1);
s.add(v0*2*(v0^v1)-v1==10858)
s.add(v0>85)
s.add(v0<=95)
s.add(v1>96)
s.add(v1<=111)

#func2(v1, v2);
s.add(v1%v2==7)
s.add(v2>90)

#func3(v2, v3);
s.add((v2/v3)+(v2^v3)==21)
s.add(v2<=99)
s.add(v3<=119)

# # #func4(v3, v4);
s.add((v3%v4)+v3==137)
s.add(v4==95)

# #func5(v4, v5);
#s.add(((v4+v5)^(v4^v5^v4))==255) < crash here??

s.add(v5<=89)
s.add(v5>85)

#func6(v5, v6, v7);
s.add(v5<=v6)
s.add(v6<=v7)
s.add(v6>110)
s.add(v7>115)
s.add((v6+v7)^(v5+v6)==44)
s.add(((v6+v7)%v5)+v6==161)


#func7(v7, v8, v9);
s.add(v7>=v8)
s.add(v8>=v9)
s.add(v7<=119)
s.add(v8>90)
s.add(v9<=89)
s.add((v7+v9)^(v8+v9)==122)
s.add(((v7+v9)%v8)+v9==101)



#func8(v9, v10, v11);
s.add(v9<=v10)
s.add(v10<=v11)
s.add(v11<=114)
s.add(((v9+v10))/v11*v10==97)
s.add((v11^(v9-v10))*v10==-10088)



#func9(v11, v12, v13);
s.add(v11==v12)
s.add(v12>=v13)
s.add(v13<=99)
s.add(v13+(v11*(v13-v12))-v11==-1443)



#func10(v13, v14, v15);
s.add(v13>=v14)
s.add(v14>=v15)
s.add(v14*(v13+v15+1)-v15==15514)
s.add(v14>90)
s.add(v14<=99)



#func11(v15, v16, v17);
s.add(v16>=v15)
s.add(v15>=v17)
s.add(v16>100)
s.add(v16<=104)
s.add(v15+(v16^(v16-v17))-v17==70)
s.add(((v16+v17)/v15)+v15==68)


#func12(v17, v18, v19);
s.add(v17>=v18)
s.add(v18>=v19)
s.add(v18<=59)
s.add(v19<=44)
s.add(v17+(v18^(v18+v19))-v19==111)
s.add((v18^(v18-v19))+v18==101)



#func13(v19, v20, v21);
s.add(v19<=v20)
s.add(v20<=v21)
s.add(v19>40)
s.add(v20>90)
s.add(v21<=109)
s.add(v21+(v20^(v21+v19))-v19==269)
s.add((v21^(v20-v19))+v20==185)



#func14(v21, v22, v23);
s.add(v21>=v23)
s.add(v22>=v23)
s.add(v22<=99)
s.add(v23>90)
s.add(v21+(v22^(v22+v21))==185+v23) #<???
#s.add(v21+(v22^(v22+v21)-v23)==185) integer overflow


#func15(v23, v24, v25);
s.add(v24>=v25)
s.add(v24>=v23)
s.add(v25>95)
s.add(v24<=109)
s.add(((v24-v23)*v24^v25)-v23==1214)
s.add(((v25-v24)*v25^v23)+v24==-1034)

print s.check()
modl=s.model()
res = ""
for i in range(0,26):
    obj = globals()['v%i' % i]
    c = modl[obj].as_long()
    print('v%i: %x' % (i, c))
    res = res + chr(c)
    print res


print res
