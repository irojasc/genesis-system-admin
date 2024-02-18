
class user:
	def __repr__(self):
		return "{{user: {0}, pwd: {1}, name: {2}, doc: {3}, phone: {4}, auth: {5}, level: {6}}}".format(self.user, 
																								  self.pwd, 
																								  self.name, 
																								  self.doc, 
																								  self.phone,
																								  self.auth,
																								  self.level)
	
	def __str__(self):
		return "{{user: {0}, pwd: {1}, name: {2}, doc: {3}, phone: {4}, auth: {5}, level: {6}}}".format(self.user, 
																								  self.pwd, 
																								  self.name, 
																								  self.doc, 
																								  self.phone,
																								  self.auth,
																								  self.level) 
	
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
		return '{{prdCode: {0}, isbn: {1}, title: {2}, autor: {3}, publisher: {4}, dateOut: {5}, lang: {6}, pages: {7}, edition: {8}, cover: {9}, id: {10}, width: {11}, height: {12}, content: {13}, itemCategory: {14}}}'.format(self.prdCode,
																																	self.isbn, self.title,
																																	self.autor, self.publisher,
																																	self.dateOut, self.lang,
																																	self.pages, self.edition,
																																	self.cover, self.id, self.width, self.height)
	
	def __str__(self):
		return "{{prdCode: {0}, isbn: {1}, title: {2}, autor: {3}, publisher: {4}, dateOut: {5}, lang: {6}, pages: {7}, edition: {8}, cover: {9}, id: {10}, width: {11}, height:{12}, content: {13}, itemCategory: {14}}}".format(self.prdCode,
																																	self.isbn, self.title,
																																	self.autor, self.publisher,
																																	self.dateOut, self.lang,
																																	self.pages, self.edition,
																																	self.cover, self.id, self.width,
																																	self.height, self.content, self.itemCategory)

	def __init__(self, itemCode: str = None, id: int = None, isbn: str = None, title: str = None, autor: str = None,
			   	publisher: str = None, dateOut: str = None, lang: str = None, pages: int = None, edition: int = None,
				cover: bool = None, width: int = None, height: int = None, itemCategory: str = None, content: str = None):
		self.itemCode = itemCode
		self.prdCode = '{0}_{1}'.format(self.itemCode, str(id)) if itemCode != None else None
		self.isbn = isbn
		self.title = title
		self.autor = autor
		self.publisher = publisher 
		self.dateOut = dateOut
		self.lang = lang
		self.pages = pages
		self.edition = edition
		#cover: 1 blanda, 2 dura
		self.cover = 2 if bool(cover) else 1
		self.width = width
		self.height = height
		self.content = content
		self.id = id
		self.itemCategory = itemCategory #libro,artesania 
	
	def setActive(self, condition: bool):
		self.active = condition

	def setISBN(self, isbn: str):
		self.isbn = isbn
		
	def setTitle(self, title: str):
		self.title = title
	
	def setAutor(self, autor: str):
		self.autor = autor
	
	def setPublisher(self, publisher: str):
		self.publisher = publisher
	
	def setPv(self, pv: float):
		self.Pv = float(pv)
	
	def setId(self, id: int = None):
		self.id = id
		self.prdCode = '{0}_{1}'.format(self.itemCode, str(id)) if self.prdCode else self.prdCode

	def setItemCategory(self, itemCategory: str = None):
		self.itemCategory = itemCategory

	def setDateOut(self, dateOut: str = None):
		self.dateOut = dateOut

	def setEdition(self, edition: int = None):
		self.edition = edition
	
	def setPages(self, pages: int = None):
		self.pages = pages

	def setLang(self, lang: str = None):
		self.lang = lang
	
	def setCover(self, cover: int = None):
		self.cover = cover

	def setWidth(self, width: int = None):
		self.width = width

	def setHeight(self, height: int = None):
		self.height = height

	def setContent(self, content: str = None):
		self.content = content	

	def getId(self)->int:
		return self.id
	
	def getISBN(self)->str:
		return self.isbn
	
	def getTitle(self)->str:
		return self.title
	
	def getAutor(self)->str:
		return self.autor

	def getPublisher(self)->str:
		return self.publisher
	
	def getItemCategory(self)->str:
		return self.itemCategory
	
	def getLang(self)->str:
		return self.lang
	
	def getContent(self)->str:
		return self.content

	def getDateOut(self)->str:
		return self.dateOut
	
	def getPages(self)->int:
		return self.pages
	
	def getEdition(self)->int:
		return self.edition
	
	def getCover(self)->int:
		return self.cover
	
	def getWidth(self)->int:
		return self.width
	
	def getHeight(self)->int:
		return self.height
	
class ware_product:
	def __repr__(self):
		return "{{product: {0}, wareData: {1}}}".format(self.product,
												  self.wareData,
												  )

	def __str__(self):
		return "{{product: {0}, wareData: {1}}}".format(self.product,
												  self.wareData,
												  )
	
	def __init__(self, item: product = None, wareData: dict = {}):
		self.product = item
		self.wareData = wareData

	def addDataWareProduct(self, wareName:str = None, qtyNew: int = None, qtyOld: int = None, qtyMinimun: int = 1,
						pvNew: float = 0.0, pvOld: float = 0.0, dsct: int = 0, loc: str = None,
						isEnabled: bool = True, isExists: bool = None, idWare: id = None):
		dataTemp = {
			"qtyNew": qtyNew,
			"qtyOld": qtyOld,
			"qtyMinimun": qtyMinimun,
			"pvNew": pvNew,
			"pvOld": pvOld,
			"dsct": dsct,
			"loc": loc if loc != None else "SIN UBICACION",
			"isEnabled": isEnabled,
			"isExists": isExists,
			"idWare": idWare
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