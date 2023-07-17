import mysql.connector
from objects import user
from objects import ware_book
from objects import book
from objects import ware_
from decouple import Config, RepositoryEnv


DOTENV_FILE = 'C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))
ROOT = 'C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/'

# ware_gestor: maneja datos de almacen
class wares_gestor:
	def __init__(self, condition = "main"):
		if condition == "main":
			self.wares = []
			self.load_wares()

	def connectDB(self):
		try:
			self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST'), user= env_config.get('MYSQL_USER'), passwd= env_config.get('MYSQL_PASSWORD'), port=env_config.get('MYSQL_PORT'))
			self.cursor = self.mydb.cursor()
		except:
			print("No se puede conectar a genesisDB")
			self.cursor.close()
			self.mydb.close()

	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def load_wares(self):
		self.connectDB()
		query = "select * from genesisDB.wares where enabled = true order by id asc;"
		try:
			self.cursor.execute(query)
			# param5: ware enabled, param6: tooltip enabled
			for (param1, param2, param3, param4, param5, param6) in self.cursor:
				objWare = ware_(param2, param3, bool(param5), bool(param6))
				self.wares.append(objWare)
			self.disconnectDB()
		except:
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

	def sort_ware(self):
		# funcion que mueve a primera posicion los datos de almacen actual
		self.wares.insert(0, self.wares.pop(next((i for i, item in enumerate(self.wares) if item.cod == self.abrev), -1)))

	def exist_ware(self):
		ware_name = ""
		try:
			file = open(ROOT + "registro.txt", "r")
			vect = file.readlines()
			self.abrev = vect[0].split(":")[1].strip('\n')
			ware_name = vect[1].split(":")[1].strip('\n')
			for i in self.wares:
				if i.cod == self.abrev:
					file.close()
					self.sort_ware()
					return True, (i.cod, self.wares, (i.enabled, i.toolTip)), ware_name
			file.close()
			return False, None, "UNKNOWN"
		except:
			file.close()
			return False, None, "UNKNOWN"

	def upload_location(self, almc = "", cod_book = "", ubic = ""):
		self.connectDB()
		#query = "use genesisDB;"
		query = ("update genesisDB.ware_books set genesisDB.ware_books.ubic_" + almc + " = '" + ubic + "' where genesisDB.ware_books.cod_book = '" + cod_book + "';")
		try:
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnectDB()
		except:
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

# ware_gestor: maneja de items en almacen
class ware_gestor:
	def __init__(self):
		self.ware_list = []
		self.temp_list = []
	
	def connect_db(self):
		self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST'), user= env_config.get('MYSQL_USER'), passwd= env_config.get('MYSQL_PASSWORD'), port=env_config.get('MYSQL_PORT'))
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

	def activateItem(self, codBook: str = ""):
		try:
			self.connect_db()
			query = ("insert into genesisDB.ware_books (cod_book) values ('%s')" % (codBook))
			self.cursor.execute(query)
			self.mydb.commit()
			self.disconnect_db()
			return True
		except:
			print("No se puede conectar a DB en activación de item")
			self.disconnect_db()
			return False

class users_gestor:
	def __init__(self):
		self.users = []
		self.fill_users()
		#try:
		#	self.mydb = mysql.connector.connect(host = "mysql-28407-0.cloudclusters.net", user="admin01", passwd="alayza2213", port="28416")
		#	self.cursor = self.mydb.cursor()
		#except:
		#	print("No se puede conectar a genesisDB")
		#	self.cursor.close()
		#	self.mydb.close()

	def connectDB(self):
		try:
			self.mydb = mysql.connector.connect(host = env_config.get('MYSQL_HOST'), user= env_config.get('MYSQL_USER'), passwd= env_config.get('MYSQL_PASSWORD'), port=env_config.get('MYSQL_PORT'))
			self.cursor = self.mydb.cursor()
		except:
			print("No se puede conectar a genesisDB")
			self.cursor.close()
			self.mydb.close()

	def disconnectDB(self):
		self.cursor.close()
		self.mydb.close()

	def fill_users(self):
		self.connectDB()
		query = ("use genesisDB;")
		query1 = ("select * from users;")
		try:
			self.cursor.execute(query)
			self.cursor.execute(query1)
			#param2: usr, param3: pssswd, param4: name, param5: doc, param6: phone, param7: enabled
			for (param1, param2, param3, param4, param5, param6, param7, param8) in self.cursor:
				objUser = user(param2, param3, param4, param5, param6, bool(param7), bool(param8))
				self.users.append(objUser)
			self.disconnectDB()
		except:
			print("No se puede conectar a genesisDB")
			self.disconnectDB()

	def check_login(self, name, passwd):
		for i in self.users:
			if i.user == name and i.passwd == passwd:
				return True, (i.user, self.users, i.enabled, i.purchaseEnabled)
		return False, (i.user, self.users, False)


class documents:
	def __init__(self):
		print("Hola Mundo")

	def get_PDFReport(self):
		print("Hola Mundo")






