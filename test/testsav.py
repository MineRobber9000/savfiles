from __future__ import print_function
from sav import SAVFile,SAVFileBank

def section_title(name):
	print(name)
	print("-".join([""]*(len(name)+1)))

def assert_mod(test_name,cond,numtabs=2):
	print(test_name,end=":"+("\t"*numtabs))
	if cond:
		print("SUCCESS")
	else:
		print("FAILURE")

# From the above import statements to this comment is boilerplate for my custom test suite.
# Now for some helper functions!

def bank_and_address_to_offset(bank,address):
	return (bank*0x2000)+address

section_title("SAV File Library Tests:")

section_title("\"No predefined data\" tests:")

test = SAVFile()

assert_mod("SAV File starts in bank addressing mode",test.mode==SAVFile.BANKS)
assert_mod("Bank addressing mode results in Bank objects",test[0].__class__==SAVFileBank)
assert_mod("Data defaults to 0xFF for uninitialized data",test[0][0x0000]==255)

test[1][0x0000] = 0

assert_mod("Initialized data in banks is propagated",test.data[bank_and_address_to_offset(1,0x0000)]==0)

section_title("Same data type, but ADDRESS addressing mode:")

test.mode = SAVFile.ADDRESS

assert_mod("Address addressing mode does NOT result in Bank object",type(test[0])==int,1)

assert_mod("Uninitialized data defaults to 0xFF",test[bank_and_address_to_offset(3,0x0000)]==255,3)

section_title("\"With loaded data\" tests:")

test.mode = SAVFile.BANKS
test.load("test.sav")

assert_mod("01:A000 is 0xFF",test[1][0x0000]==255,5)
assert_mod("01:AD11 is 0xC3",test[1][0x0d11]==195,5)
