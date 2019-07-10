import sys
import re

from collections import deque
from math import sqrt

from utils import dic_precedence, ft_error
from X_class import X
from oper import Operator


class Equation:
	"""
	Class used to parse the equation given as argument to our program.

	Class attributes:
		- None

	Object attributes:
		- equation_str : the input string (argument to the program)
		- tree : parsed tree corresponding to the equation
	"""

	def __init__(self, line='', flag_h=False, flag_t=False, flag_n=False, flag_v=False):
		self.eq_init = ''
		self.equation_str = line
		self.tree = []
		self.tree_for_printing = None

		self.reduced_elem = {}
		self.reduced_str = ''
		self.new_reduced_str= ''

		self.max_degree = 0
		self.min_degree = 0
		self.delta = None
		self.delta_str = ''
		self.solution1 = None
		self.solution1_str = ''
		self.solution2 = None
		self.solution2_str = ''

		self.flag_h = flag_h
		self.flag_t = flag_t
		self.flag_n = flag_n
		self.flag_v = flag_v

	def parsing_errors(self):
		if not self.equation_str:
			ft_error("Syntax error : please provide a valid equation.")
		self.eq_init = self.equation_str
		self.equation_str = self.equation_str.replace(' ', '')
		if '=' not in self.equation_str:
			ft_error("Syntax error : please provide a valid equation.")

		dic_error = {
			r"(^=|=$|=.*=)": "Syntax error : please provide a valid equation.",
			r"[^X\+0-9\(\)=\^\*\-\./]": "Syntax error : unauthorized token in equation.",
			r"(^[\*\^/]|=[\*\^/])": "Syntax error : first element is a wrong operator (ony + and - allowed)",
			r"[\*\^/\+\-=]$": "Syntax error : last element is not a valid token to end the equation.",
			r"(\.[^0-9]|[^0-9]\.)": "Syntax error : need a digit before and after a dot.",
			r"([0-9]X|X[0-9])": "Syntax error : an operator has to precede or succeed an X element.",
			r"([=\(\-\+\^\*/][\*/\^]|[\*\^\+\-/\(]=|[\-\+\^\*/][\+\-\*/\^])":
				"Syntax error : two operators side by side which cannot be combined.",
			r"\(\)": "Syntax error : empty parentheses.",
			r"(\([^\)]*=|.*=[^\(]*\))": "Syntax error : error in parentheses.",
		}

		for k, v in dic_error.items():
			reg = re.compile(k)
			if reg.search(self.equation_str):
				ft_error(v)

		# if re.search(r"(^=|=$|=.*=)", self.equation_str):
		# 	ft_error("Syntax error : please provide a valid equation.")
		# if re.search(r"[^X\+0-9\(\)=\^\*\-\.]", self.equation_str):
		# 	ft_error("Syntax error : unauthorized token in equation.")
		# if re.search(r"(^[\*\^/]|=[\*\^/])", self.equation_str):
		# 	ft_error("Syntax error : first element is a wrong operator (ony + and - allowed)")
		# if re.search(r"[\*\^/\+\-=]$", self.equation_str):
		# 	ft_error("Syntax error : last element is not a valid token to end the equation.")
		# if re.search(r"(\.[^0-9]|[^0-9]\.)", self.equation_str):
		# 	ft_error("Syntax error : need a digit before and after a dot.")
		# if re.search(r"([0-9]X|X[0-9])", self.equation_str):
		# 	ft_error("Syntax error : an operator has to precede or succeed an X element.")
		# if re.search(r"([=\(\-\+\^\*/][\*/\^]|[\*\^\+\-/\(]=|[\-\+\^\*/][\+\-\*/\^])", self.equation_str):
		# 	ft_error("Syntax error : two operators side by side which cannot be combined.")
		# if re.search(r"\(\)", self.equation_str):
		# 	ft_error("Syntax error : empty parentheses.")
		# if re.search(r"(\([^\)]*=|.*=[^\(]*\))", self.equation_str):
		# 	ft_error("Syntax error : error in parentheses.")

		return None

	def build_trees(self):
		"""Method which builds the left and right trees from the input string, using a syntactic binary tree"""
		operator_stack = deque()
		list_eq = self.equation_str.split('=')[0] + '-' + '(' + self.equation_str.split('=')[1] + ')'
		list_eq = list_eq.replace('(+', '(0+').replace('(-', '(0-')
		j = 0
		while j < len(list_eq):
			n = ''
			while j < len(list_eq) and ('0' <= list_eq[j] <= '9' or list_eq[j] == '.'):
				n = n + list_eq[j]
				j += 1
			if n:
				j -= 1
				self.tree.append(X(factor=float(n), power=0.0, flag_h=self.flag_h))
			elif list_eq[j] == 'X':
				self.tree.append(X(flag_h=self.flag_h))
			elif list_eq[j] in dic_precedence.keys():
				while operator_stack and operator_stack[-1] != '('\
						and dic_precedence[operator_stack[-1].oper] >= dic_precedence[list_eq[j]]:
					self.tree.append(operator_stack.pop())
				operator_stack.append(Operator(list_eq[j]))
			elif list_eq[j] == '(':
				operator_stack.append(list_eq[j])
			elif list_eq[j] == ')':
				while operator_stack and operator_stack[-1] != '(':
					self.tree.append(operator_stack.pop())
				if not operator_stack:
					ft_error("Error : mismatched parentheses.")
				if operator_stack[-1] == '(':
					operator_stack.pop()
			j += 1
		while operator_stack:
			if operator_stack[-1] == '(':
				ft_error("Error : mismatched parentheses.")
			else:
				self.tree.append(operator_stack.pop())

		return None

	@staticmethod
	def ft_print_tree(e, spacing='', right=False):
		if (isinstance(e, X) or isinstance(e, float)) and right:
			print(f"{spacing}  {e}")
			return
		elif (isinstance(e, X) or isinstance(e, float)) and not right:
			print(f"{spacing} |  {e}")
			return
		print(f"{spacing}  {e}")
		print(f"{spacing}  |_left : ")
		Equation.ft_print_tree(e.left, spacing + ' ')
		print(f"{spacing}  |_right : ")
		Equation.ft_print_tree(e.right, spacing + ' ', right=True)

	def ft_getdegree(self):
		for key in sorted(list(self.reduced_elem.keys())):
			if self.reduced_elem[key].factor != 0:
				self.max_degree = key
				break
		for k, v in self.reduced_elem.items():
			if k < self.min_degree and v.factor:
				self.min_degree = k
			if k > self.max_degree and v.factor:
				self.max_degree = k
		if not self.max_degree % 1:
			self.max_degree = int(self.max_degree)
		return None

	def reduced_equation_str(self):
		string = ''
		for i, e in enumerate(sorted(list(self.reduced_elem.keys()))):
			if self.flag_h and not self.reduced_elem[e].factor:
				continue
			if not self.reduced_elem[e].factor % 1:
				self.reduced_elem[e].factor = int(self.reduced_elem[e].factor)
			if not self.reduced_elem[e].power % 1:
				self.reduced_elem[e].power = int(self.reduced_elem[e].power)
			if i == 0:
				string += self.reduced_elem[e].__str__()
			else:
				string += ' + ' + self.reduced_elem[e].__str__()
		string += ' = 0'
		string = string.replace('+ -', '- ')
		if self.flag_h:
			string = string.replace(' * X^0', '').replace('X^1', 'X').replace('1 * ', '')
		if string == ' = 0': string = '0 = 0'

		return string

	def reduce_equation(self):

		def complete_newtree(new_tree, e):
			if isinstance(e, X):
				new_tree.append(e)
			elif isinstance(e, Operator):
				complete_newtree(new_tree, e.left)
				complete_newtree(new_tree, e.right)
			return None

		def reduce_intermediate():
			output_stack = deque()
			new_tree = deque()
			count = 0
			for i, e in enumerate(self.tree):
				if isinstance(e, float) or isinstance(e, X):
					output_stack.append(e)
				if isinstance(e, Operator):
					e.right = output_stack.pop()
					if not output_stack:
						e.left = X(factor=0, power=0, flag_h=self.flag_h)
					else:
						e.left = output_stack.pop()
					e.evaluate()
					if self.flag_v and i != len(self.tree) - 1:
						if not count:
							print("\nOperations carried out during tree traversal")
							print("=================================================")
							count = 1
						Equation.ft_print_tree(e)
						print("-------------------------------------------------")
					output_stack.append(e.value)
			if self.flag_t:
				self.tree_for_printing = e
			complete_newtree(new_tree, e.value)
			return new_tree

		def complete_dict(new_tree):
			count = 0
			for e in new_tree:
				if e.power not in self.reduced_elem.keys():
					self.reduced_elem[e.power] = e
				else:
					if self.flag_v:
						if not count:
							print("\nOperations carried out during final combination")
							print("=================================================")
							count = 1
						print(f"{self.reduced_elem[e.power]} + {e} = {self.reduced_elem[e.power] + e}")
						print("-------------------------------------------------")
					self.reduced_elem[e.power] = self.reduced_elem[e.power] + e
			return None

		new_tree = reduce_intermediate()
		complete_dict(new_tree)
		self.reduced_str = self.reduced_equation_str()
		self.ft_getdegree()
		return None

	def num_format(self, n=None):
		if n is not None:
			if isinstance(n, float) and not n % 1: n = int(n)
			n_str = f"{n:.3f}" if (isinstance(n, float) and self.flag_h) else f"{n}"
			return n_str

	def solve_equation(self):

		def deal_negatives():
			new_dico_elem = {}
			for k, v in self.reduced_elem.items():
				new_dico_elem[k - self.min_degree] = v * X(power=-self.min_degree, flag_h=self.flag_h)
			self.reduced_elem = new_dico_elem
			self.new_reduced_str = self.reduced_equation_str()
			self.ft_getdegree()
			print(
				"There is at least one degree strictly lower than 0. Therefore, we multiply each element by the lowest degree to try to solve this equation.")
			print(f"New reduced form : {self.new_reduced_str}")
			print(f"Polynomial degree of the new equation : {self.max_degree}")
			return None

		a = 0
		b = 0
		c = 0
		if self.flag_n:
			if self.min_degree < 0:
				deal_negatives()
		elif self.min_degree < 0:
			ft_error("There exists a degree strictly lower than 0. This cannot be solved. Use -n flag to try to solve this equation.")
		if self.max_degree > 2:
			ft_error("This equation is of a degree higher than 2. This algorithm is not built to solve it.")
		for k,v in self.reduced_elem.items():
			if k == 2:
				a = v.factor
			elif k == 1:
				b = v.factor
			elif k == 0:
				c = v.factor
		if not a and not b and not c:
			print("Always true. Infinity of possible values for X in the set of real numbers.")
			sys.exit(0)
		elif not a and not b and c:
			ft_error("Impossible equation.")
		elif (not a and b and not c) or (a and not b and not c):
			self.solution1 = 0
		elif not a and b and c:
			self.solution1 = -c / b
			self.solution1_str = f"X = -({self.num_format(c)}) / {self.num_format(b)} = {self.num_format(self.solution1)}"
		else:
			self.delta = b ** 2 - 4 * a * c
			self.delta_str = f"Δ = {self.num_format(b)}^2 - 4 * {self.num_format(a)} * {self.num_format(c)} = {self.num_format(self.delta)}"

			if self.delta == 0:
				self.solution1 = -b / (2 * a)
				self.solution1_str = f"X = -({self.num_format(b)}) / (2 * {self.num_format(a)}) = {self.num_format(self.solution1)}"

			elif self.delta > 0:
				sq_delta_pos = sqrt(self.delta)
				self.solution1 = (-b - sq_delta_pos) / (2 * a)
				self.solution2 = (-b + sq_delta_pos) / (2 * a)
				self.solution1_str = (f"X1 = (-({self.num_format(b)}) - sqrt({self.num_format(self.delta)}) / (2 * {a}) = "
				f"(- ({self.num_format(b)}) - {self.num_format(sq_delta_pos)} / (2 * {self.num_format(a)}) = {self.num_format(self.solution1)}")
				self.solution2_str = (f"X2 = (-({self.num_format(b)}) + sqrt({self.num_format(self.delta)}) / (2 * {self.num_format(a)}) = "
				f"(- ({self.num_format(b)}) + {self.num_format(sq_delta_pos)} / (2 * {self.num_format(a)}) = {self.num_format(self.solution2)}")

			elif self.delta < 0:
				sq_delta = sqrt(-self.delta)
				if not b:
					self.solution1 = f"(-i * {self.num_format(sq_delta)}) / {2 * a}"
					self.solution2 = f"(i * {self.num_format(sq_delta)}) / {2 * a}"
				else:
					self.solution1 = f"({self.num_format(-b)} - i * {self.num_format(sq_delta)}) / {self.num_format(2 * a)}"
					self.solution2 = f"({self.num_format(-b)} + i * {self.num_format(sq_delta)}) / {self.num_format(2 * a)}"
				self.solution1_str = (f"X1 = (-({self.num_format(b)}) - i * sqrt({self.num_format(-self.delta)}) / (2 * {self.num_format(a)}) "
				f"= {self.num_format(self.solution1)}")
				self.solution2_str = (f"X2 = (-({self.num_format(b)}) + i * sqrt({self.num_format(-self.delta)}) / (2 * {self.num_format(a)}) "
				f"= {self.num_format(self.solution2)}")

		return None

	def print_final_results(self):
		str1 = self.num_format(self.solution1)
		str2 = self.num_format(self.solution2)
		if self.delta is None:
			print("The unique solution to the selfuation is:")
			print(f"X = {str1}") if not self.flag_v else print(self.solution1_str)
		elif self.delta == 0:
			if self.flag_v: print(self.delta_str)
			print("Discriminant is null. There is one double solution :")
			print(f"X = {str1}") if not self.flag_v else print(self.solution1_str)
		elif self.delta > 0:
			if self.flag_v: print(self.delta_str)
			print("Discriminant is strictly positive. The two real solutions are:")
			print(f"X1 = {str1}\nX2 = {str2}") if not self.flag_v else print(f"{self.solution1_str}\n{self.solution2_str}")
		elif self.delta < 0:
			if self.flag_v: print(self.delta_str)
			print("Discriminant is strictly negative. The two complex solutions are:")
			print(f"X1 = {str1}\nX2 = {str2}") if not self.flag_v else print(f"{self.solution1_str}\n{self.solution2_str}")
		print('')

		return None




