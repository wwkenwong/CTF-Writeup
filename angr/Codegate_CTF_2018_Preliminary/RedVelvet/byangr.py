#using posix for question input with fgets ...
import angr
proj = angr.Project('./RedVelvet', auto_load_libs=False)
target=[0x00000000004015F9]
avoid=[0x4009f7,0x4009ed]
st = proj.factory.entry_state()

for _ in xrange(26):
    k = st.posix.files[0].read_from(1)
    st.se.add(k != 0)
    st.se.add(k != 10)
    st.se.add(k>=0x20)
    st.se.add(k<=0x7e)

#constraint last byte as "\n" 
k = st.posix.files[0].read_from(1)
st.se.add(k == 10)


#constraint size as 27
st.posix.files[0].seek(0)
st.posix.files[0].length = 27


pg = proj.factory.path_group(st)
pg.explore(find=target,avoid=avoid)

print pg.found

print pg.found[0].posix.dumps(0)



# will got this :What_You_Wanna_Be?:)_lc_la\n  but has got one successful run with What_You_Wanna_Be?:)_la_la\n , probably the int overflow issue in func14 affected the sat solver
