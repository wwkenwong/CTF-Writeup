```x86
   0x00000000004006a6 <+0>:	push   rbp
   0x00000000004006a7 <+1>:	mov    rbp,rsp
   0x00000000004006aa <+4>:	sub    rsp,0x70
   0x00000000004006ae <+8>:	mov    QWORD PTR [rbp-0x68],rdi
   0x00000000004006b2 <+12>:	mov    rax,QWORD PTR fs:0x28
   0x00000000004006bb <+21>:	mov    QWORD PTR [rbp-0x8],rax
   0x00000000004006bf <+25>:	xor    eax,eax
   0x00000000004006c1 <+27>:	movabs rax,0x797472657771275f
   0x00000000004006cb <+37>:	mov    QWORD PTR [rbp-0x30],rax
   0x00000000004006cf <+41>:	movabs rax,0x73617d7b706f6975
   0x00000000004006d9 <+51>:	mov    QWORD PTR [rbp-0x28],rax
   0x00000000004006dd <+55>:	movabs rax,0x7a6c6b6a68676664
   0x00000000004006e7 <+65>:	mov    QWORD PTR [rbp-0x20],rax
   0x00000000004006eb <+69>:	movabs rax,0x7c6d6e62766378
   0x00000000004006f5 <+79>:	mov    QWORD PTR [rbp-0x18],rax
   0x00000000004006f9 <+83>:	mov    DWORD PTR [rbp-0x5c],0x0
   0x0000000000400700 <+90>:	jmp    0x400777 <validate+209>
   0x0000000000400702 <+92>:	mov    eax,DWORD PTR [rbp-0x5c]
   0x0000000000400705 <+95>:	movsxd rdx,eax
   0x0000000000400708 <+98>:	mov    rax,QWORD PTR [rbp-0x68]
   0x000000000040070c <+102>:	add    rax,rdx
=> 0x000000000040070f <+105>:	movzx  eax,BYTE PTR [rax]
   0x0000000000400712 <+108>:	cmp    al,0x5e
   0x0000000000400714 <+110>:	jle    0x40072a <validate+132>
   0x0000000000400716 <+112>:	mov    eax,DWORD PTR [rbp-0x5c]
   0x0000000000400719 <+115>:	movsxd rdx,eax
   0x000000000040071c <+118>:	mov    rax,QWORD PTR [rbp-0x68]
   0x0000000000400720 <+122>:	add    rax,rdx
   0x0000000000400723 <+125>:	movzx  eax,BYTE PTR [rax]
   0x0000000000400726 <+128>:	cmp    al,0x7d
   0x0000000000400728 <+130>:	jle    0x400734 <validate+142>
   0x000000000040072a <+132>:	mov    edi,0x0
   0x000000000040072f <+137>:	call   0x400590 <exit@plt>
   0x0000000000400734 <+142>:	mov    DWORD PTR [rbp-0x58],0x0
   0x000000000040073b <+149>:	jmp    0x40076d <validate+199>
   0x000000000040073d <+151>:	mov    eax,DWORD PTR [rbp-0x58]
   0x0000000000400740 <+154>:	movsxd rdx,eax
   0x0000000000400743 <+157>:	mov    rax,QWORD PTR [rbp-0x68]
   0x0000000000400747 <+161>:	add    rdx,rax
   0x000000000040074a <+164>:	mov    eax,DWORD PTR [rbp-0x58]
   0x000000000040074d <+167>:	movsxd rcx,eax
   0x0000000000400750 <+170>:	mov    rax,QWORD PTR [rbp-0x68]
   0x0000000000400754 <+174>:	add    rax,rcx
   0x0000000000400757 <+177>:	movzx  eax,BYTE PTR [rax]
   0x000000000040075a <+180>:	movsx  eax,al
   0x000000000040075d <+183>:	sub    eax,0x5f
   0x0000000000400760 <+186>:	cdqe   
   0x0000000000400762 <+188>:	movzx  eax,BYTE PTR [rbp+rax*1-0x30]
   0x0000000000400767 <+193>:	mov    BYTE PTR [rdx],al
   0x0000000000400769 <+195>:	add    DWORD PTR [rbp-0x58],0x1
   0x000000000040076d <+199>:	cmp    DWORD PTR [rbp-0x58],0x17
   0x0000000000400771 <+203>:	jle    0x40073d <validate+151>
   0x0000000000400773 <+205>:	add    DWORD PTR [rbp-0x5c],0x1
   0x0000000000400777 <+209>:	cmp    DWORD PTR [rbp-0x5c],0x2
   0x000000000040077b <+213>:	jle    0x400702 <validate+92>
   0x000000000040077d <+215>:	movabs rax,0x7b646e6a7d756d7a
   0x0000000000400787 <+225>:	mov    QWORD PTR [rbp-0x50],rax
   0x000000000040078b <+229>:	movabs rax,0x7b6f646e5f667b6f
   0x0000000000400795 <+239>:	mov    QWORD PTR [rbp-0x48],rax
   0x0000000000400799 <+243>:	movabs rax,0x61677b5f7a685f7b
   0x00000000004007a3 <+253>:	mov    QWORD PTR [rbp-0x40],rax
   0x00000000004007a7 <+257>:	mov    BYTE PTR [rbp-0x38],0x0
   0x00000000004007ab <+261>:	mov    DWORD PTR [rbp-0x54],0x0
   0x00000000004007b2 <+268>:	jmp    0x4007e0 <validate+314>
   0x00000000004007b4 <+270>:	mov    eax,DWORD PTR [rbp-0x54]
   0x00000000004007b7 <+273>:	movsxd rdx,eax
   0x00000000004007ba <+276>:	mov    rax,QWORD PTR [rbp-0x68]
   0x00000000004007be <+280>:	add    rax,rdx
   0x00000000004007c1 <+283>:	movzx  edx,BYTE PTR [rax]
   0x00000000004007c4 <+286>:	mov    eax,DWORD PTR [rbp-0x54]
   0x00000000004007c7 <+289>:	cdqe   
   0x00000000004007c9 <+291>:	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
   0x00000000004007ce <+296>:	cmp    dl,al
   0x00000000004007d0 <+298>:	je     0x4007dc <validate+310>
   0x00000000004007d2 <+300>:	mov    edi,0x0
   0x00000000004007d7 <+305>:	call   0x400590 <exit@plt>
   0x00000000004007dc <+310>:	add    DWORD PTR [rbp-0x54],0x1
   0x00000000004007e0 <+314>:	cmp    DWORD PTR [rbp-0x54],0x18
   0x00000000004007e4 <+318>:	jle    0x4007b4 <validate+270>
   0x00000000004007e6 <+320>:	mov    edi,0x400be4
   0x00000000004007eb <+325>:	call   0x400540 <puts@plt>
   0x00000000004007f0 <+330>:	nop
   0x00000000004007f1 <+331>:	mov    rax,QWORD PTR [rbp-0x8]
   0x00000000004007f5 <+335>:	xor    rax,QWORD PTR fs:0x28
   0x00000000004007fe <+344>:	je     0x400805 <validate+351>
   0x0000000000400800 <+346>:	call   0x400550 <__stack_chk_fail@plt>
   0x0000000000400805 <+351>:	leave  
   0x0000000000400806 <+352>:	ret 
   
   ```
   
   ```c
   __int64 __fastcall validate(__int64 a1)
{
  signed int i; // [sp+14h] [bp-5Ch]@1
  signed int j; // [sp+18h] [bp-58h]@5
  signed int k; // [sp+1Ch] [bp-54h]@10
  __int64 v5; // [sp+20h] [bp-50h]@10
  __int64 v6; // [sp+28h] [bp-48h]@10
  __int64 v7; // [sp+30h] [bp-40h]@10
  char v8; // [sp+38h] [bp-38h]@10
  __int64 v9; // [sp+40h] [bp-30h]@1
  __int64 v10; // [sp+48h] [bp-28h]@1
  __int64 v11; // [sp+50h] [bp-20h]@1
  __int64 v12; // [sp+58h] [bp-18h]@1
  __int64 v13; // [sp+68h] [bp-8h]@1

  v13 = *MK_FP(__FS__, 40LL);
  v9 = 0x797472657771275FLL;
  v10 = 0x73617D7B706F6975LL;
  v11 = 0x7A6C6B6A68676664LL;
  v12 = 0x7C6D6E62766378LL;
  for ( i = 0; i <= 2; ++i )
  {
    if ( *(_BYTE *)(i + a1) <= 94 || *(_BYTE *)(i + a1) > 125 )
      exit(0);
    for ( j = 0; j <= 23; ++j )
      *(_BYTE *)(a1 + j) = *((_BYTE *)&v9 + *(_BYTE *)(j + a1) - 95);
  }
  //zmu}jnd{o{f_ndo{{_hz_{ga
  //p $dl
  v5 = 0x7B646E6A7D756D7ALL;
  v6 = 0x7B6F646E5F667B6FLL;
  v7 = 0x61677B5F7A685F7BLL;
  v8 = 0;
  for ( k = 0; k <= 24; ++k )
  {
    if ( *(_BYTE *)(k + a1) != *((_BYTE *)&v5 + k) )
      exit(0);
  }
  puts("haha nice!");
  return *MK_FP(__FS__, 40LL) ^ v13;
}
```
