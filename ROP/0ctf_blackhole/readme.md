# Black Hole Theory - 250pts

題目:
>
>Can get the flag from a [black hole](blackhole.tar.gz)?
>
>By the way, here is a so called [return-to-csu](https://www.blackhat.com/docs/asia-18/asia-18-Marco-return-to-csu-a-new-method-to-bypass-the-64-bit-Linux-ASLR.pdf) method which you may want to know :P
>(though personally thought this should be well-known in 2018)
>
>202.120.7.203:666
>
>In memory of Stephen William Hawking (1942–2018).


呢條係比賽solve唔到,之後睇其他writeup 加返d sleep上去就run到 .....

其實我本身個solution都唔太可能solve得切,因為要brute force 一個半byte = 16^3

Total =flag length * 16^3 * printable ascii char

呢題係Defcon Qual 2017 mute翻版,有seccomp, no output

```
#  line  CODE  JT   JF      K
# =================================
#  0000: 0x20 0x00 0x00 0x00000004  A = arch
#  0001: 0x15 0x00 0x0d 0xc000003e  if (A != ARCH_X86_64) goto 0015
#  0002: 0x20 0x00 0x00 0x00000000  A = sys_number
#  0003: 0x35 0x0b 0x00 0x40000000  if (A >= 0x40000000) goto 0015
#  0004: 0x15 0x09 0x00 0x00000000  if (A == read) goto 0014
#  0005: 0x15 0x08 0x00 0x00000003  if (A == close) goto 0014
#  0006: 0x15 0x07 0x00 0x0000000a  if (A == mprotect) goto 0014
#  0007: 0x15 0x06 0x00 0x0000003c  if (A == exit) goto 0014
#  0008: 0x15 0x05 0x00 0x000000e7  if (A == exit_group) goto 0014
#  0009: 0x15 0x00 0x05 0x00000002  if (A != open) goto 0015
#  0010: 0x20 0x00 0x00 0x0000001c  A = args[1] >> 32
#  0011: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0015
#  0012: 0x20 0x00 0x00 0x00000018  A = args[1]
#  0013: 0x15 0x00 0x01 0x00000000  if (A != 0x0) goto 0015
#  0014: 0x06 0x00 0x00 0x7fff0000  return ALLOW
#  0015: 0x06 0x00 0x00 0x00000000  return KILL


```
題目有一個bof, 可以用黎read ROP gadget,trigger mprotect 改變bss由 rw->rwx, input shellcode 去read flag

由於seccomp ban左 write, 所以要用side channel attack leak flag

gadget 主要都係用 csu gadget (universal gadget)


呢條其實唔洗brute force ASLR都solve到, 因為alarm libc implementation 係用 syscall,

而read 會將input length pass 入eax,只要read 10 byte ->EAX /RAX = 0xa -> syscall 0xa ==mprotect

少改一下defcon mute d shellcode-> input shellcode to known bss->leak flag

[solve.py](solve.py)


