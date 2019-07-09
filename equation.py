import sys

from collections import deque
from math import sqrt

from utils import dic_precedence, ft_error
from X_class import X
from oper import Operator
from visu import printBTree


class Equation:
	"""
	Class used to parse the equation given as argument to our program.

	Class attributes:
		- None

	Object attributes:
		- equation_str : the input string (argument to the program)
		- tree : parsed tree corresponding to the equation
	"""

	def __init__(self, line='', flag_h=False, flag_v=False, flag_n=False):
		self.eq_init = ''
		self.equation_str = line
		self.tree = []
		self.reduced_elem = {}
		self.reduced_str = ''
		self.new_reduced_str= ''
		self.max_degree = 0
		self.min_degree = 0
		self.delta = None
		self.solution1 = None
		self.solution2 = None
		self.flag_h = flag_h
		self.flag_v = flag_v
		self.flag_n = flag_n

	def parsing_errors(self):
		if '=' not in self.equation_str:
			ft_error("Syntax error : please provide a valid equation.")
		self.eq_init = self.equation_str
		self.equation_str = self.equation_str.replace(' ','')
		permission = set([e for e in dic_precedence.keys()] + [')', '(', 'X', '.'])
		if self.equation_str[0] == '*' or self.equation_str[0] == '/':
			ft_error("Syntax error : first element is a wrong operator (ony + and - allowed)")
		for i in range(len(self.equation_str)):
			if self.equation_str[i] not in permission and not self.equation_str[i].isdigit():
				ft_error("Syntax error : unauthorized token in equation.")
			if i < len(self.equation_str) - 1:
				if (self.equation_str[i] == '.' and not self.equation_str[i + 1].isdigit())\
					or (self.equation_str[i + 1] == '.' and not self.equation_str[i].isdigit()):
					ft_error("Syntax error : need a digit before and after a dot.")
				if self.equation_str[i] in dic_precedence.keys() and self.equation_str[i + 1] in dic_precedence.keys():
					if not (self.equation_str[i] == '=' and self.equation_str[i + 1] in ['+', '-']):
						ft_error("Syntax error : two operators side by side which cannot be combined.")
				if self.equation_str[i] in ['('] and self.equation_str[i + 1] in dic_precedence.keys():
					if not self.equation_str[i + 1] in ['+', '-', '=']:
						ft_error("Syntax error : two operators side by side which cannot be combined.")
			else:
				if self.equation_str[i] in dic_precedence.keys() or self.equation_str[i] == '.':
					ft_error("Syntax error : last element is not a valid token to end the equation.")
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
				self.tree.append(X(factor=float(n), power=0.0))
			elif list_eq[j] == 'X':
				self.tree.append(X())
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

	def ft_getdegree(self):
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

		def ft_print_tree(e, spacing=''):
			if isinstance(e, X):
				print(f"{spacing} {e}")
				return
			print(f"{spacing} {e}")
			print(f"{spacing} -> left : ")
			ft_print_tree(e.left, spacing + ' ')
			print(f"{spacing} -> right : ")
			ft_print_tree(e.right, spacing + ' ')

		def reduce_intermediate():
			output_stack = deque()
			new_tree = deque()
			for e in self.tree:
				if isinstance(e, float) or isinstance(e, X):
					output_stack.append(e)
				if isinstance(e, Operator):
					e.right = output_stack.pop()
					if not output_stack:
						e.left = X(factor=0, power=0)
					else:
						e.left = output_stack.pop()
					e.evaluate()
					output_stack.append(e.value)
			if self.flag_v:
				ft_print_tree(e)
				printBTree(e, lambda n: (n._oper(), n.left, n.right))
			complete_newtree(new_tree, e.value)
			return new_tree

		def complete_dict(new_tree):
			for e in new_tree:
				if e.power not in self.reduced_elem.keys():
					self.reduced_elem[e.power] = e
				else:
					self.reduced_elem[e.power] = self.reduced_elem[e.power] + e
			return None

		new_tree = reduce_intermediate()
		complete_dict(new_tree)
		self.reduced_str = self.reduced_equation_str()
		self.ft_getdegree()
		return None

	def solve_equation(self):
		a = 0
		b = 0
		c = 0
		if self.flag_n:
			if self.min_degree < 0:
				new_dico_elem = {}
				for k,v in self.reduced_elem.items():
					new_dico_elem[k - self.min_degree] = v * X(power=-self.min_degree)
				self.reduced_elem = new_dico_elem
				self.new_reduced_str = self.reduced_equation_str()
				self.ft_getdegree()
				print("There is at least one degree strictly lower than 0. Therefore, we multiply each element by the lowest degree to try to solve this equation.")
				print(f"New reduced form : {self.new_reduced_str}")
				print(f"Polynomial degree of the new equation : {self.max_degree}")
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
		else:
			self.delta = b ** 2 - 4 * a * c
			if self.delta == 0:
				self.solution1 = -b / (2 * a)
			elif self.delta > 0:
				self.solution1 = (-b - sqrt(self.delta)) / (2 * a)
				self.solution2 = (-b + sqrt(self.delta)) / (2 * a)
			elif self.delta < 0:
				if not self.flag_h:
					self.solution1 = f"({b} - i * {sqrt(-self.delta)}) / {2 * a}"
					self.solution2 = f"({b} + i * {sqrt(-self.delta)}) / {2 * a}"
				elif not b:
					self.solution1 = f"(-i * {sqrt(-self.delta):.2f}) / {2 * a}"
					self.solution2 = f"(i * {sqrt(-self.delta):.2f}) / {2 * a}"
				else:
					self.solution1 = f"({b} - i * {sqrt(-self.delta):.2f}) / {2 * a}"
					self.solution2 = f"({b} + i * {sqrt(-self.delta):.2f}) / {2 * a}"
		if isinstance(self.solution1, float) and not self.solution1 % 1:
			self.solution1 = int(self.solution1)
		if self.solution2 and isinstance(self.solution2, float) and not self.solution2 % 1:
			self.solution2 = int(self.solution2)
		return None






