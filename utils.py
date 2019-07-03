import sys

dic_precedence = {
	'+': 5,
	'-': 5,
	'*': 6,
	'/': 7,
	'^': 8,
	'=': 9,
}


def ft_error(message):
	print(message)
	sys.exit(0)