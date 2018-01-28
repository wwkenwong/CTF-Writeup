# Insomni-hack teaser 2018 onecall

題目都話明係onecall,當然係要用one gadget rce做啦(????

不過因為係arm, 所以冇tools 直接output gadget


唔緊要我地可以撞(????????


拖個libc入ida,search "/bin/sh", 入到d code, xref到頂,由個堆addr 開始brute force

撞一個鐘就可以get shell

'''

flag: INS{did_you_gets_here_by_chance?}

'''


# Intended Solution

1. https://ntropy-unc.github.io/exploit/pwn/gets/rop/aarch64/arm/magic/gadget/writeup/post/2018/01/21/OneCall.html

2. https://gist.github.com/cosine0/97151015512872a84ac164547410a9e0

