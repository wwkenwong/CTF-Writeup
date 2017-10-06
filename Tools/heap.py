import subprocess
import re
from gdb import *


#from https://youtu.be/qFyoWH_5Clo?t=2827
#source heap.py
#ph command addr

chunkptr=lookup_type('struct malloc_chunk').pointer()

class PrintHeap(Command):

	def __init__(self):
		super (PrintHeap, self).__init__("ph",COMMAND_USER)

	def printchunk(self,addr):
		chunk=addr.cast(chunkptr).dereference()
		prevsize=chunk['prev_size']
		size=chunk['size']
		fd=chunk['fd']
		bk=chunk['bk']
		print ('Chunk @ 0x%x' % (addr))

		if size&1:
			print('    prevsize: (inuse)')
		else:
			print('    prevsize:  %d (0x%x)' % (prevsize,prevsize))
		print('    size: %d (0x%x)'%(size&~7,size))
		print('    fd: 0x%x' % (fd))
		print('    bk: 0x%x' % (bk))
		return chunk

	def printheap(self,addr):
		while True:
			chunk=self.printchunk(addr)
			print('')
			size=chunk['size']&~7
			if size>10000:
				break
			addr+=size

	def printbin(self,addr):
		b=addr.cast(chunkptr).dereference()
		chunk=b['fd']
		while chunk !=addr:
			chunk=self. printchunk(chunk)['fd']
		print ('')


	def invoke(self, arg, from_tty):
		args=arg.split()
		cmd=args[0]
		if len(args)>1:
			addr=parse_and_eval(args[1])
		if cmd=='chunk':
			self.printchunk(addr)
		elif cmd=='mem':
			self.printchunk(addr-16)
		elif cmd=='heap':
			self.printheap(addr)

		##for printing bin informations
		elif cmd=='bin':   
			self.printheap(addr)












