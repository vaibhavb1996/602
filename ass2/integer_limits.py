#Copyright 2018 Vaibhav Bansal vbansal@bu.edu
def unsigned_int(bytes):
	number=(2**(bytes*8))-1
	return number

def min_signed(bytes):
	number=-1*(2**((bytes*8)-1))
	return number

def max_signed(bytes):
	number=2**((bytes*8)-1)-1
	return number

if __name__=='__main__':
	Table = "{:<6} {:<22} {:<22} {:<22}"
	print(Table.format('Bytes','Largest Unsigned Int','Minimum Signed Int','Maximum Signed Int'))
	i=1
	while i<9:
		print(Table.format(i,unsigned_int(i),min_signed(i),max_signed(i)))
		i=i+1

