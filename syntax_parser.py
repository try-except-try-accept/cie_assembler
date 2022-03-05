


from config import *

class ParserException(Exception):
	pass

class Operation:

	# operand modes:

	# 0 address
	# 1 denary literal
	# 2 hex literal
	# 3 bin literal
	# 4 ACC
	# 5 IX
	def __init__(self, opcode, op_modes, den_code):
		self.code = opcode
		self.den_code = den_code
		self.op_modes = op_modes

	def set_operand(self, operand):
		if self.check_operand(operand):
			self.operand = operand
		else:
			raise ParserException(f"Operand {operand} invalid for opcode {self.code}.")

	def check_operand(self, operand):
		"""Check operand is valid for this operation"""
		if operand is None:
			return len(self.op_modes) == 0
		elif operand[0] == "#":
			return 1 in self.op_modes
		elif operand[0] == "&":
			return 2 in self.op_modes
		elif operand[0] == "B":
			return 3 in self.op_modes
		elif operand == "ACC":
			return 4 in self.op_modes
		elif operand == "IX":
			return 5 in self.op_modes
		elif operand.isdigit():
			return 0 in self.op_modes


	def to_denary(self):
		return self.den_code.zfill(OPCODE_DIGS) + str(self.den_literal).zfill(OPERAND_DIGS)



class Parser:




	def __init__(self, code=""):

		# opcode # operand mode

		# operand modes:

		# 0 address
		# 1 denary literal
		# 2 hex literal
		# 3 bin literal
		# 4 ACC
		# 5 IX

		self.valid_op_exceptions = ["ACC", "IX"]

		self.op_map = {"LDM":Operation("LDM", [1], "10"),
					   "LDD": Operation("LDD", [0], "11"),
					   "LDI": Operation("LDI", [0], "12"),
					   "LDX": Operation("LDX", [0], "13"),
					   "LDR": Operation("LDR", [1], "14"),
					   "MOV": Operation("MOV", [5], "20"),
					   "STO": Operation("STO", [0], "21"),
					   "ADD": Operation("ADD", [0, 1, 2, 3], "40"),
					   "SUB": Operation("SUB", [0, 1, 2, 3], "50"),
					   "INC": Operation("INC", [4, 5], "41"),
					   "DEC": Operation("DEC", [4, 5], "51"),
					   "JMP": Operation("JMP", [0], "60"),
					   "CMP": Operation("CMP", [0, 1], "70"),
					   "CMI": Operation("CMI", [0], "71"),
					   "JPE": Operation("JPE", [0], "61"),
					   "JPN": Operation("JPN", [0], "62"),
					   "IN": Operation("IN", [], "90"),
					   "OUT": Operation("OUT", [], "91"),
					   "END": Operation("END", [], "00"),
					   "AND": Operation("AND", [0, 1, 2, 3], "80"),
					   "OR": Operation("OR", [0, 1, 2, 3], "81"),
					   "XOR": Operation("XOR", [0, 1, 2, 3], "82"),
					   "LSL": Operation("LSL", [1], "30"),
					   "LSR": Operation("LSR", [1], "31")}

		print(list(self.op_map.keys()))

		self.symbols = {}
		self.code = code.replace("\t", " ").split("\n")
		self.first_pass()
		print("Symbol table created: ")
		print(self.symbols)
		self.second_pass()



	def first_pass(self):

		for line, instruction in enumerate(self.code):
			instruction = instruction.split()
			if ":" in instruction[0]:						# colon denotes a symbol is used
				symbol = instruction[0][:-1]				# remove colon from symbol name
				op = "#0"
				if len(instruction) > 1:
					op = instruction[1]							# opcode / operand is second token


				if op in self.op_map.keys():				# is symbol labelling an instruction?
					symbol_value = line
				else:
					symbol_value = self.validate_literal(op)

				self.validate_symbol(symbol)
				self.symbols[symbol] = symbol_value



	def second_pass(self):

		symbols = {}
		for line, instruction in enumerate(self.code):
			print(instruction)

			opcode, operand, symbol = None, None, None

			instruction = instruction.split()

			if len(instruction) == 1:							# if one token - opcode or blank symbol
				opcode = instruction[0]
				self.validate_opcode(opcode)

			elif len(instruction) == 2:
				if instruction[0] in self.op_map.keys():
					opcode, operand = instruction
				elif instruction[1] in self.op_map.keys():
					symbol, opcode = instruction
				else:
					print("Found symbol, operand")

					symbol, operand = instruction

			elif len(instruction) == 3:
				symbol, opcode, operand = instruction
				self.validate_opcode(opcode)

			else:
				raise ParserException(f"Line {line} contains {len(instruction)} tokens.")



			if symbol is not None:
				if symbol.replace(":", "") not in self.symbols.keys():
					raise ParserException(f"Unknown symbol: {symbol}")

			if opcode is not None:									# data labels (no opcodes)
				opcode = self.op_map[opcode]
				opcode.set_operand(operand)
				opcode.den_literal = self.validate_operand(operand)

				self.ram[self.pc] = opcode.to_denary()
				self.pc += 1


	def validate_symbol(self, symbol):
		if not symbol[0].isalpha():
			raise ParserException(f"Symbol identifier must begin with a letter: {symbol}")
		elif not symbol.isalnum():
			raise ParserException(f"Symbol identifier cannot contain special characters: {symbol}")
		elif symbol in self.symbols:
			raise ParserException(f"Symbol identifier already used: {symbol}")

	def validate_opcode(self, token):
		if token not in self.op_map.keys():
			raise ParserException(f"Invalid opcode: {token}")


	def validate_operand(self, token):

		if token == "0" or token is None:
			return 0

		symbol_value = self.symbols.get(token)

		if symbol_value is not None:												# check if token is symbol
			return symbol_value
		elif token in self.valid_op_exceptions:
			return token
		elif token.isdigit():														# check if token is address
			address = int(token)
			if address > RAM_SIZE - 1:
				raise ParserException(f"Address {address} exceeds size of RAM")
			else:
				return address
		else:																		# check if token is valid literal
			return self.validate_literal(token)




	def validate_literal(self, token):
		literal_id = token[0]
		base = {"#":10, "&":16, "B":2}.get(literal_id)

		if base is None:
			raise ParserException(f"Invalid literal id {literal_id} in token {token}")



		try:
			val = int(token[1:], base)
		except:
			raise ParserException(f"Token {val} is not a valid base {base} number.")

		if MIN_MEM_VALUE <= val <= MAX_MEM_VALUE:
			return val
		else:
			raise ParserException(f"Value {val} exceeds min / max possible.")








if __name__ == "__main__":

	from os import getcwd
	print(getcwd())

	passed = []
	failed = []

	with open(getcwd()+"/"+"opcodes_tests.txt", "r") as f:
		for line in f:
			if line.startswith("#"):
				continue
			print(line)
			desc, code, result = line.split("/")

			print("Testing:", desc)

			error = False

			try:
				Parser(code.replace(",", "\n"))
			except ParserException as e:
				print(e)
				error = True



			if result == "True" and error or result == "False" and not error:
				raise ParserException("Incorrect test result")



