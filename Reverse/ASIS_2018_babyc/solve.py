import angr
proj = angr.Project('./patched_bin', auto_load_libs=False)
target=[0x804a6fc]
avoid=[0x804aa08]
st = proj.factory.entry_state()

for _ in xrange(31):
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
st.posix.files[0].length = 32


pg = proj.factory.path_group(st)
pg.explore(find=target,avoid=avoid)

print pg.found
#Ah_m0vfu3c4t0r!    0y1ng:(@_ @4@
print pg.found[0].posix.dumps(0)
#ASIS{574a1ebc69c34903a4631820f292d11fcd41b906}
