import angr
 
#start_addr=0x400efc
target_addr=0x400f3c
avoid_addr=0x40143a
explode=(0x400f10,0x400f20)

start = 0x400f0a
#start = 0x400f0a # Where the path begin
end = 0x400f3c   # Where we want to go
explode = (0x400f10, 0x400f20) # The addresses of explosions

proj = angr.Project('./bomb', load_options={'auto_load_libs':False}) # load the binary

state = proj.factory.blank_state(addr=start) # Create the path

# Push the 6 digit returned by our read_six_numbers function.
for i in xrange(6):
    state.stack_push(state.se.BVS('int_{}'.format(i), 4*8)) 

# Create and explore the function
path = proj.factory.path_group(state)
ex = path.explore(find=end, avoid=explode)

if ex.found:
    found = ex.found[0].state

    answer = []

    # Pop 3 64bit integer from the stack
    # we will convert it to 32 bit values

    for x in xrange(3):
        curr_int = found.se.any_int(found.stack_pop())

        answer.append(str(curr_int & 0xffffffff))
        answer.append(str(curr_int >> 32))

    print(" ".join(answer))