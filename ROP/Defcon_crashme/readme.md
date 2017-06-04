From IDA pro,we know that, we have to enter this string:

Smash me outside, how bout dAAAAAAAAAAA

with 39 length to the question, the function will scan the inputed string,if it contain this,

jump to return 

make use of the crashoff function from GDB,

we merged the pattern with the generated one

and obtained crashoff =72

$ebp+8 is the return address

set break point to the return,

use info reg

we can see that rdi register currently pointed to the string we entered

use ROPGadget to search 'jmp rdi'

construct our exploit as

shellcode+string+junk make it to 72+gadget address

exploit
