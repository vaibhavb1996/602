# Copyright 2018 Vaibhav Bansal vbansal@bu.edu
# Copyright 2018 Ayush Shirsat ayush34@bu.edu
# Copyright 2018 Julie Park ysp599@bu.edu

class Polynomial:

    def __init__(self, value = None):
    	if value is None:
    		value = []
		dic = {}
		self.dic = dic
		for i, coeff in enumerate(value):
			self.dic[len(value) - 1 - i] = coeff	

    def __setitem__(self, key, value):
    	self.dic[key] = value

    def __getitem__(self, i):
    	if i in self.dic:
    		return self.dic[i]
		return 0

    def __str__(self):
    	return '{}'.format(self.dic.values())

    def __repr__(self):
		return str(self)

    def __eq__(self, other):
		if (self.dic == other.dic):
			return True
		return False
	
    def eval(self,value):
		result = 0
		for i in self.dic:
			result = result + (self.dic[i] * (value ** i))
		return result

    def __add__(self,other):
		addition = Polynomial([])
		addition.dic = {k: self[k] + other[k] for k in set(self.dic) | set(other.dic)}
		return addition

    def __sub__(self, other):
		subtraction = Polynomial([])
		subtraction.dic = {k: self[k] - other[k] for k in set(self.dic) | set(other.dic)}
		return subtraction

    def __mul__(self, other):
		product = Polynomial([])
		for sKey in self.dic:
			for oKey in other.dic:
				product.dic[sKey + oKey] = 0
		for sKey in self.dic:
			for oKey in other.dic:
				product.dic[oKey + sKey] = product.dic[oKey + sKey] + (self.dic[sKey] * other.dic[oKey])
		return product

    def deriv(self):
		der = Polynomial([])
		low = min(self.dic.keys())
		der.dic = self.dic.copy()
		for k in sorted(der.dic.keys()):
			if k != 0:
				if k != low:
					der.dic[k-1] = der.dic[k-1] + k * der.dic[k]
					der.dic[k]= 0
				else:
					der.dic[k-1] = k * der.dic[k]
					der.dic[k] = 0
			elif k == 0:
				der.dic[k] = 0 
		while der.dic[max(sorted(der.dic.keys()))] == 0:
			der.dic.pop(max(sorted(der.dic.keys())))
		return der	

def main():
	pass

if __name__ == '__main__':
	main()

