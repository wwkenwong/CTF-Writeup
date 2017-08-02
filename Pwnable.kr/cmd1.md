   
[cmd1] 

```C++

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "flag")!=0;
	r += strstr(cmd, "sh")!=0;
	r += strstr(cmd, "tmp")!=0;
	return r;
}

```
cmd1@ubuntu:~$ ./cmd1 "/bin/cat *"

mommy now I get what PATH environment is for :)
