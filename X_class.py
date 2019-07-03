import oper

class X:

	def __init__(self, factor=1.0, power=1.0):
		self.factor = factor
		self.power = power

	def __add__(self, other):
		if isinstance(other, X) and other.power == self.power:
			new_obj = X()
			new_obj.factor = other.factor + self.factor
			new_obj.power = self.power
			return new_obj
		if (isinstance(other, X) and not other.factor) or not other:
			return self
		elif not self.factor:
			return other
		o = oper.Operator('+')
		o.left = self
		o.right = other
		return o

	def __radd__(self, other):
		return self + other

	def __sub__(self, other):
		new_obj = X()
		if isinstance(other, X) and other.power == self.power:
			new_obj.factor = self.factor - other.factor
			new_obj.power = self.power
			return new_obj
		if (isinstance(other, X) and not other.factor) or not other:
			return self

	def __rsub__(self, other):
		return self - other

	def __mul__(self, other):
		if isinstance(other, X):
			new_obj = X()
			new_obj.factor = self.factor * other.factor
			new_obj.power = self.power + other.power
			return new_obj
		if isinstance(other, float):
			self.factor *= other
			return self
		o = oper.Operator('*')
		o.left = self
		o.right = other
		return o

	def __rmul__(self, other):
		return self * other

	def __truediv__(self, other):
		if isinstance(other, X):
			new_obj = X()
			new_obj.factor = self.factor / other.factor
			new_obj.power = self.power - other.power
			return new_obj
		if isinstance(other, float):
			self.factor = self.factor / other
			return self
		o = oper.Operator('/')
		o.left = self
		o.right = other
		return o

	def __rtruediv__(self, other):
		return self / other

	def __pow__(self, other):
		new_obj = X()
		if isinstance(other, float):
			new_obj.factor = self.factor ** other
			new_obj.power = self.power * other
			return new_obj

	def __eq__(self, other):
		if isinstance(other, X) and other.power == self.power and other.factor == self.factor:
			return True
		return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __gt__(self, other):
		if isinstance(other, X):
			if self.power > other.power:
				return True
			elif self.power == other.power:
				return self.factor > other.factor
		return False

	def __lt__(self, other):
		if isinstance(other, X):
			if self.power < other.power:
				return True
			elif self.power == other.power:
				return self.factor < other.factor
		return False

	def __str__(self):
		return f"{self.factor} * X^{self.power}"

	def __repr__(self):
		return self.__str__()