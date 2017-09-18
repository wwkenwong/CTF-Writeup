# CSAW 2017 pwn 100 scv

# 題目:


>                                         SCV
>            SCV is too hungry to mine the minerals. Can you give him some food?
>                                 nc pwn.chal.csaw.io 3764

>[scv](scv)
>[ibc-2.23.so](ibc-2.23.so)


呢題有少少煩

IO dump:

```
-------------------------
[*]SCV GOOD TO GO,SIR....
-------------------------
1.FEED SCV....
2.REVIEW THE FOOD....
3.MINE MINERALS....
-------------------------
>>

```

有3個function:

1.入buffer

2.print buffer

3.exit

