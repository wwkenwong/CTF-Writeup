# PlaidCTF 2018 Roll-a-d8

From the question : 

```
This might only be helpful to Google employees... or is it? https://crbug.com/821137
```

We can search for the regression test under v8 's repo, but we need to slightly modify the test before really can trigger crashes

You have to modify the maxsize (increase) before triggering the crash on the d8 engine with the regression test 

After triggering the bug , we can leak the address of the array buffer with the help of the oobArray :
![alt text](1.png)

The buffer address is highlighted in red,while yellow box if pointed to oobArray :
![alt text](2.png)

We can leak the jit address by place it inside a {}, since object inside would be align each other within the memory region

![alt text](3.png)

check under vmmap, we can see what we need is not within the rwx jit region:
![alt text](4.png)

Locate to it, we saw there is a pointer belongs to the rwx region
![alt text](5.png)

Locate that pointer , we saw something looks like instructions (red box):
![alt text](6.png)

We can trigger sigtrap by overwriting it with 0xcc:
![alt text](7.png)


Poped a xcalc :)
![alt text](8.png)


# Reference and other exploits

1. https://pastebin.com/gtJA92j8

2. https://gist.github.com/sroettger/d077d3907999aaa0f89d11d956b438ea

3. https://gist.github.com/saelo/52985fe415ca576c94fc3f1975dbe837

4. https://gist.github.com/itszn/73cc299b9bcff1ed585e6206d1ade58e



