
class user:
	def __repr__(self):
		return "user()"
	
	def __str__(self):
		return str(self.auth)
	
	def __init__(self, user: str = None, pwd: str = None, name: str = None, doc: str = None, phone: str = None, auth: dict = None, level: int = None):
		self.user = user
		self.pwd = pwd
		self.name = name
		self.doc = doc
		self.phone = phone
		# auth es dict que contiene [enabled, producSrch]
		self.auth = auth
		self.level = level

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
	def __init__(self, objBook=None, wares = None, data = None, isFromSystem: bool = False):
		ware_data = {}
		if not(isFromSystem):
			for index, i in enumerate(wares[1]):
				base = 3 * index + 7
				temp_data = { 
					"cant_" + i.cod: 0 if data[base] == "" else int(data[base]),
					"ubic_" + i.cod: str(data[base + 1]),
					"isok_" + i.cod: bool(data[base + 2])
				}
				ware_data.update(temp_data)
		else:
			for index, i in enumerate(wares[1]):
				temp_data = { 
					"cant_" + i.cod: int(data) if index==0 else 0,
					"ubic_" + i.cod: "SIN UBICACION",
					"isok_" + i.cod: True
				}
				ware_data.update(temp_data)

		self.objBook = objBook
		self.almacen_data = ware_data

class product:
	def __init__(self, type: str = None, id: int = None, data: list = [], genderID="", Pc=0):
		self.type = type
		self.id = id
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

	def setISBN(self, isbn: str):
		self.isbn = isbn
		
	def setName(self, name: str):
		self.name = name
	
	def setAutor(self, autor: str):
		self.autor = autor
	
	def setEditorial(self, editorial: str):
		self.editorial = editorial
	
	def setPv(self, pv: float):
		self.Pv = float(pv)

class ware:
	def __repr__(self):
		return "ware()"
	
	def __str__(self):
		return str(self.auth)

	def __init__(self, id: int = None, cod = "", auth: dict = None):
		self.id = id
		self.cod = cod
		self.auth = auth