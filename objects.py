class user:
	def __init__(self, user = "", passwd = "", name = "", doc = "", phone = "", enabled = False, purchaseEnabled = False):
		self.user = user
		self.passwd = passwd
		self.name = name
		self.doc = doc
		self.phone = phone
		self.enabled = enabled
		self.purchaseEnabled = purchaseEnabled

class supplier:
	def __init__(self, id, name, admin, phone, direction, mail):
		self.id = id
		self.name = name
		self.register = register
		self.admin = admin
		self.phone = phone
		self.direction = direction
		self.mail = mail

class gender:
	def __init__(self, id, name):
		self.id = id
		self.name = name

class movement_detail:
	def __init__(self, id, userID, books_IDs, depart_ID, depart_date, arrival_ID, arrival_date, cond = [False,False]):
		self.id = id
		self.userID = userID
		self.books_IDs = books_IDs
		self.depart_ID = depart_ID
		self.depart_date = depart_date
		self.arrival_ID = arrival_ID
		self.arrival_date = arrival_date
		self.cond = cond

class daily_sale:
	def __init__(self, id, date, books_IDs = [] , total_ = 0):
		self.id = id
		self.books_IDs = books_IDs
		self.date = date
		self.total_ = total_

class ware_book:
	#def __init__(self,wares = None, objBook = None, ware_quantity = [], ware_location = [], permissions = []):
	def __init__(self, objBook=None, wares = None, data = None):
		ware_1 = wares[1][0].cod
		ware_2 = wares[1][1].cod
		ware_3 = wares[1][2].cod
		ware_4 = wares[1][3].cod

		self.objBook = objBook
		self.almacen_data = {"cant_" + ware_1: int(data[7]),
							 "ubic_" + ware_1: str(data[8]),
							 "isok_" + ware_1: bool(data[9]),
							 "cant_" + ware_2: int(data[10]),
							 "ubic_" + ware_2: str(data[11]),
							 "isok_" + ware_2: bool(data[12]),
							 "cant_" + ware_3: int(data[13]),
							 "ubic_" + ware_3: str(data[14]),
							 "isok_" + ware_3: bool(data[15]),
			                 "cant_" + ware_4: int(data[16]),
							 "ubic_" + ware_4: str(data[17]),
							 "isok_" + ware_4: bool(data[18])}

class book:
	#def __init__(self, cod, isbn, name, autor, editorial, supplierID, Pv = 0, genderID = "", Pc = 0, dsct = 0):
	def __init__(self, data, genderID="", Pc=0, dsct=0):
		self.cod = str(data[0]) # este
		self.isbn = str(data[1]) # este
		self.name = str(data[2]) # este
		self.autor = str(data[3]) # este
		self.editorial = str(data[4]) #este
		self.supplierID = str(data[5]) #este
		self.genderID = genderID
		self.Pc = Pc
		self.Pv = float(data[6]) #este
		self.dsct = dsct

class ware_:
	def __init__(self, cod = "", dir = "", enabled = False, toolTip = False):
		self.cod = cod
		self.dir = dir
		self.enabled = enabled
		self.toolTip = toolTip





