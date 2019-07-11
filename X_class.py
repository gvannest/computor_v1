import oper

from utils import ft_error

class X:
	"""
	Class of the X elements form the equation

	class attributes:
		- flag_h : human_readable flag

	instance attributes:
		- factor : factor in front of X
		- power : degree of the X element

	instance methods:
		- mainly overcharge of operations operator to fi with X elements
	"""

	flag_h = False

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
		if isinstance(other, X) and other.power == self.power:
			new_obj = X()
			new_obj.factor = self.factor - other.factor
			new_obj.power = self.power
			return new_obj
		if (isinstance(other, X) and not other.factor) or not other:
			return self
		elif not self.factor:
			return -1.0 * other
		o = oper.Operator('+')
		o.left = self
		o.right = -1.0 * other
		return o

	def __rsub__(self, other):
		return -1.0 * self + other

	def __mul__(self, other):
		if isinstance(other, X):
			new_obj = X()
			new_obj.factor = self.factor * other.factor
			new_obj.power = self.power + other.power
			return new_obj
		if isinstance(other, float):
			self.factor *= other
			return self
		return other * self

	def __rmul__(self, other):
		return self * other

	def __truediv__(self, other):
		if isinstance(other, X) and not other.factor:
			ft_error("Error : division by zero.")
		if isinstance(other, X):
			new_obj = X()
			new_obj.factor = self.factor / other.factor
			new_obj.power = self.power - other.power
			return new_obj
		if isinstance(other, float):
			self.factor = self.factor / other
			return self
		ft_error("Equation non reductible and unsolvable.")
		return None

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
		str_factor = f"{self.factor:.2f}" if isinstance(self.factor, float) and X.flag_h else f"{self.factor}"
		str_power = f"{self.power:.2f}" if isinstance(self.power, float) and X.flag_h else f"{self.power}"
		if self.power < 0:
			return f"{str_factor} * X^({str_power})"
		else:
			return f"{str_factor} * X^{str_power}"

	def __repr__(self):
		return self.__str__()