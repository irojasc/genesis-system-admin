import mysql.connector
import boto3
import logging
import os.path
import os
from objects import user, ware, ware_product, product, product_transfer
from decouple import Config, RepositoryEnv
from datetime import datetime, date
import bcrypt
import time
from PyQt5.QtWidgets import QInputDialog, QLineEdit
from PyQt5 import QtWidgets


# import traceback

DOTENV_FILE = 'C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))
ROOT = 'C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/'

# ware_gestor: maneja datos de almacen
class wares_gestor:
	def __init__(self, condition = "main"):
		if condition == "main":
			self.wareList = []
			self.load_wares()

	def connectDB(self):
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST'), user= env_config.get('MYSQL_USER'), passwd= env_config.get('MYSQL_PASSWORD'), port=env_config.get('MYSQL_PORT'))
		self.cursor = self.mydb.cursor()

	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def createWare(self, index_value, perheaders):
		index, value = index_value
		headers = perheaders.copy()
		headers.pop(0)
		perDict = {}
		perDict.update({"enabled": bool(value[2])})
		perDict.update({"isVirtual": bool(value[3])})
		for index, header in enumerate(headers):
			pair = {header[0]: bool(value[5+index])}
			perDict.update(pair)
		return ware(value[0], value[1], perDict)
	
	def load_wares(self):
		query = "select id, code, enabled, isVirtual, ws.* from genesisDB.ware w inner join genesisDB.wareset ws on w.warelvl = ws.lvl where enabled = true order by id asc;"
		query2 = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'wareset' order by ordinal_position;")
		try:
			self.connectDB()
			self.cursor.execute(query)
			wareRows = self.cursor.fetchall()
			#query2 para obtener headers de wareset
			self.cursor.execute(query2)
			headers = self.cursor.fetchall()
			self.wareList = list(map(lambda x: self.createWare(x, headers), enumerate(wareRows)))

		except mysql.connector.Error as error:
			print("Error: {}".format(error))

		finally:
			try:
				if self.mydb.is_connected():
					self.disconnectDB()
					# print("MySQL connection is closed")
			except:
				print("No se pudo conectar")

	def sort_ware(self, fileWare: str = None):
		# funcion que mueve a primera posicion los datos de almacen actual
		# self.wareList.insert(0, self.wareList.pop(next((i for i, item in enumerate(self.wareList) if item.cod == fileWare), -1)))
		self.wareList.insert(0, self.wareList.pop(next((i for i, item in enumerate(self.wareList) if item.cod == fileWare), -1)))
		index = list(map(lambda x: x[0] if x[1].cod == fileWare else None, enumerate(self.wareList)))
		return True if isinstance(index[0], int) else False

	def exist_ware(self):
		ware_name = ""
		try:
			file = open(ROOT + "registro.txt", "r")
			vect = file.readlines()
			abrev = vect[0].split(":")[1].strip('\n')
			ware_name = vect[1].split(":")[1].strip('\n')
			file.close()
			if self.sort_ware(abrev):
				copiedList = self.wareList.copy()
				fstWare = copiedList.pop(0)
				return True, (fstWare, copiedList), ware_name
			else:
				return False, None, "UNKNOWN"
		except:
			file.close()
			return False, None, "UNKNOWN"

	def upload_location(self, almc = "", cod_book = "", ubic = ""):
		self.connectDB()
		query = ("update genesisDB.ware_books set genesisDB.ware_books.ubic_" + almc + " = '" + ubic + "' where genesisDB.ware_books.cod_book = '" + cod_book + "';")
		try:
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnectDB()
		except:
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

	def updateDBItem(self, data: ware_product = None):
		query_product = "update genesisDB.product set"
		query_parameters = []
		query_parameters.append(" isbn = NULL ") if not(data.product.getISBN()) else query_parameters.append(" isbn = '" + data.product.getISBN() + "'")
		None if not(data.product.getTitle()) else query_parameters.append(" title = '" + data.product.getTitle() + "'")
		None if not(data.product.getAutor()) else query_parameters.append(" autor = '" + data.product.getAutor() + "'")
		None if not(data.product.getPublisher()) else query_parameters.append(" publisher = '" + data.product.getPublisher() + "'")
		query_parameters.append(" dateOut = NULL ") if not(data.product.getDateOut()) else query_parameters.append(" dateOut = '" + data.product.getDateOut() + "'")
		query_parameters.append(" edition = NULL ") if not(data.product.getEdition()) else query_parameters.append(" edition = " + str(data.product.getEdition()))
		query_parameters.append(" pages = NULL ") if not(data.product.getPages()) else query_parameters.append(" pages = " + str(data.product.getPages()))
		query_parameters.append(" idLanguage = NULL ") if not(data.product.getLang()) else query_parameters.append(" idLanguage = (select l.id from genesisDB.language as l where l.language = '" + data.product.getLang() + "')")
		query_parameters.append(" cover = NULL ") if data.product.getCover() < 0 else query_parameters.append(" cover = " + str(data.product.getCover()))
		query_parameters.append(" width = NULL ") if not(data.product.getWidth()) else query_parameters.append(" width = " + str(data.product.getWidth()))
		query_parameters.append(" height = NULL ") if not(data.product.getHeight()) else query_parameters.append(" height = " + str(data.product.getHeight()))
		query_parameters.append(" content = NULL ") if not(data.product.getContent()) else query_parameters.append(" content = '" + data.product.getContent() + "'")
		query_product = query_product + ", ".join(query_parameters) + ", editDate = '" + str(date.today()) + "' where id = " + str(data.product.getId()) + ";"
		try:
			self.connectDB()
			self.cursor.execute(query_product)
			# query_2 para hacer el insert de los ware_products
			existsData = list(filter(lambda x: x["isExists"], data.wareData.values())) if not((len(data.wareData) == 1 and None in data.wareData)) else None
			if existsData:
				#La parte de update datos para datos ya existentes
				Data2Update = list(map(lambda x: (x["qtyNew"], x["qtyOld"], x["pvNew"], x["pvOld"], x["loc"],
									x["dsct"], x["qtyMinimun"], x["isEnabled"], x["idWare"],
									data.product.getId(), x["idWare"], data.product.getId()), existsData))
				stmt_update = "update genesisDB.ware_product wp set qtyNew = %s, qtyOld = %s, pvNew = %s, " + \
					"pvOld = %s, loc = %s, dsct = %s, qtyMinimun = %s, isEnabled = %s, editDate = '" + str(date.today()) + "' " + \
					"where wp.idWare = %s and wp.idProduct = %s and (select exists(select wp.qtyNew where wp.idWare = %s and wp.idProduct = %s))"
				self.cursor.executemany(stmt_update, Data2Update)

				#La parte de insert nuevos datos para ware_product
				Data2Insert = list(map(lambda x: (x["idWare"], data.product.getId(), x["qtyNew"], x["qtyOld"], x["pvNew"], x["pvOld"],
									x["loc"], x["dsct"], x["qtyMinimun"], x["isEnabled"], x["idWare"], data.product.getId()), existsData))
				
				stmt_insert = "insert into genesisDB.ware_product (idWare, idProduct, qtyNew, qtyOld, pvNew, pvOld, loc, dsct, " + \
							"qtyMinimun, isEnabled) (select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s where not (select exists(select " + \
							"genesisDB.ware_product.qtyNew from genesisDB.ware_product where idWare = %s and idProduct = %s)))"
				self.cursor.executemany(stmt_insert, Data2Insert)

			self.mydb.commit()
		
		except mysql.connector.Error as error:
			print("Error: {}".format(error))

		except Exception as error:
			print("An exception ocurred:", error)
		
		finally:
			try:
				if self.mydb.is_connected():
					self.disconnectDB()
					return True
			except:
				print("No se pudo conectar a DB en getItemData")
				return False

	def insertNewItemDB(self, data: ware_product = None, currentWare: str = None):
		#anteriormente se lee el spinbox stock para ver si te tiene que agregar cantidad a nuevo producto
		if bool(data) and bool(currentWare):
			#esta parte es para hacer las subconsultas
			idItemSubQuery = "(select id from genesisDB.item where item = '" + data.product.getItemCategory() + "')" if bool(data.product.getItemCategory()) else None
			idLanguageSubQuery = "(select id from genesisDB.language where language = '" + data.product.getLang() + "')" if bool(data.product.getLang()) else None
			
			# query_1 para hacer el insert principal de product
			query_1 = "insert into genesisDB.product (id, idItem, isbn, title, autor, publisher, content, " + \
			"dateOut, idLanguage, pages, edition, cover, width, height) values (%s, %s, %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s);" % (str(data.product.getId()), idItemSubQuery, 
			"'" + data.product.getISBN() + "'" if data.product.getISBN() else "NULL",
			data.product.getTitle(), data.product.getAutor(), data.product.getPublisher(),
			"'" + data.product.getContent() + "'" if data.product.getContent() else "NULL",
			"'" + data.product.getDateOut() + "'" if data.product.getDateOut() else "NULL",
			idLanguageSubQuery if idLanguageSubQuery else "NULL",
			str(data.product.getPages()) if data.product.getPages() else "NULL",
			str(data.product.getEdition()) if data.product.getEdition() else "NULL",
			str(0 if data.product.getCover() == 1 else 1 if data.product.getCover() == 2 else 0) if data.product.getCover() else "NULL",
			str(data.product.getWidth()) if data.product.getWidth() else "NULL",
			str(data.product.getHeight()) if data.product.getHeight() else "NULL")
			
			try:
				self.connectDB()
				self.cursor.execute(query_1)
				# query_2 para hacer el insert de los ware_products
				existsData = list(filter(lambda x: x["isExists"], data.wareData.values())) if not((len(data.wareData) == 1 and not(data.wareData[None]))) else None
				if existsData:
					# Data2Tuple = list(map(lambda x: (x["idWare"], str(data.product.getId()), str(x["qtyNew"]), str(x["qtyOld"]), str(x["pvNew"]), str(x["pvOld"]), x["loc"], str(x["dsct"]), str(x["qtyMinimun"]), x["isEnabled"]), existsData))
					Data2Tuple = list(map(lambda x: (x["idWare"], data.product.getId(), x["qtyNew"], x["qtyOld"], x["pvNew"], x["pvOld"], x["loc"], x["dsct"], x["qtyMinimun"], x["isEnabled"]), existsData))
					stmt = "insert into genesisDB.ware_product (idWare, idProduct, qtyNew, qtyOld, pvNew, pvOld, loc, dsct, qtyMinimun, isEnabled) " + \
					"values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					self.cursor.executemany(stmt, Data2Tuple)
				self.mydb.commit()
				self.disconnectDB()
				return True
			
			except Exception as error:
				print("Something wrong happen: ", error)
				self.disconnectDB()
				return False
			
	def getNextCodDB(self):
		query = "SELECT 'next', max(cast(p.id as signed)) + 1 as next, null, null, null FROM genesisDB.product p UNION SELECT 'item', i.id, i.item, i.code, null FROM genesisDB.item i UNION SELECT 'lang', l.id, l.language, null, null FROM genesisDB.language l UNION SELECT 'ctgy',c.id, c.ctgy, c.lvl, null FROM genesisDB.category c UNION SELECT 'ware', `code`, `name`, cast(`isVirtual` as UNSIGNED), w.id FROM genesisDB.ware w where w.enabled = 1;"
		try:
			self.connectDB()
			self.cursor.execute(query)
			data = self.cursor.fetchall()
			nextCode = list(filter(lambda x: True if x[0] == 'next' else False, data))[0][1]
			items = list(map(lambda x: (x[1], x[2], x[3]),list(filter(lambda x: True if x[0] == 'item' else False, data))))
			languages = list(map(lambda x: (x[1], x[2]),list(filter(lambda x: True if x[0] == 'lang' else False, data))))
			category1 = list(map(lambda x: (x[1], x[2], x[3]),list(filter(lambda x: True if (x[0] == 'ctgy' and int(x[3]) == 1) else False, data))))
			category2 = list(map(lambda x: (x[1], x[2], x[3]),list(filter(lambda x: True if (x[0] == 'ctgy' and int(x[3]) == 2) else False, data))))
			category3 = list(map(lambda x: (x[1], x[2], x[3]),list(filter(lambda x: True if (x[0] == 'ctgy' and int(x[3]) == 3) else False, data))))
			#wares[1]: cod, wares[2]: name, wares[3]: isVirtual, wares[4]: id
			availableWares = list(map(lambda x: (x[1], x[2], x[3], x[4]),list(filter(lambda x: True if (x[0] == 'ware') else False, data))))
			data_dict = {"next": nextCode, "items": items, "languages": languages,"category1": category1, "category2": category2, "category3": category3, "wares": availableWares}
			self.disconnectDB()
			return True, data_dict
		except Exception as error:
			print("Something wrong happen: ", error)
			self.disconnectDB()
			return False, None

