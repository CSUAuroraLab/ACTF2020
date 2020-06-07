arr1 = [0, 15, 78, 6, 54, 27, 26, 14, 34, 92, 58, 68, 23, 133, 90, 79, 94, 93, 137, 26, 106, 97, 55, 91, 49, 103, 105, 54, 40, 37, 115]
arr2 = [-62, 80]


def decode(s, key):
	a = map(ord, s)
	enc = ''
	for i in range(len(key)):
		enc += chr(a[i] ^ ord(key[i]))
	return enc

def main():
	a = [(arr2[0] + arr2[1]) >> 1, (arr2[1] - arr2[0]) >> 1]
	s = ''
	for i in range(len(arr1)):
		s += chr((arr1[i] - i) ^ a[i % len(a)])
	key1 = '%$#@!'
	key2 = 'f1owe'
	key = (key2[2] + key1) * 2 + 'r' + (key2 + key1[4]) * 3
	flag = decode(s, key)
	print(flag)


main()

# flag{pre77y_pYth0n_&nd_f1ow3r*}