"""A SAV file library for Python.

Eventually this will let you edit all files easily, for right now you won't get easy access to RTC data."""

class SAVFileBank:
	def __init__(self,sav,bank,data):
		self.sav = sav
		self.bank = bank
		self.data = data

	def __getitem__(self,k):
		return self.data[k]

	def __setitem__(self,k,v):
		self.data[k] = v
		self.sav.updateFromBank(self.bank,self.data)

class SAVFile:
	BANKS = 0
	ADDRESS = 1
	def __init__(self,filename="",banks=4,mbc=1):
		self.data = []
		self.banks = banks
		self.mode = self.BANKS
		if filename:
			self.load(filename)
		else:
			if mbc==1:
				self.data = [0xFF] * (banks*0x2000)

	def load(self,filename):
		with open(filename,"rb") as f:
			self.data = list(bytearray(f.read()))

	def output(self,filename):
		with open(filename,"wb") as f:
			f.write(bytearray(self.data))

	def __getitem__(self,k):
		if type(k)!=int:
			return -1
		if self.mode == self.BANKS:
			offset = k*0x2000
			return SAVFileBank(self,k,self.data[offset:offset+0x2000])
		else:
		 	return self.data[k]

	def __setitem__(self,k,v):
		if type(k)!=int:
			return
		self.data[k] = v

	def updateFromBank(self,bank,data):
		offset = bank * 0x2000
		self.data[offset:offset+0x2000] = data