# ware_gestor: maneja de items en almacen
class WareProduct:
	def __init__(self):
		self.innerWareList = []
		self.temp_list = []

	def __del__(self):
		del self

	def __enter__(self):
		return self

	def __exit__(self,ext_type,exc_value,traceback):
		del self
	
	def connect_db(self):
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST'), user= env_config.get('MYSQL_USER'), passwd= env_config.get('MYSQL_PASSWORD'), port=env_config.get('MYSQL_PORT'))
		self.cursor = self.mydb.cursor()

	def disconnect_db(self):
		self.cursor.close()
		self.mydb.close()

	#actualiza cantidades de in/out directo a Ware Inner List
	def update_backtablequantity(self, newList: list = None, oldList: list = None, operationType: str = None, currentWare = None, location: str = None):
		mainList = newList + oldList
		for i in mainList:
			# formato de i: {'loc': 'ubic', 'cod': 'gn_x', 'isbn': '13dgs..', 'title': 'title', 'qtyNew': x, 'qtyOld': y}
			for j in self.innerWareList:
				if j.product.prdCode == i["cod"] and i["qtyOld"] == None:
					if location is not None: j.wareData[currentWare]["loc"] = location
					if operationType == "ingreso":
						j.wareData[currentWare]["qtyNew"] += i["qtyNew"]
					elif operationType == "salida":
						j.wareData[currentWare]["qtyNew"] -= i["qtyNew"]

				elif j.product.prdCode == i["cod"] and i["qtyNew"] == None:
					if location is not None: j.wareData[currentWare]["loc"] = location
					if operationType == "ingreso":
						j.wareData[currentWare]["qtyOld"] += i["qtyOld"]
					elif operationType == "salida":
						j.wareData[currentWare]["qtyOld"] -= i["qtyOld"]



	#actualiza cantidades de in/out directo a Data Base ware_product table
	def update_quantity(self, listNew: list[int] = None, listOld: list[int] = None, operationType: str = "", idWare: str = "", location: str = "", isGestorRequest=False):
		oprDict = { "ingreso": "+",
		"salida": "-"}
		tmp_NewList = []
		tmp_OldList = []
		self.connect_db() if not isGestorRequest else None
		try:
			# for j in listNew:
			# 	tmp_NewList.append((str(j["cantidad"]), j["cod"]))
			tmp_NewList = list(map(lambda x: (str(x["qtyNew"]), str(0), x["cod"].split("_")[1]), listNew))
			tmp_OldList = list(map(lambda x: (str(0), str(x["qtyOld"]), x["cod"].split("_")[1]), listOld))
			tmp_MainList = tmp_NewList + tmp_OldList

			if location == "":
				query_ = ("update genesisDB.ware_product set qtyNew = qtyNew " + oprDict[
					operationType] + " %s, qtyOld = qtyOld " + oprDict[
					operationType] + " %s, editDate = '" + str(date.today()) + "' where idProduct = %s and idWare = " + idWare)
			else:
				query_ = ("update genesisDB.ware_product set qtyNew = qtyNew " + oprDict[
					operationType] + " %s, qtyOld = qtyOld " + oprDict[
					operationType] + " %s, editDate = '" + str(date.today()) + "', loc = '" + location.upper() + "' where idProduct = %s and idWare = " + idWare)

			self.cursor.executemany(query_, tmp_MainList)
			self.mydb.commit() if not isGestorRequest else None
			self.disconnect_db() if not isGestorRequest else None
			return True

		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()		
			return False
		
	#carga de cero toda la lista de productos a Ware Inner List desde Data Base
	def loadInnerTable(self, updateDate: datetime.date = None):
		
		query = ("select w.code, i.code, p.id, isbn, title, autor, publisher, dateOut, language, pages, edition, cover, width, height, qtyNew,  qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled from genesisDB.product p left join genesisDB.ware_product wp on wp.idProduct = p.id left join genesisDB.language l on l.id = p.idLanguage left join genesisDB.ware w on w.id = wp.idWare inner join genesisDB.item i on i.id = p.idItem order by p.id asc;") if updateDate == None else ("select w.code, i.code, p.id, isbn, title, autor, publisher, dateOut, language, pages, edition, cover, width, height, qtyNew,  qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled from genesisDB.product p left join genesisDB.ware_product wp on wp.idProduct = p.id left join genesisDB.language l on l.id = p.idLanguage left join genesisDB.ware w on w.id = wp.idWare inner join genesisDB.item i on i.id = p.idItem where p.creationDate >= '{0}' or p.editDate >= '{0}' or wp.editDate >= '{0}' or p.creationDate >= '{0}' order by p.id asc;".format(updateDate))

		try:
			self.connect_db()
			self.cursor.execute(query)
			WareProductsRows = self.cursor.fetchall()
			for WareProduct in WareProductsRows:
				if not(len(self.innerWareList)):
					item = product(itemCode=WareProduct[1], id=WareProduct[2], isbn=WareProduct[3], title=WareProduct[4], autor=WareProduct[5], publisher=WareProduct[6],
					dateOut=WareProduct[7], lang=WareProduct[8], pages=WareProduct[9], edition=WareProduct[10], cover=WareProduct[11],
					width=WareProduct[12], height=WareProduct[13])
					wareproduct = ware_product(item, {})
					wareproduct.addDataWareProduct(WareProduct[0], qtyNew=WareProduct[14], qtyOld=WareProduct[15], qtyMinimun=WareProduct[16],
					pvNew=WareProduct[17], pvOld=WareProduct[18], dsct=WareProduct[19], loc=WareProduct[20], isEnabled=WareProduct[21])
					self.innerWareList.append(wareproduct)
				else:
					index = next((i for i, item in enumerate(self.innerWareList) if item.product.prdCode == '%s_%d' % (WareProduct[1], WareProduct[2])), None)
					if isinstance(index, int):
						if updateDate != None:
							self.innerWareList[index].product = product(itemCode=WareProduct[1], id=WareProduct[2], isbn=WareProduct[3],
							title=WareProduct[4], autor=WareProduct[5], publisher=WareProduct[6], dateOut=WareProduct[7], lang=WareProduct[8],
							pages=WareProduct[9], edition=WareProduct[10], cover=WareProduct[11], width=WareProduct[12], height=WareProduct[13])
						self.innerWareList[index].addDataWareProduct(WareProduct[0], WareProduct[14], WareProduct[15], WareProduct[16], WareProduct[17], WareProduct[18], WareProduct[19], WareProduct[20], WareProduct[21])
					else:
						# print("[destructured]",WareProduct[1],WareProduct[2],WareProduct[3],WareProduct[4],WareProduct[5],WareProduct[6],WareProduct[7],WareProduct[8],WareProduct[9],WareProduct[10],WareProduct[11],WareProduct[12],WareProduct[13])
						item = product(itemCode=WareProduct[1], id=WareProduct[2], isbn=WareProduct[3], title=WareProduct[4],
						autor=WareProduct[5], publisher=WareProduct[6], dateOut=WareProduct[7], lang=WareProduct[8], pages=WareProduct[9],
						edition=WareProduct[10], cover=WareProduct[11], width=WareProduct[12], height=WareProduct[13])
						# print("[composed]", item)
						wareproduct = ware_product(item, {})
						wareproduct.addDataWareProduct(WareProduct[0], WareProduct[14], WareProduct[15], WareProduct[16], WareProduct[17], WareProduct[18], WareProduct[19], WareProduct[20], WareProduct[21])
						self.innerWareList.append(wareproduct)

		except mysql.connector.Error as error:
			print("Error: {}".format(error))

		# except Exception:
		# 	# print("An error occurred:", error) 
		# 	traceback.print_exc()
			
		finally:
			try:
				if self.mydb.is_connected():
					self.disconnect_db()
					return True
			except:
				print("No se pudo conectar a DB en load_mainlist")
				return False

	#Cambia la locacion de producto ubicado en ware_product table from Data Base
	def changeItemLocation(self, iditem: str = "", location: str= "SIN UBICACION", currentWare: str="")->bool:
		try:
			self.connect_db()
			query = ("update genesisDB.ware_product set loc = '" + location + "', editDate = '" + str(date.today()) + "' where idProduct=" + iditem + " and idWare=(select id from genesisDB.ware where code = '" + currentWare + "');")
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnect_db()
			return True
		except Exception as error:
			print("Location: Activating Item: ", error)
			self.disconnect_db()
			return False
		
	#Cambia la locacion de producto ubicado en Ware Inner List
	def changeInnerItemLocation(self, idItem: int = "", location: str= "SIN UBICACION", currentWare: str= ""):
		try:
			index = list(filter(lambda x: x[1].product.getId() == idItem, enumerate(self.innerWareList)))[0][0]
			self.innerWareList[index].wareData[currentWare]["loc"] = location
			return True
		except Exception as error:
			print("error as", error)
			return False
	
	def updateInnerItem(self, data: ware_product = None):
		try:
			index = list(filter(lambda x: x[1].product.id == data.product.id, enumerate(self.innerWareList)))[0][0]
			self.innerWareList[index] = data 
			return True
		except Exception as error:
			return False

	def insertInnerNewItem(self, data: ware_product = None, own_wares = None):
		if bool(data):
			self.innerWareList.append(data)
			return True
		else:
			return False

	def getItemDataFromDB(self, idProduct: int = None)-> bool:
		query = ("select w.code, w.id, w.isVirtual, idItem, idProduct, isbn, title, autor, publisher, dateOut, language,pages, edition, cover, width, height, content, category, qtyNew, qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled, 'item' from " + \
				"(select wp.idWare as idWare, i.code as idItem, p.id as idProduct, isbn, title, autor, publisher, dateOut, language, pages, edition, cover, width, height, content, i.item as category, qtyNew,  qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled " + \
				"from genesisDB.product p " + \
				"left join genesisDB.ware_product wp on wp.idProduct = p.id " + \
				"left join genesisDB.language l on l.id = p.idLanguage " + \
				"inner join genesisDB.item i on i.id = p.idItem " + \
				"where p.id = " + str(idProduct) + ") as s " + \
				"left join genesisDB.ware w on w.id = s.idWare " + \
				"union " + \
				"select w.code, w.id, w.isVirtual, idItem, idProduct, isbn, title, autor, publisher, dateOut, language,pages, edition, cover, width, height, content, category, qtyNew, qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled, 'item' from " + \
				"(select wp.idWare as idWare, i.code as idItem, p.id as idProduct, isbn, title, autor, publisher, dateOut, language, pages, edition, cover, width, height, content, i.item as category, qtyNew,  qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled " + \
				"from genesisDB.product p " + \
				"left join genesisDB.ware_product wp on wp.idProduct = p.id " + \
				"left join genesisDB.language l on l.id = p.idLanguage " + \
				"inner join genesisDB.item i on i.id = p.idItem " + \
				"where p.id = " + str(idProduct) + ") as s " + \
				"right join genesisDB.ware w on w.id = s.idWare " + \
				"union select l.id, l.language, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 'lang' from genesisDB.language l;") if idProduct else False
		try:
			self.connect_db()
			self.cursor.execute(query)
			item = self.cursor.fetchall()
			if not(item[0][0]) and (item[0][26] == 'item'):
				languages = []
				productLocal = product(	itemCode=item[0][3], id=item[0][4], isbn=item[0][5], title=item[0][6], 
						   				autor=item[0][7], publisher=item[0][8], dateOut=item[0][9], lang=item[0][10],
										pages=item[0][11], edition=item[0][12], cover=item[0][13], width=item[0][14],
										height=item[0][15], content=item[0][16], itemCategory=item[0][17])
				wareProductLocal = ware_product(item = productLocal)
				for i in item[1:]:
					if i[26] == 'item':
						wareProductLocal.addDataWareProduct(wareName=i[0], isVirtual=bool(i[2]), idWare= i[1], isExists=False, flag=False)
					elif i[26] == 'lang':
						languages.append((i[0], i[1]))
						
			elif item[0][0]:
				languages = []
				productLocal = product(	itemCode=item[0][3], id=item[0][4], isbn=item[0][5], title=item[0][6],
										autor=item[0][7], publisher=item[0][8], dateOut=item[0][9], lang=item[0][10],
										pages=item[0][11], edition=item[0][12], cover=item[0][13], width=item[0][14],
										height=item[0][15], content=item[0][16], itemCategory=item[0][17])
				wareProductLocal = ware_product(item=productLocal)
				for obj in item:
					if bool(obj[0]) and obj[26] == 'item':
						wareProductLocal.addDataWareProduct(wareName=obj[0], qtyNew=obj[18], qtyOld=obj[19], qtyMinimun=obj[20], pvNew=obj[21], pvOld=obj[22], dsct=obj[23], loc=obj[24], isEnabled=bool(obj[25]), isExists=bool(obj[3]), idWare=obj[1], flag=True, isVirtual=bool(obj[2]))
					elif bool(obj[0]) and obj[26] == 'lang':
						languages.append((obj[0], obj[1]))
		
		except mysql.connector.Error as error:
			print("Error: {}".format(error))

		except Exception as error:
			print("An exception ocurred:", error)
		
		finally:
			try:
				if self.mydb.is_connected():
					self.disconnect_db()
					return True, languages.copy(), wareProductLocal
			except:
				print("No se pudo conectar a DB en getItemData")
				return False, None, None

	def compareEvaluation(self, wareDataItem, fromWare, toWare):
		#falta el tema del habilitado y desabilitado
		#la comparacion solo se realiza con lo items nuevos, ¡NO APLICA PARA ANTIGUOS!
		if (fromWare in wareDataItem) and (toWare in wareDataItem) and ('isEnabled' in wareDataItem[fromWare]) and ('isEnabled' in wareDataItem[toWare]):
			if (wareDataItem[fromWare]["qtyNew"] > wareDataItem[fromWare]["qtyMinimun"]) and ((wareDataItem[toWare]["qtyNew"] < wareDataItem[toWare]["qtyMinimun"]) or (wareDataItem[toWare]["qtyNew"] == 0)) and bool(wareDataItem[fromWare]['isEnabled']) and bool(wareDataItem[toWare]['isEnabled']):
				return True
		else:
			return False
	
	def compareTwoItemsWare(self, FromWare: str = None, ToWare: str = None) -> list:
		tmp_list = list(filter(lambda x: self.compareEvaluation(wareDataItem=x.getWareData(), fromWare=FromWare, toWare=ToWare), self.innerWareList))
		data_tranfer = list(map(lambda x: {'loc': x.wareData[FromWare]['loc'], 'cod': x.product.getPrdCode(), 'isbn': x.product.getISBN(), 'title': x.product.getTitle(), 'qtyNew': 1, 'qtyOld': None}, tmp_list))
		return (tmp_list, data_tranfer) if bool(tmp_list) and bool(data_tranfer) else ([], [])

	#registra el traslado de productos entre dos wares
	def insertTransferToDB(self, fromWareCod: str = None, 
						toWareCod: str = None, 
						fromUserName: str = None, 
						tmpNewList: list = None,
						tmpOldList: list = None,
						data: tuple = None, fromIdWare: str = None):
		
		listNew = tmpNewList
		listOld = tmpOldList
		NewListCopy = listNew.copy()
		variable = False
		#>esta parte es para ordenar las tablas NewItemTable y OldItemTable
		for i in listOld:
			for j in listNew:
				if i['cod'] == j['cod']:
					j['qtyOld'] = i['qtyOld']
					variable = True
			if not variable:
				NewListCopy.append(i)
			variable = False
		list2DB = list(map(lambda x: (str(x['cod'].split('_')[1]),str(x['qtyNew']) if x['qtyNew'] else '0', str(x['qtyOld']) if x['qtyOld'] else '0' ), NewListCopy))
		#>esta parte es para ordenar las tablas NewItemTable y OldItemTable
		
		try:
			idTS = str(int(time.time()))
			query = f"insert into genesisDB.transfer_ (codeTS, fromWareId, toWareId, fromUser, fromDate, state) values ('{idTS}', (select id from genesisDB.ware where code = '{fromWareCod}'), (select id from genesisDB.ware where code = '{toWareCod}'), '{fromUserName}', '{str(date.today())}', 3);"
			stmt = f"insert into genesisDB.transfer_product (idTransfer, idProduct, qtyNew, qtyOld) values ('{idTS}', %s, %s, %s)"
			self.connect_db()
			self.cursor.execute(query)
			self.cursor.executemany(stmt, list2DB)
			#>Empieza la actualizacion de cantidades en DB
			if not self.update_quantity(listNew=listNew, listOld=listOld,operationType='salida', idWare=fromIdWare, isGestorRequest=True):
				self.disconnect_db()
				return False
			#>Termina la actualizacion de cantidades en DB
			self.mydb.commit()
		
		except mysql.connector.Error as error:
			print("Error: {}".format(error))
			return False

		except Exception as error:
			print("An error occurred:", error)
			return False

		finally:
			try:
				if self.mydb.is_connected():
					self.disconnect_db()
					return True
			except:
				print("DB did not connect")

