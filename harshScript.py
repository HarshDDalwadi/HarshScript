from Errors import *
from Lexer import *
from Interpreter import *
from Parser import *
from constants import *
from Context import *

def run(fn, text):
	lexer = Lexer(fn, text)
	tokens, error = lexer.make_tokens()
	if(error):
		return None, error
	# Generate AST
	parser = Parser(tokens)
	ast = parser.parse()

	if(ast.error) : return None, ast.error

	#Run Program
	interpreter = Interpreter()
	context = Context('<program>')
	result = interpreter.visit(ast.node, context)

	return result.value, result.error
