from Errors import *
from Nodes import *
from constants import *

class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
	
	def register(self, res):
		if (isinstance(res, ParseResult)):
			if (res.error):
				self.error = res.error
			return res.node
		
		return res

	def success(self, node):
		self.node = node
		return self
	
	def failure(self, error):
		self.error = error
		return self


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.token_index = -1
		self.advance()
	
	def advance(self):
		self.token_index += 1
		if(self.token_index < len(self.tokens)):
			self.current_token = self.tokens[self.token_index]
		return self.current_token
	
	def parse(self):
		res = self.expression()
		if(not res.error and self.current_token.type != TT_EOF):
			return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected '+', '-', '*' or '/'"))
		return res
	
	def atom(self):
		res = ParseResult()
		token = self.current_token
		if token.type in (TT_INT, TT_FLOAT):
			res.register(self.advance())
			return res.success(NumberNode(token))
		elif token.type == TT_LPAREN:
			res.register(self.advance())
			expr = res.register(self.expression())
			if res.error: return res
			if self.current_token.type == TT_RPAREN:
				res.register(self.advance())
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))
		return res.failure(InvalidSyntaxError(token.pos_start, token.pos_end, "Expected int, float, '+', '-' or '('"))
	
	def power(self):
		return self.bin_op(self.atom, (TT_POW, ), self.factor)

	def factor(self):
		res = ParseResult()
		token = self.current_token
		if(token.type in (TT_PLUS, TT_MINUS)):
			res.register(self.advance())
			factor = res.register(self.factor())
			if(res.error): return res
			return res.success(UnaryOpNode(token, factor))

		return self.power()
	
	def term(self):
		return self.bin_op(self.factor, (TT_MUL, TT_DIV))

	def expression(self):
		return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

	def bin_op(self, func_a, ops, func_b = None):
		if(func_b == None): func_b = func_a
		res = ParseResult()
		left = res.register(func_a())
		if res.error : return res

		while(self.current_token.type in ops):
			op_token = self.current_token
			res.register(self.advance())
			right = res.register(func_b())
			if res.error : return res
			left = BinOpNode(left, op_token, right)

		return res.success(left)
	