class users_gestor:
	_pswHashed = "Ivan Rojas"

	@property
	def pswHashed(self) -> str:
		return self._pswHashed
	
	@pswHashed.setter
	def pswHashed(self, initialPsw: str = None) -> None:
		if bool(initialPsw) and len(initialPsw) > 0:
			_pswHashed = initialPsw
		else:
			print("Something wrong happened")

	@pswHashed.getter
	def pswHashed(self) -> None:
		return self._pswHashed 

	def checkCurrentUserByPwd(self, parent=None):
		text, isPressedOk = QInputDialog.getText(parent, 'Validar usuario', 'Ingrese contraseña', QtWidgets.QLineEdit.Password)
		if(isPressedOk) and bool(text) and len(text) > 0:
			checkAnswer = bcrypt.checkpw(bytes(text, "utf-8"), bytes(self.pswHashed, "utf-8"))
			if checkAnswer: return (True, 'acepted')
			if not checkAnswer: return (False, 'denied')
		else:
			return (False, "aborted")
	
	def __init__(self):
		self.userList = []
		self.fill_users()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	def connectDB(self):
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST'), user= env_config.get('MYSQL_USER'), passwd= env_config.get('MYSQL_PASSWORD'), port=env_config.get('MYSQL_PORT'))
		# print("MySQL connection is open")
		self.cursor = self.mydb.cursor()

	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def createUser(self, index_value, perheaders: list = None):
		index, value = index_value
		headers = perheaders.copy()
		headers.pop(0)
		perDict = {}
		perDict.update({"enabled": bool(value[3])})
		for index, header in enumerate(headers):
			pair = {header[0]: bool(value[5+index])}
			perDict.update(pair)
		return user(value[1], value[2], None, value[0], None, perDict, value[4])
	
	def fill_users(self):
		query = ("select idDoc, user, pw, enabled, us.* from genesisDB.user u inner join genesisDB.userset us on u.userSet = us.lvl;")
		query2 = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'userset' ORDER BY ordinal_position;")
		try:
			self.connectDB()
			self.cursor.execute(query)
			userRows = self.cursor.fetchall()
			# nombres de las cabeceras de los permisos de usuario
			self.cursor.execute(query2)
			perHeaders = self.cursor.fetchall()
			self.userList = list(map(lambda x: self.createUser(x, perHeaders), enumerate(userRows)))
		
		except mysql.connector.Error as error:
			print("Error: {}".format(error))

		finally:
			try:
				if self.mydb.is_connected():
					self.disconnectDB()
					# print("MySQL connection is closed")
			except:
				print("No se pudo conectar")

	def check_login(self, usr: str = "", pwd: str = ""):
		objResult = next((obj for obj in self.userList if (obj.user == usr) and bcrypt.checkpw(bytes(pwd, "utf-8"), bytes(obj.pwd, "utf-8"))), None)
		if (bool(objResult) and objResult.auth["enabled"]):
			return objResult
		else:
			return None
	
	def checkPSW(self, Password: str = None) -> tuple:
		#areMatched: Bool
		try:
			if (isinstance(Password, str) and len(Password) > 0):
				areMatched = bcrypt.checkpw(bytes(Password, "utf-8"), bytes(self.pswHashed, "utf-8"))
				return areMatched, None
			else:
				return False, None
		except Exception as e:
			print("Error: %s" % e)
			return False, None

