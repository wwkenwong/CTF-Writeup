# VXCTF 2nd Flag Checking Oracle 2


# 題目:

>Flag Checking Oracle 2
>Last time there is a bug in our flag checking oracle. This time the bug is fixed, what can you do? Hahahaaa
>
>
>[fco_v2.0.py](fco_v2.0.py)


題目好簡單,不過係打script麻煩d

睇code大概知道

1.如果input length 等於flag length,會多左0.5秒sleeping time

2.每中一隻字,會roughly 多0.5秒sleeping time


經過出題人少少提示,我發現原來pwntools有計latency嘅tools,經過幾次trial and error就開始send server 

等大約個半鐘就有flag

# Code:

[solve.py](solve.py)
