import angr
 
start = 0x401062 #start point of phase5
#start = 0x40107f #start point of phase5 no ok
end = 0x4010EE   # Where we want to go
explode = (0x401084,0x4010C6) # The addresses of explosions


proj = angr.Project('./bomb', load_options={'auto_load_libs':False}) # load the binary

state = proj.factory.blank_state(addr=start) # Create the path
password_addr = 0x100 # The arbitrary address of the string
password_lenght = 6   # The lenght of the string
password = state.se.BVS('password', password_lenght*8) #We create the symbolic bitvector string

state.memory.store(password_addr, password) # We store the BVS at the arbitrary address

# We set the constraint of printable chars to the input.
for i in xrange(password_lenght):
    m = state.memory.load(password_addr + i, 1)
    state.add_constraints(m >= 0x20)
    state.add_constraints(m <= '}')

# We put the strings in register
state.regs.rdi = password_addr

# Create and explore the function
path = proj.factory.path_group(state)
ex = path.explore(find=end, avoid=explode)

if ex.found:
    found = ex.found[0].state
    
    res = found.se.any_str(password) # Print the result string

    print(res)
