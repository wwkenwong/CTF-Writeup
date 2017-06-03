

high
------------------------
|    bin/sh           | argument
------------------------
|    AAAA             | calling convention(pass an invalid return address to faciliate a call)
------------------------
|    System           | return to function 
------------------------
|     AAAA            | overwrite old ebp
------------------------<------ebp
|  AAAAAAAAAAAAAAAAAAA|
------------------------  total 136
|  AAAAAAAAAAAAAAAAAAA|
------------------------
|  AAAAAAAAAAAAAAAAAAA|
------------------------<------esp
low



write from low address to high address
