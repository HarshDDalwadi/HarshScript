from Position import *
from constants import *
from Errors import *
from Token import *

class Lexer:
	def __init__(self, fn, text):
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)
		self.current_char = None
		self.fn = fn
		self.advance()
	
	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

	def make_tokens(self):
		tokens = []
		while (self.current_char != None):
			if(self.current_char in '\t '):
				self.advance()
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char in LETTERS:
				tokens.append(self.make_identifier())
			elif self.current_char == '+':
				tokens.append(Token(TT_PLUS, pos_start = self.pos))
				self.advance()
			elif self.current_char == '-':
				tokens.append(Token(TT_MINUS, pos_start = self.pos))
				self.advance()
			elif self.current_char == '*':
				tokens.append(Token(TT_MUL,pos_start = self.pos))
				self.advance()
			elif self.current_char == '/':
				tokens.append(Token(TT_DIV, pos_start = self.pos))
				self.advance()
			elif self.current_char == '^':
				tokens.append(Token(TT_POW, pos_start = self.pos))
				self.advance()
			elif self.current_char == '=':
				tokens.append(Token(TT_EQ, pos_start = self.pos))
				self.advance()
			elif self.current_char == '(':
				tokens.append(Token(TT_LPAREN, pos_start = self.pos))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(TT_RPAREN, pos_start = self.pos))
				self.advance()
			else:
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
				
		tokens.append(Token(TT_EOF, pos_start=self.pos))
		return tokens, None
	
	def make_number(self):
		num_str = ''
		dot_count = 0
		pos_start = self.pos.copy()

		while(self.current_char != None and self.current_char in DIGITS + '.'):
			if(self.current_char == '.'):
				if(dot_count == 1): break
				dot_count += 1
				num_str += '.'
			else:
				num_str += self.current_char
			self.advance()
			
		if dot_count == 0:
			return Token(TT_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

	def make_identifier(self):
		id_str = ''
		pos_start = self.pos.copy()

		while(self.current_char != None and self.current_char in LETTERS_DIGITS + '_'):
			id_str += self.current_char
			self.advance()

		tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
		return Token(tok_type, id_str, pos_start, self.pos)