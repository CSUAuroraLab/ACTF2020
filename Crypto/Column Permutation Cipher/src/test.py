#-*-coding=UTF-8*-*
from Cryptodome.Util.number import *
from math import *
book="""In computer security, Capture the Flag (CTF) is a computer security competition. CTF contests are usually designed to serve as an educational exercise to give participants experience in securing a machine, as well as conducting and reacting to the sort of attacks found in the real world.actf{Welcome_to_the_world_of_cryptography}. Reverse-engineering, network sniffing, protocol analysis, system administration, programming, and cryptanalysis are all skills which have been required by prior CTF contests at DEF CON. There are two main styles of capture the flag competitions: attack/defense and jeopardy."""
book=book.lower()
lenb=len(book)
line=ceil(sqrt(lenb))
book+=" "*(line-lenb%line)
cipher=""
for i in range(line):
    for j in range(line):
        cipher+=book[j*line+i]
print(cipher)