class transfer_gestor:
	def __init__(self, currentIdWare: int = None):
		self.getTransferNotification2Inner(currentIdWare=currentIdWare)

	def __del__(self):
		del self

	def __enter__(self):
		return self

	def __exit__(self,ext_type,exc_value,traceback):
		del self
	
	def connect_db(self):
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST'), user= env_config.get('MYSQL_USER'), passwd= env_config.get('MYSQL_PASSWORD'), port=env_config.get('MYSQL_PORT'))
		self.cursor = self.mydb.cursor()

	def disconnect_db(self):
		self.cursor.close()
		self.mydb.close()

	#obtiene todos los transfers hace inner self.transferDict
	def getTransferNotification2Inner(self, currentIdWare: int = None):
		try:
			query = f"select codeTS, wf.code as codeFrom, wt.code as codeTo, tr.fromUser, tr.toUser, tr.fromDate, tr.toDate, tr.state, tr.note, tp.idProduct, p.isbn, p.title, tp.qtyNew, tp.qtyOld from genesisDB.transfer_ as tr inner join genesisDB.transfer_product as tp on tr.codeTS = tp.idTransfer inner join genesisDB.product as p on tp.idProduct = p.id inner join genesisDB.ware as wf on wf.id = tr.fromWareId inner join genesisDB.ware as wt on wt.id = tr.toWareId where ((tr.state > 1) or (tr.toDate = '{str(date.today())}' )) and (tr.fromWareId = {str(currentIdWare)} or tr.toWareId = {str(currentIdWare)});"
			self.connect_db()
			self.cursor.execute(query)
			WareProductsRows = self.cursor.fetchall()
			self.transferDict = {}
			for index, value in enumerate(WareProductsRows):
				
				if not value[0] in self.transferDict:
					self.transferDict.update({value[0]: product_transfer(idTransfer=value[0],
									fromWareCod=value[1], 
									toWareCod=value[2], 
									fromUserName=value[3], 
									toUserName=value[4], 
									fromDate=value[5], 
									toDate= value[6] if value[6] else None , 
									state=value[7], 
									notes=str(value[8]),
									idProduct=value[9], 
									isbn=str(value[10]), 
									title=value[11], 
									qtyNew=value[12], 
									qtyOld=value[13])})
				elif value[0] in self.transferDict:
					self.transferDict[value[0]].addProduct(idProduct=value[9], isbn=str(value[10]), title=value[11], qtyNew=value[12], qtyOld=value[13])

		except mysql.connector.Error as error:
			print("Error: {}".format(error))
			return None

		except Exception as error:
			print("An error occurred:", error)
			return None

		finally:
			try:
				if self.mydb.is_connected():
					self.disconnect_db()
					return True
				else:
					return False
			except:
				print("DB did not connect")

	def getTranferDict(self):
		return self.transferDict.copy()
	
	def getProductsList2Statement(self, idTranfer: str = None):
		#pattern: (qtyNew, qtyOld, iProduct)
		stmtList = list(map(lambda x: (str(x[3]), str(x[4]), str(x[0])), self.transferDict[idTranfer].getProducts()))
		return None if not len(stmtList) else stmtList
	
	#upgState: Upgrade State 3->2->1
	def upgStateInnerAndDB(self, currentUserName: str = None, idTransfer: str = None, currentWareId: id = None, isFinalStep: bool = None):
		stmtAnswer = self.getProductsList2Statement(idTransfer) if isFinalStep else None
		query = f"update genesisDB.transfer_ set toUser='{currentUserName}', state = state - 1 where codeTS = '{idTransfer}';" if not isFinalStep else f"update genesisDB.transfer_ set state = state - 1, toDate = '{str(date.today())}' where codeTS = '{idTransfer}';"
		stmt = None if not isFinalStep else "update genesisDB.ware_product set qtyNew = qtyNew + %s, qtyOld = qtyOld + %s, editDate = '" + str(date.today()) + "'  where idWare = " + str(currentWareId) + " and idProduct = %s"
		try:
			self.connect_db()
			self.cursor.execute(query)
			None if not(isFinalStep) and not(stmtAnswer) else self.cursor.executemany(stmt, stmtAnswer)
			self.mydb.commit()
			self.transferDict[idTransfer].downGradeIdStateByOne()
			self.transferDict[idTransfer].setToUserName(currentUserName) if not isFinalStep else self.transferDict[idTransfer].setToDate(date.today())
		
		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()		
			return False
		
		except Exception as error:
			print("An error occurred:", error)
			return False

		finally:
			try:
				if self.mydb.is_connected():
					self.disconnect_db()
					return True
			except:
				print("DB did not connect")
			
	def getToWareCodByIdTransfer(self, idTransfer: str = None) -> str:
		return self.transferDict[idTransfer].getToWareCod()
	
	def getIdStateByIdTransfer(self, idTransfer: str = None) -> str:
		return self.transferDict[idTransfer].getStateId()

class documents:
	def __init__(self):
		print("Hola Mundo")

	def get_PDFReport(self):
		print("Hola Mundo")

class aws_s3:
	def __init__(self) -> None:
		self.directions = {
			"product": lambda x: "C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/imgs/books_imgs/%s.jpg" % (x)
			}

	def existsLocalFile(self, filepath: str = ""):
		return True if os.path.isfile(filepath) else False

	def downloadImage(self, file_name, bucket, object_name):
		s3_client = boto3.client('s3')
		try:    
			s3_client.download_file(bucket, object_name, file_name)
		except Exception as e:
			logging.error(e)
			return False
		return True

	def get_ProductImage(self, codbook: str = ""):
		if not(not(codbook)):
			if not(self.existsLocalFile(self.directions["product"](codbook))) and self.downloadImage(self.directions["product"](codbook), "genesiscuscobucket", "%s.webp" % (codbook)):
				return True, self.directions["product"](codbook)
			elif self.existsLocalFile(self.directions["product"](codbook)):
				return True, self.directions["product"](codbook)
			else:
				return False, None






