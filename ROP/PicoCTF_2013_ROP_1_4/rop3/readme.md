
Firstly,use IDA pro check string, nothing can use


then gdb->crashoff-> A*140+ return address

We used write to print out the address of library function

then using debugger to check the offset

For function in the PLT , they have fixed address during runtime,
We just call the write(1,read,4)

there is an vulnerable function here, and we set it to return address of calling write to exploit the address

By using find /bin/sh <------- search /bin/sh first, then bin/sh  <important 

search runtime address by print system, print read etc to leak the address locally

calculate the offset

exploit with A*140+Sys+AAAA+'bin/sh'



Reference= https://github.com/ctfs/write-ups-2013/tree/master/pico-ctf-2013/rop-3


btw The fake return address can be anything, so I chose "\x00"*4 (remember an address is 4 bytes).

