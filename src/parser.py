import ply.yacc as yacc


def build_parser():
	# ..
	return yacc.yacc()


def p_error(p):
	p.success = False
	print("Syntax Error!", p)


if __name__ == "__main__":
	print()
	