import sys

dic_precedence = {
	'+': 3,
	'*': 4,
	'/': 4,
	'-': 8,
	'^': 9,
	'=': 10,
}


def ft_error(message):
	print(message)
	sys.exit(0)