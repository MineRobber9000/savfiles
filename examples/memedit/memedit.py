import argparse,sav,sys

# Makes 4F (hex 0x59) run code from the 3rd item of your inventory. (RAM location $D322) Can optionally make 4F the first item in
# your inventory.

# This is adaptable! Just replace payload.bin with a payload that is at most 0x1B bytes long (or change the offset address (0xda65)).

def getMainDataOffset(a):
	return 0x05a3+(a-0xd2f7)

BN_OFFSET = getMainDataOffset(0xd5a0)
BOX_OFFSET = 0xb0c0
INVENTORY_OFFSET = getMainDataOffset(0xd31d)

def myhex(n,p=2):
	return hex(n)[2:].zfill(p).upper()

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

def getBank(box):
	if box<7:
		return 2
	return 3

def getAddr(box):
	if box>=7:
		box -= 6
	return [0x0000,0x0462,0x08c4,0x0d26,0x1188,0x15ea][box-1]

def getIndividualChecksumAddr(box):
	if box>=7:
		box -= 6
	return 0x1a4d+(box-1)

payload = []
with open("payload.bin","rb") as f:
	payload = list(bytearray(f.read()))
payload_length = len(payload)

if __name__=="__main__":
	ap = argparse.ArgumentParser(prog="python ace4f.py",description="Adds Pocket Computer to a save file.") #Converts a save file to make 4F execute code from the 3rd item in your inventory.",epilog="Note: do not use the Daycare, as it breaks this method. If you must use the Daycare, run this program on the save after you remove the Pokemon from the Daycare.")
	ap.add_argument("save",help="Save file to convert.")
	ap.add_argument("box",help="Box to install the save editor in.",type=int)
	ap.add_argument("--list-boxes","-l",action="store_true",help="List empty boxes and quit.")
	ap.add_argument("--current-box","-c",action="store_true",help="Print the current box and continue working.")
#	ap.add_argument("--add-item-to-inventory",action="store_true",help="Adds 4F to your inventory.")
	args = ap.parse_args()
	save = sav.SAVFile(args.save)
	cur_box = (save[1][BN_OFFSET]&0x7F)
	if args.current_box:
		print(cur_box)
#	print("SRAM{}:{}".format(myhex(getBank(args.box)),myhex((getAddr(args.box)+0xa000),4)))
	if args.list_boxes:
		b = []
		for i in (1,2,3,4,5,6,7,8,9,10,11,12):
			if save[getBank(i)][getAddr(i)]==0:
				b.append(i)
		if len(b)==0:
			print "No boxes are empty!"
		elif len(b)==1:
			print "Box {} is empty.".format(b[0])
		else:
			print "Boxes {} and {} are empty.".format(", ".join([str(x) for x in b[:-1]]),str(b[-1]))
		sys.exit(0)
#	inv = Inventory(save[1],INVENTORY_OFFSET,20)
#	print inv.amount_of_items
#	print " ".join(map(hex,inv.data[inv.getOffset(0):inv.getOffset(0)+2]))
#	inv.add_item(0x5d,1)
#	print " ".join(map(hex,inv.data[inv.getOffset(1):inv.getOffset(1)+2]))
#	print inv.data[5]==0xFF
#	print inv.amount_of_items
	offset = getAddr(args.box)
	save[getBank(args.box)][offset:offset+payload_length]=payload[0:payload_length]
	save[getBank(args.box)][0x1a4c]=gen_checksum(save[getBank(args.box)][0x0000:0x1a4c])
	save[getBank(args.box)][getIndividualChecksumAddr(args.box)]=gen_checksum(save[getBank(args.box)][getAddr(args.box):getAddr(args.box)+1122])
#	if args.add_item_to_inventory:
#		inv.add_item(0x59,0x01)
#		inv.blast(save[1])
	if args.box==cur_box:
		save[1][BOX_OFFSET:BOX_OFFSET+payload_length]=payload[0:payload_length]
		save[1][0x1523]=gen_checksum(save[1][0x0598:(0x0598+(0x1523-0x0598+1))])
	save.output(args.save+".mod")
