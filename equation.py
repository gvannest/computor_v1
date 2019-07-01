import sys

from collections import deque

from settings import dic_precedence
from X_class import X

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
		self.tree = deque()


	def build_trees(self):
		"""Method which builds the left and right trees from the input string, using a syntactic binary tree"""
		trees = [deque(),deque()]
		operator_stack = deque()
		list_eq = [self.equation_str.split('=')[0], self.equation_str.split('=')[1]]
		list_eq[1] = '-' + '(' + list_eq[1] + ')'
		for i in range(2):
			j = 0
			while j < len(list_eq[i]):
				n = ''
				while j < len(list_eq[i]) and ('0' <= list_eq[i][j] <= '9' or list_eq[i][j] == '.'):
					n = n + list_eq[i][j]
					j += 1
				if n:
					j -= 1
					trees[i].append(X(factor=float(n), power=0))
				elif list_eq[i][j] == 'X':
					trees[i].append(X())
				elif list_eq[i][j] in dic_precedence.keys():
					while operator_stack and operator_stack[-1] != '('\
							and dic_precedence[operator_stack[-1]] >= dic_precedence[list_eq[i][j]]:
						trees[i].append(operator_stack.pop())
					operator_stack.append(list_eq[i][j])
				elif list_eq[i][j] == '(':
					operator_stack.append(list_eq[i][j])
				elif list_eq[i][j] == ')':
					while operator_stack and operator_stack[-1] != '(':
						trees[i].append(operator_stack.pop())
					if not operator_stack:
						print("Error : mismatched parentheses.")
						sys.exit(0)
					if operator_stack[-1] == '(':
						operator_stack.pop()
				j += 1
			while operator_stack:
				if operator_stack[-1] == '(':
					print("Error : mismatched parentheses.")
					sys.exit(0)
				else:
					trees[i].append(operator_stack.pop())

		self.tree = trees[0].extend(trees[1])

		return None


	def reduce_equation(self):
		trees = [deque(),deque()]





