import sys

dic_precedence = {
	'+': 5,
	'*': 6,
	'/': 7,
	'-': 8,
	'^': 9,
	'=': 10,
}


def ft_error(message):
	print(message)
	sys.exit(0)