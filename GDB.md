info reg

info functions

#for GOT table

$ objdump -d rop3-7f3312fe43c46d26 | grep ">:"

08048360 <read@plt>:

...

...

080483a0 <write@plt>:


#for offset

$ objdump -R rop3-7f3312fe43c46d26


DYNAMIC RELOCATION RECORDS

OFFSET   TYPE              VALUE

08049ff0 R_386_GLOB_DAT    __gmon_start__

0804a000 R_386_JUMP_SLOT   read

0804a004 R_386_JUMP_SLOT   getegid

0804a008 R_386_JUMP_SLOT   __gmon_start__

0804a00c R_386_JUMP_SLOT   __libc_start_main

0804a010 R_386_JUMP_SLOT   write

0804a014 R_386_JUMP_SLOT   setresgid


radare2->i check canary

check x/x $rbp and $rbp+4/+8
