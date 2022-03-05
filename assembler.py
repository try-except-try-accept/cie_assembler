from config import *




class Assembler:



	def __init__(self):
		self.ram = [0 for i in range(RAM_SIZE)]
		self.acc = 0
		self.ix = 0
		self.pc = 0
		self.status = [0, 0]  # compare result / interrupt detected
		self.end = False
		self.symbols = {}

	def validate_address(self, address):
		if address > RAM_WIDTH - 1:
			raise self.AssemblyException("Address {address} exceeds size of RAM")


	def get_value(self, mode, value):
		# 0 mode - address
		# 1 mode - literal
		# 2 mode - indirect
		# 3 mode - indexed

		if type(value) is not int:
			value = self.symbols[value]

		if mode == 0:
			self.validate_address(value)
			return self.ram[value]

		elif mode == 1:
			return value

		elif mode == 2:
			self.validate_address(value)
			new_address = self.ram[value]
			self.validate_address(new_address)
			return self.ram[new_address]

		elif mode == 3:
			new_address = value + self.ix
			self.validate_address(new_address)
			return self.ram[new_address]

	def load(self, mode, value):
		"""Implement various load functionality"""

		if mode == 1:
			# Immediate addressing. Load the number n to ACC
			self.acc = value
		elif mode == 0:
			# Direct addressing. Load the contents of the location at the given address to
			# ACC
			self.acc = self.ram[value]
		elif mode == 2:
			# Indirect addressing. The address to be used is at the given address. Load the
			# contents of this second address to ACC
			self.acc = self.ram[self.ram[value]]
		elif mode == 3:
			# Indexed addressing. Form the address from <address> + the contents of the
			# index register. Copy the contents of this calculated address to ACC
			self.acc = self.ram[value + self.ix]
		elif mode == 4:
			# Immediate addressing. Load the number n to IX
			self.ix = value

	def move(self, register):
		"""Move the contents of the accumulator to the given register (IX)"""

		## NOTE: does not make sense to parameterise this instruction given that
		## the only possible arg is IX.
		self.ix = self.acc

	def store(self, register):
		"""Store the contents of ACC at the given address"""

		self.ram[register] = self.acc

	def add(self, mode, value):
		"""Add the contents of the given address to the ACC / Add the number n to the
		ACC"""
		value = self.get_value(mode, value)
		self.acc += value

	def subtract(self, mode, value):
		"""Subtract the contents of the given address to the ACC / Subtract the number n to the
		ACC"""
		value = self.get_value(mode, value)
		self.acc -= value

	def increment(self, mode):
		"""Add 1 to the contents of the register (ACC or IX)"""
		# 0 mode - accumulator
		# 1 mode - index register

		if mode == 0:
			self.acc += 1
		else:
			self.ix += 1

	def decrement(self, mode):
		"""Subtract 1 from the contents of the register (ACC or IX)"""
		# 0 mode - accumulator
		# 1 mode - index register

		if mode == 0:
			self.acc -= 1
		else:
			self.ix -= 1

	def jump(self, mode, address):
		"""Jump to the given address / Following a compare instruction, jump to <address> if the compare was
		True / Following a compare instruction, jump to <address> if the compare was False"""

		# 0 mode - jump always
		# 1 mode - jump if true
		# 2 mode - jump if false

		if mode == 0:
			self.pc = address
		elif mode == 1 and self.status[0]:
			self.pc = address
		elif not(self.status[0]):
			self.pc = address

	def compare(self, mode, value):
		"""Compare the contents of ACC with the contents of <address> /
		Compare the contents of ACC with number n /
		Indirect addressing. The address to be used is at the given address. Compare the
contents of ACC with the contents of this second address"""

		value = self.get_value(mode, value)

		if self.acc == value:
			self.status[0] == 1
		else:
			self.status[0] == 0

	def input(self, value):
		"""Key in a character and store its ASCII value in ACC"""
		self.acc = value

	def output(self):
		"""Output to the screen the character whose ASCII value is stored in ACC"""
		return self.acc

	def end(self):
		"""Return control to the operating system"""
		self.end = True

	def bitwise_and(self, mode, value):

		value = self.get_value(mode, value)

		self.acc = self.acc & value











