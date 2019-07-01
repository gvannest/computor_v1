class X:

	def __init__(self, factor=1, power=1):
		self.factor = factor
		self.power = power

	def __str__(self):
		return f"{self.factor} * X ^ {self.power}"

	def __add__(self, other):
		new_obj = X()
		if isinstance(other, X) and other.power == self.power:
			new_obj.factor = other.factor + self.factor
			new_obj.power = self.power
		return new_obj

	def __sub__(self, other):
		new_obj = X()
		if isinstance(other, X) and other.power == self.power:
			new_obj.factor =  self.factor - other.factor
			new_obj.power = self.power
		return new_obj

	def __mul__(self, other):
		new_obj = X()
		if isinstance(other, X):
			new_obj.factor = self.factor * other.factor
			new_obj.power = self.power + other.power
		return new_obj

	def __div__(self, other):
		new_obj = X()
		if isinstance(other, X):
			new_obj.factor = self.factor / other.factor
			new_obj.power = self.power - other.power
		return new_obj

	def __pow__(self, other):
		new_obj = X()
		if isinstance(other, float):
			new_obj.factor = self.factor ** other
			new_obj.power = self.power * other.power
		return new_obj