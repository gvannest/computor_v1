from collections import deque

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

	def __init__(self, line='', flag=False):
		self.equation_str = line
		self.tree = []
		self.reduced_tree = deque()
		self.reduced_str = ''
		self.flag_h = flag

	def parsing_errors(self):
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
			else:
				if self.equation_str[i] in dic_precedence.keys() or self.equation_str[i] == '.':
					ft_error("Syntax error : last element is not a valid token to end the equation.")
		return None

	def build_trees(self):
		"""Method which builds the left and right trees from the input string, using a syntactic binary tree"""
		self.tree = deque()
		operator_stack = deque()
		if '=' in self.equation_str:
			list_eq = self.equation_str.split('=')[0] + '-' + '(' + self.equation_str.split('=')[1] + ')'
		else:
			list_eq = self.equation_str
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
					if e.oper == '-':
						e.right = -1.0 * e.right
						e.oper = '+'
					e.evaluate()
					output_stack.append(e.value)
					# ft_print_tree(e.value)
					# print('')
			# ft_print_tree(e.value)
			complete_newtree(new_tree, e.value)
			return sorted(new_tree)

		def reduce_final(new_tree):
			self.reduced_tree = []
			tmp_list = []
			if len(new_tree) == 1:
				self.reduced_tree.append(new_tree[0])
				return None
			for e in new_tree:
				if len(tmp_list) < 1:
					tmp_list.append(e)
				elif len(tmp_list) == 1:
					tmp_list.append(e)
					o = Operator('+')
					o.right = tmp_list.pop()
					o.left = tmp_list.pop()
					o.evaluate()
					if isinstance(o.value, X):
						tmp_list.append(o.value)
					else:
						self.reduced_tree.append(o.left)
						tmp_list.append(o.right)
			while tmp_list:
				self.reduced_tree.append(tmp_list.pop())
			return None

		def reduced_equation():
			for i,e in enumerate(self.reduced_tree):
				if not e.factor % 1:
					e.factor = int(e.factor)
				if not e.power % 1:
					e.power = int(e.power)
				self.reduced_str += e.__str__()
				if i != len(self.reduced_tree) - 1:
					self.reduced_str += ' + '
				else:
					self.reduced_str += ' = 0'
			self.reduced_str = self.reduced_str.replace('+ -', '- ')
			if self.flag_h:
				self.reduced_str = self.reduced_str.replace(' * X^0', '').replace('X^1', 'X').replace('1 * ', '')
			return None

		new_tree = reduce_intermediate()
		print(new_tree)
		reduce_final(new_tree)
		reduced_equation()

		return None


