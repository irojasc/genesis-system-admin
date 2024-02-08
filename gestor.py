import mysql.connector
import boto3
import logging
import os.path
import os
from objects import user, ware, ware_product, product
from decouple import Config, RepositoryEnv
from datetime import datetime, date
import bcrypt


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
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST_LOCAL'), user= env_config.get('MYSQL_USER_LOCAL'), passwd= env_config.get('MYSQL_PASSWORD_LOCAL'), port=env_config.get('MYSQL_PORT_LOCAL'))
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
		query = "select id, code, enabled, isVirtual, ws.* from genesisdb.ware w inner join genesisdb.wareset ws on w.warelvl = ws.lvl where enabled = true order by id asc;"
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

	def updateDataItem(self, cod: str = "", data: dict = None):
		init = "update genesisDB.books set "
		for item in list(data.keys()):
			if item != "pv":
				init = init + item + ' = "' + data[item] + '", '
			else:
				init = init + item + ' = ' + data[item] + ', '
		init = init[:len(init)-2] + ' where cod = "'+ cod + '"'
		query = (init)
		try:
			self.connectDB()
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnectDB()
			return True
		except Exception as error:
			print("Something wrong happen: ", error)
			self.disconnectDB()
			return False

	def getNextCodDB(self):
		query = "SELECT 'next', max(cast(p.id as signed)) + 1 as next, null, null FROM genesisdb.product p UNION SELECT 'item', i.id, i.item, i.code FROM genesisdb.item i UNION SELECT 'lang', l.id, l.language, null FROM genesisdb.language l UNION SELECT 'ctgy',c.id, c.ctgy, c.lvl FROM genesisdb.category c UNION SELECT 'ware', null, `name`, cast(`isVirtual` as UNSIGNED) FROM genesisdb.ware w where w.enabled = 1;"
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
			availableWares = list(map(lambda x: (x[2], x[3]),list(filter(lambda x: True if (x[0] == 'ware') else False, data))))
			print(availableWares)
			data_dict = {"next": nextCode, "items": items, "languages": languages,"category1": category1, "category2": category2, "category3": category3, "wares": availableWares}
			self.disconnectDB()
			return True, data_dict
		except Exception as error:
			print("Something wrong happen: ", error)
			self.disconnectDB()
			return False, None

	def insertNewItemDB(self, data: dict = None, currentWare: str = None):

		#anteriormente se lee el spinbox stock para ver si te tiene que agregar cantidad a nuevo producto
		
		if bool(len(data)) and bool(currentWare):
			
			#esta parte es para hacer las subconsultas
			if "idItem" in data:
				data["idItem"] = "(select id from genesisdb.item where item = '" + str(data["idItem"][1]) + "')"
			if "idLanguage" in data:
				data["idLanguage"] = "(select id from genesisdb.language where language = '" + data["idLanguage"][1] + "')"

			#esta parte para crear el string separado por comas
			fieldsCSV = ",".join(tuple(data.keys()))
			valuesCSV = ",".join(tuple("'" + value + "'" if (isinstance(value, str) and key !="idItem" and key != "idLanguage") else str(value) for key, value in data.items()))
			query_1 = "insert into genesisdb.product (" + fieldsCSV + ") values (" + valuesCSV + ");"
			
			try:
				self.connectDB()
				self.cursor.execute(query_1)
				self.mydb.commit()
				self.disconnectDB()
				return True
			except Exception as error:
				print("Something wrong happen: ", error)
				self.disconnectDB()
				return False

