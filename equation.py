import sys

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

	def __init__(self, line):
		self.equation_str = line
		self.tree = []
		self.reduced_tree = deque()

	def build_trees(self):
		"""Method which builds the left and right trees from the input string, using a syntactic binary tree"""
		self.tree = deque()
		operator_stack = deque()
		list_eq = self.equation_str.split('=')[0] + '-' + '(' + self.equation_str.split('=')[1] + ')'
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

		def reduce_intermediate():
			output_stack = deque()
			new_tree = deque()
			for e in self.tree:
				if isinstance(e, float) or isinstance(e, X):
					output_stack.append(e)
				if isinstance(e, Operator):
					e.right = output_stack.pop()
					e.left = output_stack.pop()
					if e.oper == '-':
						e.right = -1.0 * e.right
						e.oper = '+'
					e.evaluate()
					print(e.oper)
					print(e.left)
					print(e.right)
					print(e.value)
					if not isinstance(e.value, X):
						if e.left and isinstance(e.left, X):
							new_tree.append(e.left)
						if e.right and isinstance(e.right, X):
							new_tree.append(e.right)
					output_stack.append(e.value)
			return sorted(new_tree)

		def reduce_final(new_tree):
			self.reduced_tree = []
			tmp_list = []
			if len(new_tree) == 1:
				self.reduced_tree.append(new_tree[1])
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
					if o.value:
						tmp_list.append(o.value)
					else:
						self.reduced_tree.append(o.left)
						tmp_list.append(o.right)

			while tmp_list:
				self.reduced_tree.append(tmp_list.pop())
			return None

		new_tree = reduce_intermediate()
		print(new_tree)
		reduce_final(new_tree)
		print(self.reduced_tree)
		return None


