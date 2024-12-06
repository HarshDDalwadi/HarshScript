from constants import *
from Number import *

class RTResult:
	def __init__(self):
		self.value = None
		self.error = None

	def register(self, res):
		if(res.error): self.error = res.error
		return res.value

	def success(self, value):
		self.value = value
		return self

	def failure(self, error):
		self.error = error
		return self

class Interpreter:
	def visit(self, node, context):
		method_name = f'visit_{type(node).__name__}'
		# visit_BinOpNode
		# visit_NumNode
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)
	
	def no_visit_method(self, node, context):
		raise Exception(f'No visit_{type(node).__name__} method defined')
	
	def visit_NumberNode(self, node, context):
		return RTResult().success(Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end))

	def visit_BinOpNode(self, node, context):
		res = RTResult()
		left = res.register(self.visit(node.left_node, context))
		if(res.error): return res
		right = res.register(self.visit(node.right_node, context))
		if(res.error): return res

		if(node.op_token.type == TT_PLUS):
			result, error = left.added_to(right)

		elif(node.op_token.type == TT_MINUS):
			result, error = left.subbed_by(right)

		elif(node.op_token.type == TT_MUL):
			result, error = left.multed_by(right)

		elif(node.op_token.type == TT_DIV):
			result, error = left.dived_by(right)
		
		elif(node.op_token.type == TT_POW):
			result, error = left.powed_by(right)

		if(error):
			return res.failure(error)
		return res.success(result.set_pos(node.pos_start, node.pos_end))

	def visit_UnaryOpNode(self, node, context):
		res = RTResult()
		number = res.register(self.visit(node.node, context))
		if(res.error): return res
		error = None
		if(node.op_token.type == TT_MINUS):
			number, error = number.multed_by(Number(-1))
		
		if(error):
			return res.failure(error)
		return res.success(number.set_pos(node.pos_start, node.pos_end))
	