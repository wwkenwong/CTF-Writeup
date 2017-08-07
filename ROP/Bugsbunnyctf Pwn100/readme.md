# Bugsbunnyctf Pwn100


```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
```

```
────────────────────────────────── Registers ───────────────────────────────────
EAX: 0xffffd1f0 ('A' <repeats 32 times>)
EBX: 0x0 
ECX: 0xfbad2288 
EDX: 0xf7fad87c --> 0x0 
ESI: 0x1 
EDI: 0xf7fac000 --> 0x1b2db0 
EBP: 0x41414141 ('AAAA')
ESP: 0xffffd210 --> 0x0 
EIP: 0x41414141 ('AAAA')
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)

Legend: code, data, rodata, heap, value
Stopped reason: SIGSEGV
0x41414141 in ?? ()
gdb-peda$ 
````



```
0x08048386 : call eax
```


