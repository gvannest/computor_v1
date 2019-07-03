
import X_class


class Operator:
	"""
	Class of the operators elements form the equation

	class attributes:
		- None

	instance attributes:
		- oper : the operator symbol as str
		- left / right : the left and right elements of the operator
		- value : the value of the operator after evaluation. Either an X object or an Operator object

	instance methods:
		- evaluate : evaluates the operator expression
	"""

	def __init__(self, oper):
		self.oper = oper
		self.left = None
		self.right = None
		self.value = None

	def evaluate(self):

		def ft_check_powtype():
			if isinstance(self.left, X_class.X) and isinstance(self.left.power, X_class.X):
				self.left.power = float(self.left.power.factor)
			if isinstance(self.right, X_class.X) and isinstance(self.right.power, X_class.X):
				self.right.power = float(self.right.power.factor)
			return None

		def ft_plus():
			self.value = self.left + self.right

		def ft_minus():
			self.value = self.left - self.right

		def ft_mul():
			self.value = self.left * self.right

		def ft_div():
			self.value = self.left / self.right

		def ft_pow():
			if isinstance(self.right, X_class.X):
				self.right = float(self.right.factor)
			self.value = self.left ** self.right

		dic_oper = {
			'+': ft_plus,
			# '-': ft_minus,
			'*': ft_mul,
			'/': ft_div,
			'^': ft_pow,
		}

		ft_check_powtype()
		dic_oper[self.oper]()

		return None

	def __add__(self, other):
		if isinstance(other, X_class.X):
			return other + self
		return self.left + self.right + other.left + other.right

	def __pow__(self, other):
		if other == 1:
			return self
		elif isinstance(other, float):
				return self * self.__pow__(other - 1)

	def __mul__(self, other):
		if isinstance(other, X_class.X) or isinstance(other, float):
			return self.left * other + self.right * other
		return self.left * other.left + self.left * other.right + self.right * other.left + self.right * other.right

	def __rmul__(self, other):
		return self * other

	def __str__(self):
		return f"{self.oper}"

	def __repr__(self):
		return self.__str__()



