
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

class product:

	def __repr__(self):
		return '{{prdCode: {0}, isbn: {1}, title: {2}, autor: {3}, publisher: {4}, dateOut: {5}, lang: {6}, pages: {7}, edition: {8}, cover: {9}}}'.format(self.prdCode,
																																	self.isbn, self.title,
																																	self.autor, self.publisher,
																																	self.dateOut, self.lang,
																																	self.pages, self.edition,
																																	self.cover)
	
	def __str__(self):
		return "{{prdCode: {0}, isbn: {1}, title: {2}, autor: {3}, publisher: {4}, dateOut: {5}, lang: {6}, pages: {7}, edition: {8}, cover: {9}}}".format(self.prdCode,
																																	self.isbn, self.title,
																																	self.autor, self.publisher,
																																	self.dateOut, self.lang,
																																	self.pages, self.edition,
																																	self.cover)

	def __init__(self, itemCode: str = None, id: int = None, isbn: str = None, title: str = None, autor: str = None, publisher: str = None, dateOut: str = None,
			  lang: str = None, pages: int = None, edition: int = None, cover: bool = None, width: int = None, height: int = None):
		self.prdCode = '{0}_{1}'.format(itemCode, str(id))
		self.isbn = isbn
		self.title = title
		self.autor = autor
		self.publisher = publisher 
		self.dateOut = dateOut.strftime("%Y") if bool(dateOut) else None
		self.lang = lang
		self.pages = pages
		self.edition = edition
		self.cover = "DURA" if cover else "BLANDA"
		self.width = width
		self.height = height
	
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

class ware_product:

	def __str__(self):
		return self.wareData
	
	def __init__(self, item: product = None, wareData: dict = {}):
		self.product = item
		self.wareData = wareData

	def addDataWareProduct(self, wareName:str = None, qtyNew: int = None, qtyOld: int = None, qtyMinimun: int = 1,
						 pvNew: float = 0.0, pvOld: float = 0.0, dsct: int = 0, loc: str = None, isEnabled: bool = True):
		dataTemp = {
			"qtyNew": qtyNew,
			"qtyOld": qtyOld,
			"qtyMinimun": qtyMinimun,
			"pvNew": pvNew,
			"pvOld": pvOld,
			"dsct": dsct,
			"loc": loc if loc != None else "SIN UBICACION",
			"isEnabled": isEnabled
		}
		self.wareData.update({wareName: dataTemp})

class ware:
	def __repr__(self):
		return "{{id: {0}, cod: {1}, auth: {2}}}".format(self.id, self.cod, self.auth)
	
	def __str__(self):
		return "{{id: {0}, cod: {1}, auth: {2}}}".format(self.id, self.cod, self.auth)

	def __init__(self, id: int = None, cod = "", auth: dict = None):
		self.id = id
		self.cod = cod
		self.auth = auth