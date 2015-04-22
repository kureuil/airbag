from enum import Enum

class ExitStatus(Enum):
	ok = 1			# Program executed, finished & passed tests
	finished = 2	# Program executed, finished but didn't pass tests
	killed = 3		# Program executed and didn't finish
	timeout = 4		# Program executed and didn't finish due to timeout
	noexec = 5		# Program didn't execute