# ware_gestor: maneja de items en almacen
class WareProduct:
	def __init__(self):
		self.innerWareList = []
		self.temp_list = []
	
	def connect_db(self):
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST_LOCAL'), user= env_config.get('MYSQL_USER_LOCAL'), passwd= env_config.get('MYSQL_PASSWORD_LOCAL'), port=env_config.get('MYSQL_PORT_LOCAL'))
		self.cursor = self.mydb.cursor()

	def disconnect_db(self):
		self.cursor.close()
		self.mydb.close()

	def update_backtablequantity(self, newList: list = None, oldList: list = None, operationType: str = None, currentWare = None):
		mainList = newList + oldList
		for i in mainList:
			# formato de i: {'loc': 'ubic', 'cod': 'gn_x', 'isbn': '13dgs..', 'title': 'title', 'qtyNew': x, 'qtyOld': y}
			for j in self.innerWareList:
				if j.product.prdCode == i["cod"] and i["qtyOld"] == None:
					if operationType == "ingreso":
						j.wareData[currentWare]["qtyNew"] += i["qtyNew"]
					elif operationType == "salida":
						j.wareData[currentWare]["qtyNew"] -= i["qtyNew"]

				elif j.product.prdCode == i["cod"] and i["qtyNew"] == None:
					if operationType == "ingreso":
						j.wareData[currentWare]["qtyOld"] += i["qtyOld"]
					elif operationType == "salida":
						j.wareData[currentWare]["qtyOld"] -= i["qtyOld"]

	def update_quantity(self, listNew: list[int] = None, listOld: list[int] = None, operationType: str = "", idWare: str = "", location: str = ""):
		oprDict = { "ingreso": "+",
		"salida": "-"}
		tmp_NewList = []
		tmp_OldList = []
		self.connect_db()
		try:
			# for j in listNew:
			# 	tmp_NewList.append((str(j["cantidad"]), j["cod"]))
			tmp_NewList = list(map(lambda x: (str(x["qtyNew"]), str(0), x["cod"].split("_")[1]), listNew))
			tmp_OldList = list(map(lambda x: (str(0), str(x["qtyOld"]), x["cod"].split("_")[1]), listOld))
			tmp_MainList = tmp_NewList + tmp_OldList

			if location == "":
				query_ = ("update genesisdb.ware_product set qtyNew = qtyNew " + oprDict[
					operationType] + " %s, qtyOld = qtyOld " + oprDict[
					operationType] + " %s, editDate = '" + str(date.today()) + "' where idProduct = %s and idWare = " + idWare)
			else:
				query_ = ("update genesisdb.ware_product set qtyNew = qtyNew " + oprDict[
					operationType] + " %s, qtyOld = qtyOld " + oprDict[
					operationType] + " %s, editDate = '" + str(date.today()) + "', loc = '" + location.upper() + "' where idProduct = %s and idWare = " + idWare)

			self.cursor.executemany(query_, tmp_MainList)
			self.mydb.commit()
			self.disconnect_db()
			return True

		except mysql.connector.Error as err:
			print("Something went wrong: {}".format(err))
			self.disconnect_db()		
			return False
		
	def None_Type(self, val):
		myList = []
		for i in range(len(val)):
			if val[i] is None:
				myList.append("")
			else:
				myList.append(val[i])
		if len(val) > 1:
			tup = tuple(myList)
		else:
			tup = ()
		return tup
	
	def loadInnerTable(self, updateDate: datetime.date = None):
		
		query = ("select w.code, i.code, p.id, isbn, title, autor, publisher, dateOut, language, pages, edition, cover, width, height, qtyNew,  qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled from genesisdb.product p left join genesisdb.ware_product wp on wp.idProduct = p.id inner join genesisdb.language l on l.id = p.idLanguage left join genesisdb.ware w on w.id = wp.idWare inner join genesisdb.item i on i.id = p.idItem order by p.id asc;") if updateDate == None else ("select w.code, i.code, p.id, isbn, title, autor, publisher, dateOut, language, pages, edition, cover, width, height, qtyNew,  qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled from genesisdb.product p left join genesisdb.ware_product wp on wp.idProduct = p.id inner join genesisdb.language l on l.id = p.idLanguage left join genesisdb.ware w on w.id = wp.idWare inner join genesisdb.item i on i.id = p.idItem where p.creationDate >= '{0}' or p.editDate >= '{0}' or wp.editDate >= '{0}' or p.creationDate >= '{0}' order by p.id asc;".format(updateDate))

		try:
			# self.innerWareList.clear()
			self.connect_db()
			self.cursor.execute(query)
			WareProductsRows = self.cursor.fetchall()
			for WareProduct in WareProductsRows:
				if not(len(self.innerWareList)):
					item = product(WareProduct[1], WareProduct[2], WareProduct[3], WareProduct[4], WareProduct[5], WareProduct[6],
					WareProduct[7], WareProduct[8], WareProduct[9], WareProduct[10], WareProduct[11], WareProduct[12], WareProduct[13])
					wareproduct = ware_product(item, {})
					wareproduct.addDataWareProduct(WareProduct[0], WareProduct[14], WareProduct[15], WareProduct[16], WareProduct[17], WareProduct[18], WareProduct[19], WareProduct[20], WareProduct[21])
					self.innerWareList.append(wareproduct)
				else:
					index = next((i for i, item in enumerate(self.innerWareList) if item.product.prdCode == '%s_%d' % (WareProduct[1], WareProduct[2])), None)
					if isinstance(index, int):
						if updateDate != None:
							self.innerWareList[index].product = product(WareProduct[1], WareProduct[2], WareProduct[3], WareProduct[4], WareProduct[5], WareProduct[6],
					WareProduct[7], WareProduct[8], WareProduct[9], WareProduct[10], WareProduct[11], WareProduct[12], WareProduct[13])
						self.innerWareList[index].addDataWareProduct(WareProduct[0], WareProduct[14], WareProduct[15], WareProduct[16], WareProduct[17], WareProduct[18], WareProduct[19], WareProduct[20], WareProduct[21])
					else:
						# print("[destructured]",WareProduct[1],WareProduct[2],WareProduct[3],WareProduct[4],WareProduct[5],WareProduct[6],WareProduct[7],WareProduct[8],WareProduct[9],WareProduct[10],WareProduct[11],WareProduct[12],WareProduct[13])
						item = product(WareProduct[1], WareProduct[2], WareProduct[3], WareProduct[4], WareProduct[5], WareProduct[6],
						WareProduct[7], WareProduct[8], WareProduct[9], WareProduct[10], WareProduct[11], WareProduct[12], WareProduct[13])
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

	def activateItem(self, codBook: str = "", condition: bool = True):
		try:
			if self.activateInnerItemState(codBook, condition):
				self.connect_db()
				if condition:
					query = ("insert into genesisDB.ware_books (cod_book) values ('%s')" % (codBook))
				else:
					query = ("delete from genesisDB.ware_books where cod_book = '%s'" % (codBook))
				self.cursor.execute(query)
				self.mydb.commit()
				self.disconnect_db()
				return True
			else:
				return False
		except Exception as error:
			print("Location: Activating Item: ", error)
			self.disconnect_db()
			return False
		
	def changeItemLocation(self, codBook: str = "", location: str= "SIN UBICACION", currentWare: str=""):
		try:
			if self.changeInnerItemLocation(codBook, location, currentWare):
				self.connect_db()
				query = ("update genesisDB.ware_books set genesisDB.ware_books.ubic_" + currentWare + " = '" + location.upper() + "' where genesisDB.ware_books.cod_book = '" + codBook + "';")
				self.cursor.execute(query)
				self.mydb.commit()
				self.disconnect_db()
				return True
			else:
				return False
		except Exception as error:
			print("Location: Activating Item: ", error)
			self.disconnect_db()
			return False
		
	def activateInnerItemState(self, codBook: str = "", condition: bool = True):
		try:
			index = list(filter(lambda x: x[1].objBook.cod == codBook, enumerate(self.innerWareList)))[0][0]
			self.innerWareList[index].objBook.setActive(condition)
			return True
		except Exception as error:
			return False
		
	def changeInnerItemLocation(self, codBook: str = "", location: str= "SIN UBICACION", currentWare: str= ""):
		try:
			index = list(filter(lambda x: x[1].objBook.cod == codBook, enumerate(self.innerWareList)))[0][0]
			self.innerWareList[index].almacen_data["ubic_" + currentWare] = location.upper();
			return True
		except Exception as error:
			return False
	
	def isZeroQuantity(self, codBook: str = ""):
		try:
			sum = 0
			index = list(filter(lambda x: x[1].objBook.cod == codBook, enumerate(self.innerWareList)))[0][0]
			keys_ = list(self.innerWareList[index].almacen_data.keys())
			keys_cant = list(filter(lambda x: x.split("_")[0] == "cant", keys_))
			for x in keys_cant:
				sum += abs((self.innerWareList[index].almacen_data[x]))
			if sum == 0:
				return True
			else:
				return False
		except Exception as error:
			return False

	def updateInnerItem(self, codBook: str = "", data: dict = None):
		try:
			index = list(filter(lambda x: x[1].objBook.cod == codBook, enumerate(self.innerWareList)))[0][0]
			self.innerWareList[index].objBook.setISBN(data["isbn"]) if ("isbn" in data) else None
			self.innerWareList[index].objBook.setName(data["name"]) if ("name" in data) else None
			self.innerWareList[index].objBook.setAutor(data["autor"]) if ("autor" in data) else None
			self.innerWareList[index].objBook.setEditorial(data["editorial"]) if ("editorial" in data) else None
			self.innerWareList[index].objBook.setPv(data["pv"]) if ("pv" in data) else None
			return True
		except Exception as error:
			return False

	def insertInnerNewItem(self, data: dict = None, own_wares = None):
		if bool(data):

			objProduct = product(data["idItem"][2], 
						data["id"], 
						None if not("isbn" in data) else data["isbn"],
						data["title"], data["autor"], data["publisher"], 
						None if not("dateOut" in data) else data["dateOut"],
						None if not("idLanguage" in data) else data["idLanguage"][1],
						None if not("pages" in data) else data["pages"],
						None if not("edition" in data) else data["edition"],
						None if not("cover" in data) else data["cover"],
						None if not("width" in data) else data["width"],
						None if not("eight" in data) else data["height"])
			
			objwareBook = ware_product(objProduct)
			self.innerWareList.append(objwareBook)
			return True
		else:
			return False

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

	def __init__(self):
		self.userList = []
		self.fill_users()

	def connectDB(self):
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST_LOCAL'), user= env_config.get('MYSQL_USER_LOCAL'), passwd= env_config.get('MYSQL_PASSWORD_LOCAL'), port=env_config.get('MYSQL_PORT_LOCAL'))
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
		query = ("select idDoc, user, pw, enabled, us.* from genesisdb.user u inner join genesisdb.userset us on u.userSet = us.lvl;")
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
				return True, areMatched
			else:
				return False, None
		except Exception as e:
			print("Error: %s" % e)
			return False, None

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






