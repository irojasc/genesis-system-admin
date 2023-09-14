import mysql.connector
import boto3
import logging
import os.path
import os
from objects import user
from objects import ware_book
from objects import book
from objects import ware
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
		for index, header in enumerate(headers):
			pair = {header[0]: bool(value[4+index])}
			perDict.update(pair)
		return ware(value[0], value[1], perDict)
	
	def load_wares(self):
		query = "select id, code, enabled, ws.* from genesisdb.ware w inner join genesisdb.wareset ws on w.warelvl = ws.lvl where enabled = true and isVirtual = False order by id asc;"
		query2 = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'wareset';")
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
class ware_gestor:
	def __init__(self):
		self.ware_list = []
		self.temp_list = []
	
	def connect_db(self):
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST_LOCAL'), user= env_config.get('MYSQL_USER_LOCAL'), passwd= env_config.get('MYSQL_PASSWORD_LOCAL'), port=env_config.get('MYSQL_PORT_LOCAL'))
		self.cursor = self.mydb.cursor()

	def disconnect_db(self):
		self.cursor.close()
		self.mydb.close()

	def update_backtablequantity(self, list = None, operacion = None, currentWare = None):
		for i in list:
			for j in self.ware_list:
				if j.objBook.cod == i["cod"]:
					if operacion == "ingreso":
						j.almacen_data["cant_" + currentWare] += i["cantidad"]
					elif operacion == "salida":
						j.almacen_data["cant_" + currentWare] -= i["cantidad"]
	"""def buscar(self, criterio, patron):
		self.temp_list.clear()
		if criterio == "cod":
			for i in self.ware_list:
				if(i.book.cod == str.upper(patron)):
					self.temp_list.append(i)
			return len(self.temp_list)
		elif criterio == "isbn":
			for i in self.ware_list:
				if(i.book.isbn == patron):
					self.temp_list.append(i)
			return len(self.temp_list)
		elif criterio == "nombre":
			for i in self.ware_list:
				if(i.book.name.find(str.upper(patron)) >= 0):
					self.temp_list.append(i)
			return len(self.temp_list)

		elif criterio == "autor":
			for i in self.ware_list:
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

	def load_mainlist(self, wares = None):
		self.ware_list.clear()
		self.connect_db()
		try:
			initial_text = "select cod_book, isbn, name, autor, editorial, supplierID, pv, "
			last_text = "select cod as cod_book, isbn, name, autor, editorial, supplierID, pv, "

			for i in wares[1]:
				initial_text = initial_text	 + "cant_" + str(i.cod) + ", ubic_" + str(i.cod) + ", isok_" + str(i.cod) + ","
				last_text = last_text + "cant_" + str(i.cod) + ", ubic_" + str(i.cod) + ", isok_" + str(i.cod) + ","
			
			initial_text = initial_text + " true as active from genesisDB.ware_books inner join genesisDB.books on genesisDB.ware_books.cod_book = genesisDB.books.cod"
			last_text = last_text + " false as active from genesisDB.books as p left join genesisDB.ware_books as m on p.cod = m.cod_book where m.cod_book is null;"
			final_query = initial_text + " union all " + last_text
			
			query = (final_query)
			# -----------  carga data de libros  -----------
			self.cursor.execute(query)
			for params in self.cursor:
				values = self.None_Type(tuple(params))
				#values = self.None_Type((params[0], params[1], params[2], params[3], params[4], params[5], params[6],
				#						 params[7], params[8], params[9], params[10], params[11], params[12],
				#						 params[13], params[14], params[15], params[16], params[17]))
				### 0 = cod_book, 1 = isbn, 2 = name, 3 = autor, 4 = editorial, 5 = supplierID, 6= pv, 7,8,9 - 10,11,12 - 13,14,15 - 16,17,18 = cant,ubc,isok
				#objLibro = book(str(values[0]),str(values[1]),str(values[2]),str(values[3]),str(values[4]),str(values[5]),str(values[6]))
				objLibro = book(values)
				#objwareBook = ware_book(wares, objLibro,[values[7],values[10],values[13],values[16]],[values[8],values[11],values[14],values[17]],[values[9],values[12],values[15],values[18]])
				objwareBook = ware_book(objLibro, wares, values)
				self.ware_list.append(objwareBook)
			# -----------  cerrar conexion db  -----------
			self.disconnect_db()

			# -----------  eliminar los codigos de almacen que no tienen objeto libro  -----------
			#for i in ware_list:
			#	if(type(i.book) != str):
			#		self.ware_list.append(i)

		except:
			print("no pudo cargar libros almacen de DB")
			self.disconnect_db()

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
			index = list(filter(lambda x: x[1].objBook.cod == codBook, enumerate(self.ware_list)))[0][0]
			self.ware_list[index].objBook.setActive(condition)
			return True
		except Exception as error:
			return False
		
	def changeInnerItemLocation(self, codBook: str = "", location: str= "SIN UBICACION", currentWare: str= ""):
		try:
			index = list(filter(lambda x: x[1].objBook.cod == codBook, enumerate(self.ware_list)))[0][0]
			self.ware_list[index].almacen_data["ubic_" + currentWare] = location.upper();
			return True
		except Exception as error:
			return False
	
	def isZeroQuantity(self, codBook: str = ""):
		try:
			sum = 0
			index = list(filter(lambda x: x[1].objBook.cod == codBook, enumerate(self.ware_list)))[0][0]
			keys_ = list(self.ware_list[index].almacen_data.keys())
			keys_cant = list(filter(lambda x: x.split("_")[0] == "cant", keys_))
			for x in keys_cant:
				sum += abs((self.ware_list[index].almacen_data[x]))
			if sum == 0:
				return True
			else:
				return False
		except Exception as error:
			return False

	def updateInnerItem(self, codBook: str = "", data: dict = None):
		try:
			index = list(filter(lambda x: x[1].objBook.cod == codBook, enumerate(self.ware_list)))[0][0]
			self.ware_list[index].objBook.setISBN(data["isbn"]) if ("isbn" in data) else None
			self.ware_list[index].objBook.setName(data["name"]) if ("name" in data) else None
			self.ware_list[index].objBook.setAutor(data["autor"]) if ("autor" in data) else None
			self.ware_list[index].objBook.setEditorial(data["editorial"]) if ("editorial" in data) else None
			self.ware_list[index].objBook.setPv(data["pv"]) if ("pv" in data) else None
			return True
		except Exception as error:
			return False

	def insertInnerNewItem(self, data: dict = None, own_wares = None):
		if bool(data):
			book_params = (data["cod"], data["isbn"] if ("isbn" in data) else "", data["name"], data["autor"], data["editorial"], "", data["pv"], True)
			objBook = book(book_params)
			values = data["stock"] if "stock" in data else 0
			objwareBook = ware_book(objBook, own_wares, values, True)
			self.ware_list.append(objwareBook)
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
		if bool(objResult):
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






