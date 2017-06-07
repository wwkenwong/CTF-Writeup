import angr
 

#can be start at 40102c rather than 1029
#because it is jmp step 
#.text:0000000000401029  cmp     eax, 2
#.text:000000000040102C  jnz     short loc_401035
#start = 0x401029
start = 0x40100c #the start point of the function,but slower
#start = 0x400f0a # Where the path begin
end = 0x40105D   # Where we want to go
explode = (0x401035,0x401058) # The addresses of explosions

proj = angr.Project('./bomb', load_options={'auto_load_libs':False}) # load the binary

state = proj.factory.blank_state(addr=start) # Create the path

# Push the 2 digit returned by our scanf.
for i in xrange(2):
    state.stack_push(state.se.BVS('int_{}'.format(i), 4*8)) 

# Create and explore the function
path = proj.factory.path_group(state)
ex = path.explore(find=end, avoid=explode)

if ex.found:
    found = ex.found[0].state

    answer = []

    # Pop 3 64bit integer from the stack
    # we will convert it to 32 bit values
    # 1 64bit integer is 2 number
    # pop 3 mean out put 6
    for x in xrange(3):
        curr_int = found.se.any_int(found.stack_pop())

        answer.append(str(curr_int & 0xffffffff))
        answer.append(str(curr_int >> 32))

    print(" ".join(answer))