import angr
import simuvex


##begin= (since it is an argv passing,no need to include begin address)
avoid=0x400850
target=0x400830
str__len=0x43 

proj = angr.Project('unbreakable-enterprise-product-activation', load_options={"auto_load_libs": False})


#use claripy if is argv type passing
input_string = angr.claripy.BVS("input_string", 8 * str__len)

state = proj.factory.entry_state(args=["./unbreakable-enterprise-product-activation", input_string], add_options={simuvex.o.LAZY_SOLVES})

#By default there's only 60 symbolic bytes, which is too small for this case
#This region is tunable in case of any out bound error found
state.libc.buf_symbolic_bytes=str__len +1
#state.libc.buf_symbolic_bytes = 500


#Constraint to printable strings
for byte in input_string.chop(8):
  state.add_constraints(byte >= ' ') # '\x20'
  state.add_constraints(byte <= '~') # '\x7e'
  state.add_constraints(byte != 0) # null


path = proj.factory.path(state=state)

ex = proj.surveyors.Explorer(start=path, find=target, avoid=avoid)

ex.run()
 
state = ex.found[0].state

 
print 'Found:', state.se.any_str(input_string)
