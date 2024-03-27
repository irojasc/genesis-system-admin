from datetime import date


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

	def getUserName(self):
		return self.user

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
		return "{{prdCode: {0}, isbn: {1}, title: {2}, autor: {3}, publisher: {4}, dateOut: {5}, lang: {6}, pages: {7}, edition: {8}, cover: {9}, id: {10}, width: {11}, height: {12}, content: {13}, itemCategory: {14}}}".format(self.prdCode,
																																	self.isbn, self.title,
																																	self.autor, self.publisher,
																																	self.dateOut, self.lang,
																																	self.pages, self.edition,
																																	self.cover, self.id, self.width,
																																	self.height, self.content, self.itemCategory)

	def __init__(self, itemCode: str = None, id: int = None, isbn: str = None, title: str = None, autor: str = None,
			   	publisher: str = None, dateOut: str = None, lang: str = None, pages: int = None, edition: int = None,
				cover: int = -1, width: int = None, height: int = None, itemCategory: str = None, content: str = None):
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

		#cover: 0 blanda, 1 dura
		try:
			self.cover = cover + 0
		except:
			self.cover = -1

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
	
	def getPrdCode(self)->str:
		return self.prdCode
	
	def getItemCode(self) -> str:
		return self.itemCode
	
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

	def addDataWareProduct(self, wareName:str = None, qtyNew: int = None, qtyOld: int = None, qtyMinimun: int = 0,
						pvNew: float = 0.0, pvOld: float = 0.0, dsct: int = 0, loc: str = None,
						isEnabled: bool = True, isExists: bool = None, idWare: id = None, flag: bool = True,
						isVirtual: bool = None):
		if flag:
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
				"isVirtual": isVirtual,
				"idWare": idWare
			}
		else:
			dataTemp = {
				"isVirtual": isVirtual,
				"isExists": isExists,
				"idWare": idWare,
				"qtyNew": 0,
				"qtyOld": 0
			}

		self.wareData.update({wareName: dataTemp if wareName else None})

	def clearWareData(self):
		self.wareData.clear()
	
	def removePairKeyValue(self, key: str = None):
		if key:
			self.wareData.pop(key)
	
	def updateWareFields(self, wareName: str = None, qtyMinimun: int = None, pvNew: float = None, pvOld: float = None,
					dsct: int = None, loc: str = None, isEnabled: bool = None, isExists: bool = None, isVirtual: bool = None,
					idWare: int = None):
		
		if wareName:
			if "qtyNew" in self.wareData[wareName]:
				try:
					self.wareData[wareName]["qtyNew"] = self.wareData[wareName]["qtyNew"] + 0
				except:
					self.wareData[wareName]["qtyNew"] = 0

			elif not("qtyNew" in self.wareData[wareName]):
				self.wareData[wareName]["qtyNew"] = 0

			if "qtyOld" in self.wareData[wareName]:
				try:
					self.wareData[wareName]["qtyOld"] = self.wareData[wareName]["qtyOld"] + 0
				except:
					self.wareData[wareName]["qtyOld"] = 0

			elif not("qtyOld" in self.wareData[wareName]):
				self.wareData[wareName]["qtyOld"] = 0

			self.wareData[wareName]["qtyMinimun"] = qtyMinimun
			self.wareData[wareName]["pvNew"] = pvNew
			self.wareData[wareName]["pvOld"] = pvOld
			self.wareData[wareName]["dsct"] = dsct
			self.wareData[wareName]["loc"] = loc
			self.wareData[wareName]["isEnabled"] = isEnabled
			self.wareData[wareName]["isExists"] = isExists
			self.wareData[wareName]["isVirtual"] = isVirtual
			self.wareData[wareName]["idWare"] = idWare

	def getWareDataLen(self):
		return len(self.wareData)

	def getWareData(self):
		return self.wareData
	
