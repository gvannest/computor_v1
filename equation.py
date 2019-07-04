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
		self.tree = None
		self.reduced_tree = deque()
		self.reduced_str = ''
		self.flag_h = flag

	def parsing_errors(self):
		if '=' not in self.equation_str:
			ft_error("Syntax error : please provide a valid equation.")
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
					if not (self.equation_str[i] == '=' and self.equation_str[i + 1] in ['-']):
						ft_error("Syntax error : two operators side by side which cannot be combined.")
				if self.equation_str[i] in ['(', ')'] and self.equation_str[i + 1] in dic_precedence.keys():
					if not self.equation_str[i + 1] in ['-', '=']:
						ft_error("Syntax error : two operators side by side which cannot be combined.")
			else:
				if self.equation_str[i] in dic_precedence.keys() or self.equation_str[i] == '.':
					ft_error("Syntax error : last element is not a valid token to end the equation.")
		return None

	def build_tree(self):
		"""Method which builds the left and right trees from the input string, using a syntactic binary tree"""

		def ft_print_tree(e, spacing=''):
			for c in e:
				if isinstance(c, Operator):
					print(f"{spacing} {c.oper}")
					ft_print_tree(c.elements, spacing)
				else:
					print(f"{spacing} {c}")
					return

		def recursive_built(equation, o):
			if not equation:
				return o
			j = 0
			while j < len(equation):
				n = ''
				while j < len(equation) and ('0' <= equation[j] <= '9' or equation[j] == '.'):
					n = n + equation[j]
					j += 1
				if n:
					j -= 1
					o.elements.append(X(factor=float(n), power=0.0))
				elif equation[j] == 'X':
					o.elements.append(X())
				elif equation[j] in dic_precedence.keys():
					if equation[j] == o.oper:
						j += 1
						continue
					elif dic_precedence[o.oper] < dic_precedence[equation[j]]:
						o.elements.append(recursive_built(equation[j + 1:], Operator(equation[j])))
					else:
						new_oper = Operator(equation[j])
						new_oper.elements.append(o)
						return recursive_built(equation[j + 1:], new_oper)
				j += 1

			return o

		clean_eq = self.equation_str.split('=')[0] + '-' + '(' + self.equation_str.split('=')[1] + ')'
		self.tree = recursive_built(clean_eq, Operator('+'))
		print(self.tree.elements)
		ft_print_tree(self.tree.elements)
		return None
