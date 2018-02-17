import argparse,sav

# Makes 4F (hex 0x59) run code from the 3rd item of your inventory. (RAM location $D322) Can optionally make 4F the first item in
# your inventory.

# This is adaptable! Just replace payload.bin with a payload that is at most 0x1B bytes long (or change the offset address (0xda65)).

def getMainDataOffset(a):
	return 0x05a3+(a-0xd2f7)

OFFSET = getMainDataOffset(0xda54)
INVENTORY_OFFSET = getMainDataOffset(0xd31d)

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

	def getOffset(self,k):
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

payload = []
with open("payload.bin","rb") as f:
	payload = list(bytearray(f.read()))
payload_length = len(payload)

if __name__=="__main__":
	ap = argparse.ArgumentParser(prog="python fix_checksum.py",description="Converts a save file to make 4F execute code from the 3rd item in your inventory.",epilog="Note: do not use the Daycare, as it breaks this method. If you must use the Daycare, run this program on the save after you remove the Pokemon from the Daycare.")
	ap.add_argument("save",help="Save file to convert.")
#	ap.add_argument("--add-item-to-inventory",action="store_true",help="Adds 4F to your inventory.")
	args = ap.parse_args()
	save = sav.SAVFile(args.save)
#	inv = Inventory(save[1],INVENTORY_OFFSET,20)
#	print inv.amount_of_items
#	print " ".join(map(hex,inv.data[inv.getOffset(0):inv.getOffset(0)+2]))
#	inv.add_item(0x5d,1)
#	print " ".join(map(hex,inv.data[inv.getOffset(1):inv.getOffset(1)+2]))
#	print inv.data[5]==0xFF
#	print inv.amount_of_items
#	save[1][OFFSET:OFFSET+payload_length]=payload[0:payload_length]
#	if args.add_item_to_inventory:
#		inv.add_item(0x59,0x01)
#		inv.blast(save[1])
	save[1][0x1523]=gen_checksum(save[1][0x0598:(0x0598+(0x1523-0x0598+1))])
	save.output(args.save+".mod")
