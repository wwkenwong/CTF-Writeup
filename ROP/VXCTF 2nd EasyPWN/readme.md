# VXCTF 2nd EasyPWN

# 題目:


>EasyPWN1
>Easiest pwn in the world!
>
>[bof](bof)




呢題係今次vxctg 嘅sanity check題,


首先ida左佢,


```C++

int __cdecl main(int argc, const char **argv, const char **envp)
{
  be_nice_to_people();
  vulnerable_function();
  write(1, "Hello, World\n", 0xDuLL);
  return 0;
}

```

有個vulnerable_function():

```C++

ssize_t vulnerable_function()
{
  char buf; // [sp+0h] [bp-80h]@1

  return read(0, &buf, 256uLL);
}

```

read buf 有bof

Function list 有一個not_called()

```C++

int not_called()
{
  return system("/bin/bash");
}
```

只要將ret addr 指向呢個function 就get shell

# Solution:

[solve.py](solve.py)


