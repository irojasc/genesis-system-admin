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
		self.register = ""
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
	def __init__(self, objBook=None, wares = None, data = None):
		ware_data = {}
		for index, i in enumerate(wares[1]):
			base = 3 * index + 7
			temp_data = { 
				"cant_" + i.cod: 0 if data[base] == "" else int(data[base]),
				"ubic_" + i.cod: str(data[base + 1]),
				"isok_" + i.cod: bool(data[base + 2])
			}
			ware_data.update(temp_data)
		
		self.objBook = objBook
		self.almacen_data = ware_data

class book:
	def __init__(self, data, genderID="", Pc=0):
		self.cod = str(data[0]) # este
		self.isbn = str(data[1]) # este
		self.name = str(data[2]) # este
		self.autor = str(data[3]) # este
		self.editorial = str(data[4]) #este
		self.supplierID = str(data[5]) #este
		self.genderID = genderID #HARDCODEADO
		self.Pc = Pc #HARDCODEADO
		self.Pv = float(data[6]) #este
		self.active = bool(data[-1]) #indica si item esta activo
	
	def setActive(self, condition: bool):
		self.active = condition


class ware_:
	def __init__(self, cod = "", dir = "", enabled = False, toolTip = False):
		self.cod = cod
		self.dir = dir
		self.enabled = enabled
		self.toolTip = toolTip





