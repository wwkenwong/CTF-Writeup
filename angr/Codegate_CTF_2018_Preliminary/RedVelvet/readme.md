


```python
>>> import angr
WARNING | 2018-02-05 10:40:47,352 | angr.analyses.disassembly_utils | Your verison of capstone does not support MIPS instruction groups.
>>> proj = angr.Project('./RedVelvet', auto_load_libs=False)
>>> simgr.explore(find=lambda s: "flag : {" in s.posix.dumps(1))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'simgr' is not defined
>>> simgr = proj.factory.simgr()
>>> simgr.explore(find=lambda s: "flag : {" in s.posix.dumps(1))
WARNING | 2018-02-05 10:42:22,015 | angr.engines.successors | Exit state has over 257 possible solutions. Likely unconstrained; skipping. <BV64 reg_28_4_64>
WARNING | 2018-02-05 10:46:39,689 | angr.state_plugins.symbolic_memory | Concretizing symbolic length. Much sad; think about implementing.
<SimulationManager with 63 deadended, 1 found (1 errored)>
>>> s 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 's' is not defined
>>> s.found
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 's' is not defined
>>> s = simgr.found[0]
>>> print s.posix.dumps(1)
Your flag : HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
HAPPINESS:)
flag : {" What_You_Wanna_Be?:)_lc_la "}

>>> flag = s.posix.dumps(0)
>>> print(flag)
What_You_Wanna_Be?:)_lc_la** ��J��??*JJ�*
�*JJJ�
        �*
>>> 
```
