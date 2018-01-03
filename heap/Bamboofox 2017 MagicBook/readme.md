# Bamboofox 2017 MagicBook

呢條係好簡單嘅heap overflow題,本身就應該solve到既(可惜揾錯one gadget RCE address),係到要推介下hitcon david 大大嘅 [One_gadget](https://github.com/david942j/one_gadget) ,

有佢就唔洗係IDA Pro 揾(錯) one gadget RCE 

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
0x603010:	0x0000000000400826	0x0000000000603030
0x603020:	0x0000000000000000	0x0000000000000021
0x603030:	0x4141414141414141	0x000000000000000a
0x603040:	0x0000000000000000	0x0000000000020fc1
0x603050:	0x0000000000000000	0x0000000000000000
0x603060:	0x0000000000000000	0x0000000000000000
0x603070:	0x0000000000000000	0x0000000000000000

```



