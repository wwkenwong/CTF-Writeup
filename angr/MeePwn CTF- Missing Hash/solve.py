import angr
 
# load the binary into an angr project.
proj = angr.Project('crackme2_fix4.exe', load_options={"auto_load_libs": False})
# I'm going to skip all the beginning of the program.
state = proj.factory.entry_state(addr=0x004015B6)
 
# scanf() reads from stdin and stores it a this address
bind_addr = 0x040305A
# a symbolic input string with a length up to 10 bytes
input_string = state.se.BVS("input_string", 8 * 10)
# To be safe, I'm constraining input string. They are printable characters
for byte in input_string.chop(8):
  state.add_constraints(byte >= ' ') # '\x20'
  state.add_constraints(byte <= '~') # '\x7e'
  state.add_constraints(byte != 0) # null
 
# bind the symbolic string at bind_addr
state.memory.store(bind_addr, input_string)
 
# Attempt to find a path
path = proj.factory.path(state=state)
ex = proj.surveyors.Explorer(start=path, find=0x401B21, avoid=0x00401B1)
ex.run()
 
state = ex.found[0].state
# We know all the values at: 0x403040, 0x403042, 0x403044, 0x403046, 0x403048, 0x40304A, 0x40304C, 0x40304E, 0x403050
for i in range(18):
  state.add_constraints(state.memory.load(0x408040 + i, 1) == 0)
  # We know the flag starts with "Z" and ends with "!"
  state.add_constraints(state.memory.load(bind_addr + 9, 1) == '!')
  state.add_constraints(state.memory.load(bind_addr, 1) == 'Z')
 
print 'Found:', state.se.any_str(input_string)
# Zer0C0d3r!
# 2.7s
