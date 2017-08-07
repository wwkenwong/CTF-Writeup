# BugsBunnyCTF 2017 rev150

呢題其實唔難,不過可能有太多io,所以angr解唔到

Ida Code:

```C++

  {
    if ( !numeric(argv[1]) )
      puts(4803080LL);
    if ( (unsigned __int8)ksjqdh(argv[1])
      && (unsigned __int8)uiyzr(argv[1])
      && (unsigned __int8)qdsdqq(argv[1])
      && (unsigned __int8)euziry(argv[1])
      && (unsigned __int8)mlhkjg(argv[1])
      && (unsigned __int8)sndsqd(argv[1])
      && (unsigned __int8)toyiup(argv[1])
      && (unsigned __int8)huhgeg(argv[1])
      && (unsigned __int8)nvjfkv(argv[1])
      && (unsigned __int8)jncsdkjf(argv[1])
      && (unsigned __int8)ieozau(argv[1])
      && (unsigned __int8)jqsgdd(argv[1])
      && (unsigned __int8)msdlmkfd(argv[1])
      && (unsigned __int8)nhdgrer(argv[1])
      && (unsigned __int8)fs546sdf(argv[1])
      && (unsigned __int8)sdff564sd(argv[1])
      && (unsigned __int8)sdff564s(argv[1])
      && (unsigned __int8)sdff564s7(argv[1])
      && (unsigned __int8)sdff564s8(argv[1])
      && (unsigned __int8)sdff564(argv[1])
      && (unsigned __int8)sdff564g5(argv[1])
      && (unsigned __int8)sdff564g8(argv[1])
      && (unsigned __int8)sdff564k3(argv[1]) )
    {
      v3 = argv[1];
      printf(40);
    }
    
```

支flag要satisfy呢n個 check statement 

當然就z3見

```
sat
[p = 7,
 k = 9,
 n = 9,
 d = 1,
 e = 3,
 j = 7,
 o = 5,
 i = 5,
 s = 1,
 b = 2,
 f = 7,
 l = 0,
 q = 8,
 a = 4,
 g = 2,
 r = 8,
 t = 2,
 c = 8,
 h = 4,
 m = 3]
```
flag:BugsBunny{42813724579039578812}


# Remark

1.睇其他writeup先發現可以咁入constraint ....

```python
for i in range(20):
	
	s.append(Int('s['+str(i)+']')) 

```

2.Bitvec is for register ~~~~~~

