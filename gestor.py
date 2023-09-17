import mysql.connector
import boto3
import logging
import os.path
import os
from objects import user, ware, ware_product, product
from decouple import Config, RepositoryEnv


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
		query = "select max(cast(substring(cod,4) as signed)) + 1 as next from genesisDB.books where cod like '%GN_%';"
		try:
			self.connectDB()
			self.cursor.execute(query)
			nextCod = "GN_%s" % (str(self.cursor.fetchall()[0][0]))
			self.disconnectDB()
			return True, nextCod
		except Exception as error:
			print("Something wrong happen: ", error)
			self.disconnectDB()
			return False, "CODIGO NO ENCONTRADO"

	def insertNewItemDB(self, data: dict = None, currentWare: str = None):
		if bool(len(data)) and bool(currentWare):
			query_1 = "insert into genesisDB.books (cod, isbn, name, autor, editorial, pv) values ('%s', '%s','%s','%s','%s', %s);" % (data["cod"],data["isbn"],data["name"], data["autor"], data["editorial"], data["pv"]) if ("isbn" in data) else "insert into genesisDB.books (cod, name, autor, editorial, pv) values ('%s', '%s','%s','%s','%s');" % (data["cod"], data["name"], data["autor"], data["editorial"], data["pv"])
			query_2 = "insert into genesisDB.ware_books (cod_book) values ('%s');" % (data["cod"])
			query_3 = "update genesisDB.ware_books set cant_%s = %s where cod_book = '%s';" % (currentWare, data["stock"], data["cod"]) if ("stock" in data) else False
			try:
				self.connectDB()
				self.cursor.execute(query_1)
				self.cursor.execute(query_2)
				if bool(query_3): self.cursor.execute(query_3)
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

	def update_backtablequantity(self, list = None, operacion = None, currentWare = None):
		for i in list:
			for j in self.innerWareList:
				if j.objBook.cod == i["cod"]:
					if operacion == "ingreso":
						j.almacen_data["cant_" + currentWare] += i["cantidad"]
					elif operacion == "salida":
						j.almacen_data["cant_" + currentWare] -= i["cantidad"]
	"""def buscar(self, criterio, patron):
		self.temp_list.clear()
		if criterio == "cod":
			for i in self.innerWareList:
				if(i.book.cod == str.upper(patron)):
					self.temp_list.append(i)
			return len(self.temp_list)
		elif criterio == "isbn":
			for i in self.innerWareList:
				if(i.book.isbn == patron):
					self.temp_list.append(i)
			return len(self.temp_list)
		elif criterio == "nombre":
			for i in self.innerWareList:
				if(i.book.name.find(str.upper(patron)) >= 0):
					self.temp_list.append(i)
			return len(self.temp_list)

		elif criterio == "autor":
			for i in self.innerWareList:
				if(i.book.autor.find(str.upper(patron)) >= 0):
					self.temp_list.append(i)
			return len(self.temp_list)
		return 0"""

	def update_quantity(self, list_, tipo, currentWare = "", location = ""):
		dict = { "ingreso": "+",
		"salida": "-"}
		temp_list = []
		self.connect_db()
		try:
			for j in list_:
				temp_list.append((str(j["cantidad"]), j["cod"]))
			if location == "":
				query_ = ("update genesisDB.ware_books set cant_" + currentWare + " = cant_" + currentWare + " " + dict[
					tipo] + " %s where cod_book = %s")
			else:
				query_ = ("update genesisDB.ware_books set cant_" + currentWare + " = cant_" + currentWare + " " + dict[
					tipo] + " %s, ubic_" + currentWare + " = '" + location.upper() + "' where cod_book = %s")

			self.cursor.executemany(query_, temp_list)
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
	
	def createWareProduct(self):
		pass


	def load_mainlist(self, wares: tuple = None):
		query = ("select w.code, i.code, p.id, isbn, title, autor, publisher, dateOut, language, pages, edition, cover, width, height, qtyNew,  qtyOld, qtyMinimun, pvNew, pvOld, dsct, loc, isEnabled from genesisdb.product p inner join genesisdb.ware_product wp on wp.idProduct = p.id inner join genesisdb.language l on l.id = p.idLanguage inner join genesisdb.ware w on w.id = wp.idWare inner join genesisdb.item i on i.id = p.idItem order by p.id asc;")
		try:
			self.innerWareList.clear()
			self.connect_db()
			self.cursor.execute(query)
			WareProductsRows = self.cursor.fetchall()

			for WareProduct in WareProductsRows:
				if not(len(self.innerWareList)):
					item = product(WareProduct[1], WareProduct[2], WareProduct[3], WareProduct[4], WareProduct[5], WareProduct[6],
					WareProduct[7].strftime("%Y"), WareProduct[8], WareProduct[9], WareProduct[10], WareProduct[11], WareProduct[12], WareProduct[13])
					wareproduct = ware_product(item, {})
					wareproduct.addDataWareProduct(WareProduct[0], WareProduct[14], WareProduct[15], WareProduct[16], WareProduct[17], WareProduct[18], WareProduct[19], WareProduct[20], WareProduct[21])
					self.innerWareList.append(wareproduct)
				else:
					index = next((i for i, item in enumerate(self.innerWareList) if item.product.prdCode == '%s_%d' % (WareProduct[1], WareProduct[2])), None)
					if isinstance(index, int):
						self.innerWareList[index].addDataWareProduct(WareProduct[0], WareProduct[14], WareProduct[15], WareProduct[16], WareProduct[17], WareProduct[18], WareProduct[19], WareProduct[20], WareProduct[21])
					else:
						item = product(WareProduct[1], WareProduct[2], WareProduct[3], WareProduct[4], WareProduct[5], WareProduct[6],
						WareProduct[7].strftime("%Y"), WareProduct[8], WareProduct[9], WareProduct[10], WareProduct[11], WareProduct[12], WareProduct[13])
						wareproduct = ware_product(item, {})
						wareproduct.addDataWareProduct(WareProduct[0], WareProduct[14], WareProduct[15], WareProduct[16], WareProduct[17], WareProduct[18], WareProduct[19], WareProduct[20], WareProduct[21])
						self.innerWareList.append(wareproduct)

		except mysql.connector.Error as error:
			print("Error: {}".format(error))
		finally:
			try:
				if self.mydb.is_connected():
					self.disconnect_db()
			except:
				print("No se pudo conectar a DB en load_mainlist")



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
			book_params = (data["cod"], data["isbn"] if ("isbn" in data) else "", data["name"], data["autor"], data["editorial"], "", data["pv"], True)
			objBook = book(book_params)
			values = data["stock"] if "stock" in data else 0
			objwareBook = ware_product(objBook, own_wares, values, True)
			self.innerWareList.append(objwareBook)
			return True
		else:
			return False

class users_gestor:
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
		objResult = next((obj for obj in self.userList if (obj.user == usr and obj.pwd == pwd)), None)
		if (bool(objResult) and objResult.auth["enabled"]):
			return objResult
		else:
			return None

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