class ware:
	def __repr__(self):
		return "{{id: {0}, cod: {1}, auth: {2}}}".format(self.id, self.cod, self.auth)
	
	def __str__(self):
		return "{{id: {0}, cod: {1}, auth: {2}}}".format(self.id, self.cod, self.auth)

	def __init__(self, id: int = None, cod = "", auth: dict = None):
		self.id = id
		self.cod = cod
		self.auth = auth

	def getWareCode(self) -> str:
		return self.cod
	
	def getWareId(self) -> int:
		return self.id
	
class product_transfer():
	def __repr__(self):
		return "{{id: {0}, type: {1}, fromUserName: {2}, toUserName: {3}, fromWareCod: {4}, toWareCod: {5}, fromDate: {6}, toDate: {7}, state: {8}, products: {9}}}".format(
				self.idTransfer, self.type, self.fromUserName, self.toUserName, self.fromWareCod, self.toWareCod, 
				self.fromDate, self.toDate, self.state, self.products)
	
	def __str__(self):
		return "{{id: {0}, type: {1}, fromUserName: {2}, toUserName: {3}, fromWareCod: {4}, toWareCod: {5}, fromDate: {6}, toDate: {7}, state: {8}, products: {9}}}".format(
				self.idTransfer, self.type, self.fromUserName, self.toUserName, self.fromWareCod, self.toWareCod, 
				self.fromDate, self.toDate, self.state, self.products)

	def __init__(self, idTransfer: str = None, fromUserName: str = None, toUserName: str = None, fromWareCod: str = None,
				toWareCod: str = None, fromDate: date = None, toDate: date = None, state: int = None, notes: str = None,
				idProduct: int = None, isbn: str = None, title: str = None, qtyNew: int = None, qtyOld: int = None):
		self.idTransfer = idTransfer
		self.type = 'TRASLADO'
		self.fromUserName = fromUserName
		self.toUserName = toUserName
		self.fromWareCod = fromWareCod
		self.toWareCod = toWareCod
		self.fromDate = fromDate
		self.toDate = toDate
		self.state = 'ABIERTO' if state == 3 else 'ATENDIDO' if state == 2 else 'CERRADO' if state == 1 else None
		self.notes = notes
		self.products = []
		self.products.append((idProduct, isbn, title, qtyNew, qtyOld))

	def setState(self, state: str = None ):
		self.state = state
	
	def setStateById(self, id: int = None ):
		self.state = 'ABIERTO' if id == 3 else 'ATENDIDO' if id == 2 else 'CERRADO' if id == 1 else None
	
	def setToUserName(self, userName: str = None):
		self.toUserName = userName
	
	def setToDate(self, toDate: date = None):
		self.toDate = toDate
	
	def getState(self):
		return self.state
	
	def getStateId(self):
		return 3 if self.state == 'ABIERTO' else 2 if self.state == 'ATENDIDO' else 1 if self.state == 'CERRADO' else None
	 
	def getIdTransfer(self):
		return self.idTransfer
	
	def getOwnType(self):
		return self.type

	def getFromWareCod(self):
		return self.fromWareCod
	
	def getToWareCod(self):
		return self.toWareCod
	
	def getFromUserName(self):
		return self.fromUserName
	
	def getToUserName(self):
		return self.toUserName

	def addProduct(self, idProduct: int = None, isbn: str = None, title: str = None, qtyNew: int = None, qtyOld: int = None):
		self.products.append((idProduct, isbn, title, qtyNew, qtyOld))
		return True

	def getProducts(self):
		return self.products
	
	def getFromDate(self) -> str:
		return self.fromDate.strftime("%Y-%m-%d") if self.fromDate else ''
	
	def getToDate(self) -> str:
		return self.toDate.strftime("%Y-%m-%d") if self.toDate else ''
	
	def downGradeIdStateByOne(self):
		self.state = 'ATENDIDO' if self.state == 'ABIERTO' else 'CERRADO' if self.state == 'ATENDIDO' else None
		
