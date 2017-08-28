# VXCTF 2nd Simple REVERSE

Question:

>Simple REVERSE
>Very simple!Just brute-force it!
>
>[rev](rev)


首先ida左佢

```C++
  scanf("%39s", &s, envp);
  if ( strlen(&s) > 0x26
    && v16 + 2 * s + 8 * v42 == 954
    && v12 + 2 * v5 + 2 * v16 == 416
    && s + 5 * v42 == 554
    && v37 + 3 * v20 - v39 == 137
    && v36 + v38 - v20 == 102
    && 2 * (v41 + v42 + v40) == 628
    && v26 + v24 + v14 - v32 == 180
    && v36 + v39 + v20 == 213
    && v10 - v27 + v30 == 66
    && 2 * v10 - v31 == 1
    && v23 + v41 == 210
    && v6 - v8 + v18 == 95
    && v7 + v28 == 228
    && v27 - v10 == 50
    && v19 + v5 + v39 == 335
    && v5 + 3 * v39 == 435
    && v19 - v5 + v28 == 131
    && v9 - v5 + v28 == 109
    && 2 * v39 + v32 == 320
    && 4 * v15 - v11 - v18 - v21 == 140
    && v8 + 3 * v33 == 437
    && v17 + v11 + v18 == 324
    && v22 + v33 == 218
    && v17 + v21 + v41 == 313
    && v11 + v41 == 209
    && v17 + v11 - v22 == 125
    && 3 * (v26 + v10) + v32 == 398
    && v22 + v10 + v26 == 204
    && v24 + v40 == 233
    && v11 - v22 == 6
    && v25 == v31
    && 2 * v24 - v10 == 190
    && v31 + 2 * v22 + 2 * v35 == 535
    && v35 + v22 + v36 == 271
    && v34 + v22 - v36 == 170
    && v29 - v34 + v36 == 51
    && v41 + v34 + v23 - v29 - 2 * v13 == 20
    && v34 + 2 * v13 - v23 - v41 == 97
    && v34 + 2 * v10 - v31 == 118 )
  {
    puts("Congratulations!");
    result = 0;
  }
  else
  {
    puts("Bye~");
    result = 0;
  }
  return result;
```

Condition 好簡單,只要入支岩嘅flag就會出configurations

咁就用z3 solver打constraint

solve完之後,harry大大就同我講原來配合global可以唔洗手打constraint -_-

呢到就紀錄底harry個solution

[solve.py](solve.py)
