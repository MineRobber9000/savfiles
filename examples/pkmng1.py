import sav

class Inventory:
	def __init__(self,bank,offset,size):
		self.size = size
		self.offset = offset
		end = offset+2+(2*size)
#		print hex(end+0xa000)
		while bank[end]!=255:
			end += 1
		self.data = bank[offset:end]

	@property
	def amount_of_items(self):
		return self.data[0]

	@property
	def is_full(self):
		return self.amount_of_items==self.size

	def _locate_FF(self):
		ret = 1
		while ret<len(self.data) and self.data[ret]!=255:
			ret += 1
		return ret

	def add_item(self,id,quantity):
		self.data[0]=self.amount_of_items+1
		noffset = self._locate_FF()
		self.data[noffset]=id
		self.data[noffset+1]=quantity
		self.data[noffset+2]=0xFF

	def remove_item(self,id,quantity=1):
		dp = self._locate_FF()
		while dp>0:
			dp-=2
			if self.data[dp]==id:
				self.data[dp+1]-=quantity
				if self.data[dp+1]<=0:
					self.data[dp+1]=0
					self.data[dp]=0xFF
					self.data[0]=self.amount_of_items - 1
				return

	def get_offset(self,k):
		return (2*k)+1

	def blast(self,bank):
		bank[self.offset:self.offset+len(self.data)]=self.data

def gen_checksum(data):
	d = 0
	dp = 0
	a = 0
	while dp<(len(data)-1):
		a = data[dp]
		dp += 1
		d+=a
		d = (d%256)
	return (-d%256)-1
