import oper

from utils import ft_error

class X:

	def __init__(self, factor=1.0, power=1.0):
		self.factor = factor
		self.power = power
		self.left = None
		self.right = None
		self.oper = ''

	def _oper(self):
		factor = str(int(self.factor)) if not self.factor % 1 else self.factor
		power = str(int(self.power)) if not self.power % 1 else self.power
		if not int(power): return str(factor)
		if int(power) == 1:
			if int(factor) == 1:
				return "X"
			else:
				return f"{factor} * X"
		elif int(power) < 0:
			if int(factor) == 1:
				return f"X^({power})"
			else:
				return f"{factor} * X^({power})"
		else:
			if int(factor) == 1:
				return f"X^{power}"
			else:
				return f"{factor} * X^{power}"

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
		if isinstance(other, X):
			new_obj = X()
			new_obj.factor = self.factor / other.factor
			new_obj.power = self.power - other.power
			return new_obj
		if isinstance(other, float):
			self.factor = self.factor / other
			return self
		ft_error("Equation non reductible et non solvable.")
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
		if self.power < 0:
			return f"{self.factor} * X^({self.power})"
		else:
			return f"{self.factor} * X^{self.power}"

	def __repr__(self):
		return self.__str__()