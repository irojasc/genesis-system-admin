from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QColor, QMouseEvent, QKeyEvent, QWheelEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QDate, Qt
from gestor import users_gestor
import copy
import math


class ui_EditNewItemDialog(QtWidgets.QDialog):
    # Type: False: Edit , True: New
    def __init__(self, method: bool = False, currentWare: str = None, parent=None):
        super(ui_EditNewItemDialog, self).__init__(parent)
        (self.setCurrentWare(currentWare=currentWare)) if (currentWare) else None
        self.method = method
        self.code = ""
        self.title = ""
        self.PrevItemPvpOld = ""
        self.returnedVal = (False, None, None)
        self.setupUi()

    def __del__(self):
        print("getting out from edit/new form ")
    
    def __enter__(self):
        return self
    
    def __exit__(self,ext_type,exc_value,traceback):
        del self

    def setCurrentWare(self, currentWare: str = None):
        self.currentWare = currentWare

    def saveDataFieldsAt(self):
        if len(self.txtISBN.text()) and self.prevData.product.getISBN() != self.txtISBN.text(): 
            self.prevData.product.setISBN(self.txtISBN.text())
        elif not(len(self.txtISBN.text())):
            self.prevData.product.setISBN(None)
        #title, autor, publisher
        if bool(self.txtTitle.text()) and self.prevData.product.getTitle() != self.txtTitle.text(): self.prevData.product.setTitle(self.txtTitle.text())
        if bool(self.txtAutor.text()) and self.prevData.product.getAutor() != self.txtAutor.text(): self.prevData.product.setAutor(self.txtAutor.text())
        if bool(self.txtPublisher.text()) and self.prevData.product.getPublisher() != self.txtPublisher.text(): self.prevData.product.setPublisher(self.txtPublisher.text())

        #dateOut
        if (self.dateOutWidget.date().year() != 1752) and self.prevData.product.getDateOut() != self.dateOutWidget.date().toString("yyyy-MM-dd"): 
            self.prevData.product.setDateOut(self.dateOutWidget.date().toString("yyyy-MM-dd"))
        elif (self.dateOutWidget.date().year() == 1752): self.prevData.product.setDateOut(None)

        #edition
        if (self.editionSpinBox.value() != 0) and self.prevData.product.getEdition() != self.editionSpinBox.value():
            self.prevData.product.setEdition(self.editionSpinBox.value())
        elif (self.editionSpinBox.value() == 0): self.prevData.product.setEdition(None)

        #pages
        if (self.pagesSpinBox.value() != 0) and self.prevData.product.getPages() != self.pagesSpinBox.value():
            self.prevData.product.setPages(self.pagesSpinBox.value())
        elif (self.pagesSpinBox.value() == 0): self.prevData.product.setPages(None)

        #languages
        if (self.cmbIdiom.currentIndex() != -1) and self.prevData.product.getLang() != self.cmbIdiom.currentText():
            self.prevData.product.setLang(self.cmbIdiom.currentText())
        elif (self.cmbIdiom.currentIndex() == -1): self.prevData.product.setLang(None)

        #cover
        if (self.cmbCover.currentIndex() != -1) and self.prevData.product.getCover() != self.cmbCover.currentIndex():
            self.prevData.product.setCover(self.cmbCover.currentIndex())
        elif (self.cmbCover.currentIndex() == -1): self.prevData.product.setCover(-1)

        #width
        if (self.widthSpinBox.value() != 0) and self.prevData.product.getWidth() != self.widthSpinBox.value():
            self.prevData.product.setWidth(self.widthSpinBox.value())
        elif (self.widthSpinBox.value() == 0): self.prevData.product.setWidth(None)

        #height
        if (self.heightSpinBox.value() != 0) and self.prevData.product.getHeight() != self.heightSpinBox.value():
            self.prevData.product.setHeight(self.heightSpinBox.value())
        elif (self.heightSpinBox.value() == 0): self.prevData.product.setHeight(None)

        #content
        if len(self.contentTxtEdit.toPlainText().strip()) and self.contentTxtEdit.toPlainText().strip() != self.prevData.product.getContent():
            self.prevData.product.setContent(self.contentTxtEdit.toPlainText().strip())
        elif not(len(self.contentTxtEdit.toPlainText().strip())): self.prevData.product.setContent(None)

        objCopied = copy.deepcopy(self.prevData)

        if bool(self.wareTableItemData.rowCount()):
            for index, value in enumerate(self.prevData.wareData):
                wareName = self.wareTableItemData.verticalHeaderItem(index).text()
                if self.wareTableItemData.cellWidget(index, 0).isChecked() and wareName == value:
                    loc_ = self.wareTableItemData.cellWidget(index,2).text().upper() if self.wareTableItemData.cellWidget(index,2).text() != "" else "SIN UBICACION"
                    min = self.wareTableItemData.cellWidget(index, 3).value()
                    new = float(self.wareTableItemData.item(index, 4).text()) if self.wareTableItemData.item(index, 4).text() != "" else 0.0
                    old = float(self.wareTableItemData.item(index, 5).text()) if self.wareTableItemData.item(index, 5).text() != "" else 0.0
                    descuento = self.wareTableItemData.cellWidget(index, 6).value()
                    enabled = True if self.wareTableItemData.cellWidget(index, 1).isChecked() else False
                    exists = True if self.wareTableItemData.cellWidget(index, 0).isChecked() else False
                    objCopied.updateWareFields(wareName=value, 
                                                    qtyMinimun=min,
                                                    pvNew=new,
                                                    pvOld=old,
                                                    dsct=descuento,
                                                    isEnabled=enabled,
                                                    isExists=exists,
                                                    loc=loc_,
                                                    idWare=self.prevData.wareData[value]["idWare"],
                                                    isVirtual=self.prevData.wareData[value]["isVirtual"])
                
                elif not(self.wareTableItemData.cellWidget(index, 0).isChecked()) and wareName == value:
                    objCopied.removePairKeyValue(value)

            #si no agrega ningun ware, entonces agrega un unico almacen None
            if not(bool(objCopied.getWareDataLen())):
                objCopied.clearWareData()
                objCopied.addDataWareProduct(wareName=None, qtyNew=None, qtyOld=None, qtyMinimun=None, pvNew=None, pvOld=None, dsct=None, loc="SIN UBICACION", isEnabled=None, isExists=None)
            
        elif not(bool(self.wareTableItemData.rowCount())):
                objCopied.clearWareData()
                objCopied.addDataWareProduct(wareName=None, qtyNew=None, qtyOld=None, qtyMinimun=None, pvNew=None, pvOld=None, dsct=None, loc="SIN UBICACION", isEnabled=None, isExists=None)


        return objCopied

    def saveEvent(self, btnConfirmation: bool = False):
        #isCancel sirve para indicar que la operacion es de cancelar solo durante operacione editar
        # se cambia los keys de los diccionarios segun titulos de base de datos
        # self.method True para cuando se crea un nuevo item
        tmp_dict = {}

        if btnConfirmation and not(self.method):
            bool_answer, text_answer = self.userValidation()
            if bool_answer and text_answer == 'acepted':
                self.returnedVal = (True, self.saveDataFieldsAt(), 'salvar')
            elif not(bool_answer) and text_answer == 'denied':
                QMessageBox.warning(self, 'Alerta',"Error durante operación", QMessageBox.Ok, QMessageBox.Ok)
        
        elif btnConfirmation and self.method:
        ######
            objItem = product(itemCode=self.dataItems[self.cmbItem.currentIndex()][2])
            objItem.setId(int(self.txtId.text().strip()))
            if bool(len(self.txtTitle.text().strip())):
                objItem.setTitle(self.txtTitle.text().strip())
            if bool(len(self.txtAutor.text().strip())):
                objItem.setAutor(self.txtAutor.text().strip())
            if bool(len(self.txtPublisher.text().strip())):
                objItem.setPublisher(self.txtPublisher.text().strip())
            if bool(len(self.cmbItem.currentText().strip())):
                objItem.setItemCategory(self.dataItems[self.cmbItem.currentIndex()][1])
                
            if bool(objItem.getId()) and bool(objItem.getTitle()) and bool(objItem.getAutor()) and bool(objItem.getPublisher()) and bool(objItem.getItemCategory()):
                if bool(len(self.txtISBN.text().strip())): objItem.setISBN(self.txtISBN.text().strip())
                if self.dateOutWidget.date().year() != 1752: objItem.setDateOut(self.dateOutWidget.date().toString("yyyy-MM-dd"))
                if bool(self.editionSpinBox.value()): objItem.setEdition(self.editionSpinBox.value())
                if bool(self.pagesSpinBox.value()): objItem.setPages(self.pagesSpinBox.value())
                if bool(self.cmbIdiom.currentText()): objItem.setLang(self.dataLanguages[self.cmbIdiom.currentIndex()][1])
                if (self.cmbCover.currentIndex() >= -1): objItem.setCover(1 if self.cmbCover.currentIndex() == 0 else 2 if self.cmbCover.currentIndex() == 1 else None)
                if bool(self.widthSpinBox.value()): objItem.setWidth(self.widthSpinBox.value())
                if bool(self.heightSpinBox.value()): objItem.setHeight(self.heightSpinBox.value())
            #     #aqui falta la parte de categorias, esto revisar arquitectura base de datos
                if bool(len(self.contentTxtEdit.toPlainText().strip())): objItem.setContent(self.contentTxtEdit.toPlainText().strip())
                # nwDict = {}
                objWareProduct = ware_product(item=objItem, wareData={}.copy())
                if bool(self.wareTableItemData.rowCount()):
                    for index, i in enumerate(self.prevData["wares"]):
                        if self.wareTableItemData.cellWidget(index, 0).isChecked():
                            loc_ = self.wareTableItemData.cellWidget(index,2).text().upper() if self.wareTableItemData.cellWidget(index,2).text() != "" else "SIN UBICACION"
                            min = self.wareTableItemData.cellWidget(index, 3).value()
                            new = float(self.wareTableItemData.item(index, 4).text()) if self.wareTableItemData.item(index, 4).text() != "" else 0.0
                            old = float(self.wareTableItemData.item(index, 5).text()) if self.wareTableItemData.item(index, 5).text() != "" else 0.0
                            descuento = self.wareTableItemData.cellWidget(index, 6).value()
                            enabled = True if self.wareTableItemData.cellWidget(index, 1).isChecked() else False
                            exists = True if self.wareTableItemData.cellWidget(index, 0).isChecked() else False
                            objWareProduct.addDataWareProduct(wareName=i[0], qtyNew=0,
                                                                qtyOld=0, qtyMinimun=min,
                                                                pvNew=new, pvOld=old, dsct=descuento,
                                                                isEnabled=enabled, isExists=exists, loc=loc_, idWare=i[3])
                    #si no agrega ningun ware, entonces agrega un unico almacen None
                    if not(bool(len(objWareProduct.wareData))):
                        objWareProduct.addDataWareProduct(wareName=None, qtyNew=None, qtyOld=None, qtyMinimun=None, pvNew=None, pvOld=None, dsct=None, loc="SIN UBICACION", isEnabled=None, isExists=None)
                
                elif not(bool(self.wareTableItemData.rowCount())):
                    objWareProduct.addDataWareProduct(wareName=None, qtyNew=None, qtyOld=None, qtyMinimun=None, pvNew=None, pvOld=None, dsct=None, loc="SIN UBICACION", isEnabled=None, isExists=None)
                self.returnedVal = (True, objWareProduct, None)
            else:
                QMessageBox.information(self, 'Mensaje', "Llenar los campos obligatorios (*)", QMessageBox.Ok, QMessageBox.Ok)
                self.returnedVal = (False, None, None)
        ######
        else:
            self.returnedVal = (False, None, None)

        self.submitclose() if self.returnedVal[0] else False
    
    def cleanInputFields(self, isInit: str = None):
        self.cmbItem.setEnabled(False)
        self.txtISBN.setReadOnly(True)
        self.txtTitle.setReadOnly(True)
        self.txtAutor.setReadOnly(True)
        self.txtPublisher.setReadOnly(True)
        # self.spinInitStock.setReadOnly(True)
        self.dateOutWidget.setReadOnly(True)
        self.editionSpinBox.setReadOnly(True)
        self.pagesSpinBox.setReadOnly(True)
        self.widthSpinBox.setReadOnly(True)
        self.cmbIdiom.readonly = True
        self.cmbCover.readonly = True
        self.heightSpinBox.setReadOnly(True)
        self.cmbCategory1.readonly = True
        self.cmbCategory2.readonly = True
        self.cmbCategory3.readonly = True
        self.contentTxtEdit.setReadOnly(True)

        self.txtISBN.setPalette(self.darkPalette)
        self.txtTitle.setPalette(self.darkPalette)
        self.txtAutor.setPalette(self.darkPalette)
        self.txtPublisher.setPalette(self.darkPalette)

        self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
        self.editionSpinBox.setPalette(self.darkPalette)
        self.pagesSpinBox.setPalette(self.darkPalette)
        self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
        self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
        self.widthSpinBox.setPalette(self.darkPalette)
        self.heightSpinBox.setPalette(self.darkPalette)
        self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
        self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
        self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
        self.contentTxtEdit.setPalette(self.darkPalette)

        self.tab_compItemData.setEnabled(False)
        self.tab_compItemData.setEnabled(True)

        #isInit se utiliza cuando se hace cambio de tabs y no se quiere cambiar el index de los combos
        self.setInitDefaultValues() if bool(isInit) else False
    
    def setDataFields(self, languages = None, data = None):
        #Si self.method : False (Metodo Editar) --- Si self.method : True (Metodo Metodo Nuevo Producto)
        #aqui es guardar el valor de data a variable prevData

        if bool(data): self.prevData = (data.copy() if isinstance(data, dict) else data)

        if bool(self.prevData) and not(self.method):
            self.cmbItem.addItem(self.prevData.product.getItemCategory())
            self.txtId.setText(str(self.prevData.product.getId()))
            self.txtISBN.setText(self.prevData.product.getISBN())
            self.txtTitle.setText(self.prevData.product.getTitle())
            self.txtAutor.setText(self.prevData.product.getAutor())
            self.txtPublisher.setText(self.prevData.product.getPublisher())
            self.dateOutWidget.setDate(self.prevData.product.getDateOut()) if self.prevData.product.getDateOut() else None
            self.editionSpinBox.setValue(self.prevData.product.getEdition()) if self.prevData.product.getEdition() else None
            self.pagesSpinBox.setValue(self.prevData.product.getPages()) if self.prevData.product.getPages() else None
            self.cmbIdiom.addItems(list(map(lambda x: x[1], languages)))
            
            index = list(filter(lambda x: x[1] == self.prevData.product.getLang(), languages))
            self.cmbIdiom.setCurrentIndex(int(index[0][0])-1) if index else self.cmbIdiom.setCurrentIndex(-1)

            self.cmbCover.setCurrentIndex(self.prevData.product.getCover())
            self.widthSpinBox.setValue(self.prevData.product.getWidth()) if self.prevData.product.getWidth() else None
            self.heightSpinBox.setValue(self.prevData.product.getHeight()) if self.prevData.product.getHeight() else None
            self.contentTxtEdit.setText(self.prevData.product.getContent()) if self.prevData.product.getContent() else None

            #en esta parte se llenan los widget de la tabla ware product para condicion de editar nuevo 
            self.wareTableItemData.setRowCount(len(self.prevData.wareData))

            for index, i in enumerate(self.prevData.wareData):

                self.wareTableItemData.setVerticalHeaderItem(index, QTableWidgetItem(i))
                isCurrentWare = (self.wareTableItemData.verticalHeaderItem(index).text() == self.currentWare.cod) if hasattr(self, 'currentWare') else '_'
                
                #Primer Widget
                #>blocksignals
                item = QCheckBox()
                item.setStyleSheet("padding-left: 17px;")
                if len(self.prevData.wareData[i]) > 1 and self.prevData.wareData[i]['isExists']:
                    item.setChecked(True)
                    item.setEnabled(False)
                else:
                    item.setChecked(False)
                item.stateChanged.connect(self.first_callback(index, bool(self.prevData.wareData[i]['isVirtual'])))
                #cambio
                None if isCurrentWare == '_' else item.setEnabled(False) if not(isCurrentWare) else None
                self.wareTableItemData.setCellWidget(index, 0, item)
                #>
                #Segundo Widget
                item = QCheckBox(enabled = False) if not(self.wareTableItemData.cellWidget(index, 0).isChecked()) else QCheckBox(enabled = True)
                item.setStyleSheet("padding-left: 17px;")
                item.setChecked(self.prevData.wareData[i]['isEnabled']) if 'isEnabled' in self.prevData.wareData[i] else None
                item.toggled.connect(self.second_callback(row=index, wareCode=i, qtyNewOld=(self.prevData.wareData[i]["qtyNew"], self.prevData.wareData[i]["qtyOld"])))
                #cambio
                None if isCurrentWare == '_' else item.setEnabled(False) if not(isCurrentWare) else None
                self.wareTableItemData.setCellWidget(index,1,item)

                #virtual = 1, not Vitirual = 0
                #aqui evalua que el primer checkbox este checked y tambien el tipo de ware, is virtual?
                item = QLineEdit(enabled = False) if (bool(self.prevData.wareData[i]['isVirtual']) or not(self.wareTableItemData.cellWidget(index, 0).isChecked())) else QLineEdit(enabled = True)
                item.setPlaceholderText("MUEBLE ?, FILA ?")
                #background black when ware is virtual
                item.setStyleSheet("QLineEdit{background-color: black; Border: 0px;}" if self.prevData.wareData[i]['isVirtual'] else "QLineEdit{Border: 0px;}")
                (item.setText(self.prevData.wareData[i]['loc']) if not(self.prevData.wareData[i]['loc'] == 'SIN UBICACION') else None) if 'loc' in self.prevData.wareData[i] else None
                item.editingFinished.connect(self.locationLineEditCallBack(index))
                #cambio
                None if isCurrentWare == '_' else item.setEnabled(False) if not(isCurrentWare) else None
                self.wareTableItemData.setCellWidget(index,2,item)

                item = MySpinBox(enabled = False) if (bool(self.prevData.wareData[i]['isVirtual']) or not(self.wareTableItemData.cellWidget(index, 0).isChecked())) else MySpinBox(enabled = True) 
                item.setFixedWidth(59)
                item.setSuffix(" und")
                item.setStyleSheet("QSpinBox{background-color: black; Border: 0px;}" if bool(self.prevData.wareData[i]['isVirtual']) else "QSpinBox{Border: 0px;}")
                item.setValue(self.prevData.wareData[i]['qtyMinimun']) if 'qtyMinimun' in self.prevData.wareData[i] and bool(self.prevData.wareData[i]['qtyMinimun'])  else None
                #cambio
                None if isCurrentWare == '_' else item.setEnabled(False) if not(isCurrentWare) else None
                self.wareTableItemData.setCellWidget(index,3,item)

                #bloqueo cuando agregamos items
                #>
                self.wareTableItemData.blockSignals(True)
                flagChecked = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable
                flagNotChecked = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|~QtCore.Qt.ItemIsEditable
                
                item = QtWidgets.QTableWidgetItem(str(self.prevData.wareData[i]['pvNew']) if 'pvNew' in self.prevData.wareData[i] and bool(self.prevData.wareData[i]['pvNew']) else '0.0')
                item.setFlags(flagNotChecked) if not(self.wareTableItemData.cellWidget(index, 0).isChecked()) else item.setFlags(flagChecked)
                #cambio
                None if isCurrentWare == '_' else item.setFlags(flagNotChecked) if not(isCurrentWare) else None
                self.wareTableItemData.setItem(index,4,item)
                
                item = QtWidgets.QTableWidgetItem(str(self.prevData.wareData[i]['pvOld']) if 'pvOld' in self.prevData.wareData[i] and bool(self.prevData.wareData[i]['pvOld']) else '0.0')
                item.setFlags(flagNotChecked) if not(self.wareTableItemData.cellWidget(index, 0).isChecked()) else item.setFlags(flagChecked)
                #cambio
                None if isCurrentWare == '_' else item.setFlags(flagNotChecked) if not(isCurrentWare) else None
                self.wareTableItemData.setItem(index,5,item)
                self.wareTableItemData.blockSignals(False)
                #>

                item = MySpinBox(enabled=False) if not(self.wareTableItemData.cellWidget(index, 0).isChecked()) else MySpinBox(enabled=True)
                item.setMaximum(100)
                item.setSingleStep(5)
                item.setSuffix(" %")
                item.setStyleSheet("Border: 0px")
                item.setValue(self.prevData.wareData[i]['dsct'] if ('dsct' in self.prevData.wareData[i] and bool(self.prevData.wareData[i]['dsct'])) else 0)
                #cambio
                None if isCurrentWare == '_' else item.setEnabled(False) if not(isCurrentWare) else None
                self.wareTableItemData.setCellWidget(index,6,item)
      
            self.returnedVal = (True, self.saveDataFieldsAt(), 'cancelar')

        elif bool(self.prevData) and self.method:
            self.dataItems = data["items"]
            self.dataLanguages = data["languages"]
            self.txtId.setText(str(data["next"]))
            self.cmbItem.addItems(list(map(lambda x: x[1], data["items"])))
            self.cmbIdiom.addItems(list(map(lambda x: x[1], data["languages"])))
            self.cmbCategory1.setModel(QStringListModel(list(map(lambda x: x[1], data["category1"]))))
            self.cmbCategory1.setCurrentIndex(-1)
            self.cmbCategory1.setEditable(True)
            self.cmbCategory1.lineEdit().setPlaceholderText("NIVEL 1")
            self.cmbCategory2.setModel(QStringListModel(list(map(lambda x: x[1], data["category2"]))))
            self.cmbCategory2.setCurrentIndex(-1)
            self.cmbCategory2.setEditable(True)
            self.cmbCategory2.lineEdit().setPlaceholderText("NIVEL 2")
            self.cmbCategory3.setModel(QStringListModel(list(map(lambda x: x[1], data["category3"]))))
            self.cmbCategory3.setCurrentIndex(-1)
            self.cmbCategory3.setEditable(True)
            self.cmbCategory3.lineEdit().setPlaceholderText("NIVEL 3")

            #en esta parte se llenan los widget de la tabla ware product para condicion de crear new item
            self.wareTableItemData.setRowCount(len(data["wares"]))
            for index, x in enumerate(data["wares"]): 

                self.wareTableItemData.setVerticalHeaderItem(index, QTableWidgetItem(x[1]))

                item = QCheckBox()
                item.setStyleSheet("padding-left: 17px;")
                item.stateChanged.connect(self.first_callback(index, bool(int(x[2]))))
                self.wareTableItemData.setCellWidget(index, 0, item)

                item = QCheckBox(enabled = False) if not(self.wareTableItemData.cellWidget(index, 0).isChecked()) else QCheckBox(enabled = True)
                item.setStyleSheet("padding-left: 17px;")
                self.wareTableItemData.setCellWidget(index,1,item)

                #virtual = 1, not Vitirual = 0
                #aqui evalua que el primer checkbox este checked y tambien el tipo de ware, is virtual?
                item = QLineEdit(enabled = False) if (bool(int(x[2])) or not(self.wareTableItemData.cellWidget(index, 0).isChecked())) else QLineEdit(enabled = True)
                item.setPlaceholderText("MUEBLE ?, FILA ?")
                #background black when ware is virtual
                item.setStyleSheet("QLineEdit{background-color: black; Border: 0px;}" if bool(int(x[2])) else "QLineEdit{Border: 0px;}")
                item.editingFinished.connect(self.locationLineEditCallBack(index))
                self.wareTableItemData.setCellWidget(index,2,item)

                item = MySpinBox(enabled = False) if (bool(int(x[2])) or not(self.wareTableItemData.cellWidget(index, 0).isChecked())) else MySpinBox(enabled = True) 
                item.setFixedWidth(59)
                item.setSuffix(" und")
                item.setStyleSheet("QSpinBox{background-color: black; Border: 0px;}" if bool(int(x[2])) else "QSpinBox{Border: 0px;}")
                self.wareTableItemData.setCellWidget(index,3,item)

                #bloqueo cuando agregamos items
                #>
                self.wareTableItemData.blockSignals(True)

                flagChecked = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable
                flagNotChecked = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|~QtCore.Qt.ItemIsEditable
                item = QtWidgets.QTableWidgetItem("")
                item.setFlags(flagNotChecked) if not(self.wareTableItemData.cellWidget(index, 0).isChecked()) else item.setFlags(flagChecked)
                self.wareTableItemData.setItem(index,4,item)

                item = QtWidgets.QTableWidgetItem("")
                item.setFlags(flagNotChecked) if not(self.wareTableItemData.cellWidget(index, 0).isChecked()) else item.setFlags(flagChecked)
                self.wareTableItemData.setItem(index,5,item)

                self.wareTableItemData.blockSignals(False)
                #>
                item = MySpinBox(enabled=False) if not(self.wareTableItemData.cellWidget(index, 0).isChecked()) else MySpinBox(enabled=True)
                item.setMaximum(100)
                item.setSingleStep(5)
                item.setSuffix(" %")
                item.setStyleSheet("Border: 0px")
                self.wareTableItemData.setCellWidget(index,6,item)

            self.setInitDefaultValues()
    
    def setInitDefaultValues(self):
        #currentIndex 1 para item de tipo libro
        self.cmbItem.setCurrentIndex(1)
        #esto por el momento va apuntar al primer idioma
        self.cmbIdiom.setCurrentIndex(-1)
        self.cmbCover.setCurrentIndex(-1)
        self.cmbCategory1.setCurrentIndex(-1)
        self.cmbCategory2.setCurrentIndex(-1)
        self.cmbCategory3.setCurrentIndex(-1)
        # self.dateOutWidget.setStyleSheet("QDateEdit{background-color: red; color:white}")

    def closeEvent(self, event):
        self.accept()
        # event.accept()

    def firstCheckBoxChanged(self, state, row, isVirtual):
        
        if self.method or not(self.method): #NUEVO PRODUCTO y EDITAR PRODUCTO
            # state = 2: para cuando el primer checkBox is Checked
            if state == 2:
                self.wareTableItemData.cellWidget(row, 1).setEnabled(True)
                if(not(isVirtual)):
                    self.wareTableItemData.cellWidget(row, 2).setEnabled(True)
                    self.wareTableItemData.cellWidget(row, 2).setStyleSheet("QLineEdit{Border: 0.5px solid rgb(220,220,220);}")
                    self.wareTableItemData.cellWidget(row, 3).setEnabled(True)
                    self.wareTableItemData.cellWidget(row, 3).setStyleSheet("QSpinBox{Border: 0.5px solid rgb(220,220,220);}")
                #>
                self.wareTableItemData.blockSignals(True)
                self.wareTableItemData.item(row,4).setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable)
                self.wareTableItemData.item(row,5).setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable)
                for i in range(self.wareTableItemData.rowCount()):
                    if i != row and self.wareTableItemData.cellWidget(i, 0).isChecked():
                        self.wareTableItemData.item(row,5).setText(self.wareTableItemData.item(i, 5).text())
                        break
                self.wareTableItemData.blockSignals(False)
                #>
                self.wareTableItemData.cellWidget(row, 6).setEnabled(True)
                self.wareTableItemData.cellWidget(row, 6).setStyleSheet("QSpinBox{Border: 0.5px solid rgb(220,220,220);}")

            if state == 0:
                self.wareTableItemData.cellWidget(row, 1).setChecked(False)
                self.wareTableItemData.cellWidget(row, 1).setEnabled(False)
                if(not(isVirtual)):
                    self.wareTableItemData.cellWidget(row, 2).clear()
                    self.wareTableItemData.cellWidget(row, 2).setEnabled(False)
                    self.wareTableItemData.cellWidget(row, 2).setStyleSheet("QLineEdit{Border: 0;}")
                    self.wareTableItemData.cellWidget(row, 3).setValue(0)
                    self.wareTableItemData.cellWidget(row, 3).setEnabled(False)
                    self.wareTableItemData.cellWidget(row, 3).setStyleSheet("QSpinBox{Border: 0;}")
                
                #>blocksignals
                self.wareTableItemData.blockSignals(True)
                item_1 = QtWidgets.QTableWidgetItem("")
                item_2 = QtWidgets.QTableWidgetItem("")
                item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|~QtCore.Qt.ItemIsEditable)
                item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|~QtCore.Qt.ItemIsEditable)
                self.wareTableItemData.setItem(row, 4, item_1)
                self.wareTableItemData.setItem(row, 5, item_2)
                self.wareTableItemData.blockSignals(False)
                #>
                self.wareTableItemData.cellWidget(row, 6).setValue(0)
                self.wareTableItemData.cellWidget(row, 6).setEnabled(False)
                self.wareTableItemData.cellWidget(row, 6).setStyleSheet("QSpinBox{Border: 0;}")

    def secondCheckBoxChanged(self, state: int = None, row: int = None, wareCode: str = None, qtyNewOld: tuple = None):
        #se verifica que los valores qty no sean None
        if qtyNewOld[0] is not None and qtyNewOld[1] is not None:
            #se verifica cantidades mayores a 0, tanto para si es para old o para new
            if (not self.wareTableItemData.cellWidget(row,1).isChecked()) and (qtyNewOld[0] > 0 or qtyNewOld[1] > 0):
                msg = QMessageBox.information(self, "Advertencia", "Cantidades existentes en almacen.\n>¡Reducir a 0 unidades¡", QMessageBox.Ok)
                self.wareTableItemData.cellWidget(row,1).setChecked(True)

    def locationLineEdit(self, row):
        txtEvaluated = self.wareTableItemData.cellWidget(row, 2).text().upper()
        if txtEvaluated != "":
            splitted = txtEvaluated.split(",")
            if len(splitted) == 2:
                stripSplitted = list(map(lambda x: x.strip(), splitted))
                mueble = stripSplitted[0].split(" ")
                fila = stripSplitted[1].split(" ")
                if mueble[0] == "MUEBLE" and fila[0] == "FILA" and len(mueble) > 1 and len(fila) > 1:
                    pass
                else:
                    QMessageBox.information(self, "Alerta", "¡Seguir el formato correcto!\n>MUEBLE (A->Z), FILA (1->100)", buttons= QMessageBox.Ok)
                    self.wareTableItemData.cellWidget(row,2).clear()
            else:
                QMessageBox.information(self, "Alerta", "¡Seguir el formato correcto!\n>MUEBLE (A->Z), FILA (1->100)", buttons= QMessageBox.Ok)
                self.wareTableItemData.cellWidget(row,2).clear()
    
    def itemContentChanged(self, itemCurrent):
        row = itemCurrent.row()
        column = itemCurrent.column()

        if column == 5 or column == 4:
            try:
                currentItem = self.wareTableItemData.item(row, column).text()
                if currentItem != "":
                    str2float = float(self.wareTableItemData.item(row, column).text())
                    pvpNewOld = math.floor(str2float*10)/10.0
                    if pvpNewOld > 9999.9: pvpNewOld = 9999.9
                    #>
                    self.wareTableItemData.blockSignals(True)
                    if column == 5:
                        for i in range(self.wareTableItemData.rowCount()):
                            if self.wareTableItemData.cellWidget(i, 0).isChecked():
                                self.wareTableItemData.item(i, column).setText(str(pvpNewOld))
                        self.saveCurrentItemSelection()
                    elif column == 4:
                        self.wareTableItemData.item(row, column).setText(str(pvpNewOld))
                    self.wareTableItemData.blockSignals(False)
                    #>
                elif currentItem == "":
                    self.wareTableItemData.blockSignals(True)
                    if column == 5:
                        for i in range(self.wareTableItemData.rowCount()):
                            if self.wareTableItemData.cellWidget(i, 0).isChecked():
                                self.wareTableItemData.item(i, column).setText("")
                    elif column == 4:
                        self.wareTableItemData.item(row, column).setText("")
                    self.wareTableItemData.blockSignals(False)

            except Exception as error:
                # print("An Exception occurred:,", error)
                self.wareTableItemData.blockSignals(True)
                if column == 5:
                    for i in range(self.wareTableItemData.rowCount()):
                        if self.wareTableItemData.cellWidget(i, 0).isChecked():
                            self.wareTableItemData.item(i, column).setText(self.PrevItemPvpOld)
                elif column == 4:
                    self.wareTableItemData.item(row, column).setText(self.PrevItemPvpNew)
                self.wareTableItemData.blockSignals(False)

    #almacena texto de item actual seleccionado
    def saveCurrentItemSelection(self):
        if self.wareTableItemData.selectedItems():
            self.PrevItemPvpNew = self.wareTableItemData.selectedItems()[0].text()
            self.PrevItemPvpOld = self.wareTableItemData.selectedItems()[1].text()

    def first_callback(self, row, isVirtual):
        return lambda x: self.firstCheckBoxChanged(x, row, isVirtual)

    def second_callback(self, row: int = None, wareCode: str = None, qtyNewOld: tuple = None):
        return lambda x: self.secondCheckBoxChanged(state=x, row=row, wareCode=wareCode, qtyNewOld=qtyNewOld)

    def locationLineEditCallBack(self, row):
        return lambda : self.locationLineEdit(row)
    
    def submitclose(self):
        self.accept()

    def txtEditSignal(self):
        cursor = self.contentTxtEdit.textCursor()
        length_ = len(self.contentTxtEdit.toPlainText())
        # print("initial cursor position: " + str(cursor.position()))
        # print("initial length: " + str(length_))
        if length_ < 601:
            self.prevcurrentPlainText_ = self.contentTxtEdit.toPlainText()
            positionCursor = cursor.position()
            self.contentTxtEdit.blockSignals(True)
            self.contentTxtEdit.setText(self.prevcurrentPlainText_)
            cursor = self.contentTxtEdit.textCursor()
            cursor.setPosition(positionCursor)
            self.contentTxtEdit.setTextCursor(cursor)
            self.contentTxtEdit.blockSignals(False)

            self.lblCaracterCount.setText("CHARACTERS: %d" % len(self.prevcurrentPlainText_))
            self.lblCaracterCount.adjustSize()

        elif length_ >= 601 and cursor.position() >= 600:
            positionCursor = cursor.position()
            self.contentTxtEdit.blockSignals(True)
            # self.contentTxtEdit.setText(self.prevcurrentPlainText_)
            self.contentTxtEdit.setText(self.contentTxtEdit.toPlainText()[:600])
            cursor = self.contentTxtEdit.textCursor()
            cursor.setPosition(positionCursor - 1) if positionCursor < 600 else cursor.setPosition(600)
            self.contentTxtEdit.setTextCursor(cursor)
            self.contentTxtEdit.blockSignals(False)
            self.lblCaracterCount.setText("CHARACTERS: %d" % len(self.contentTxtEdit.toPlainText()[:600]))
            self.lblCaracterCount.adjustSize()
            self.prevcurrentPlainText_ = self.contentTxtEdit.toPlainText()[:600]

        elif length_ >= 601 and cursor.position() < 600:
            positionCursor = cursor.position()
            if hasattr(self,'prevcurrentPlainText_'):
                self.contentTxtEdit.blockSignals(True)
                self.contentTxtEdit.setText(self.prevcurrentPlainText_)
                cursor = self.contentTxtEdit.textCursor()
                cursor.setPosition(positionCursor - 1)
                self.contentTxtEdit.setTextCursor(cursor)
                self.contentTxtEdit.blockSignals(False)
            else:
                self.contentTxtEdit.blockSignals(True)
                self.contentTxtEdit.setText(self.contentTxtEdit.toPlainText()[:600])
                self.contentTxtEdit.blockSignals(False)
                self.lblCaracterCount.setText("CHARACTERS: %d" % 600)
                self.lblCaracterCount.adjustSize()

            # cursor = self.contentTxtEdit.textCursor()
            # cursor.movePosition(11)
            # self.contentTxtEdit.setTextCursor(cursor)
        #se puede guardar la position antigua de cursor y asignar a la nueva cuando el cursor esta menos de 600
        #cantidad de caracteres igual a 600 o 601

    def setupSecondItemData(self):
        x_offset = -35
        y_offset = 20
        
        # WARNING MESSAGE OF DATEOUT
        msgwrn = ">DEJAR EN 1752 SI NO DESEA AGREGAR FECHA DE PUBLICACIÓN"
        self.lblWarning_ = QLabel(msgwrn, self.tab_compItemData)
        self.lblWarning_.setGeometry(155 + x_offset, -10 + y_offset, 240,25)
        self.lblWarning_.setWordWrap(True)
        font = self.lblWarning_.font()
        font.setBold(True)
        font.setPointSize(7)
        self.lblWarning_.setFont(font)
        self.lblWarning_.setStyleSheet("QLabel{background-color: red; color:white}")

        # DATEOUT PART
        self.lblDateOut = QLabel("PUBLICACIÓN (AÑO): ",self.tab_compItemData)
        self.lblDateOut.adjustSize()
        self.lblDateOut.move(x_offset + 43, y_offset + 20)
        self.lblDateOut.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblDateOut.setStyleSheet("background-color: lightblue")
        

        # self.dateOutWidget = QDateEdit(QDate.currentDate(),self.tab_compItemData)
        self.dateOutWidget = MyDateEdit(self.tab_compItemData)
        self.dateOutWidget.setMaximumDate(QDate.currentDate().addYears(1))
        self.dateOutWidget.setMinimumDate(QDate(1752,1,1))
        self.dateOutWidget.setDate(QDate(-2,1,1))
        self.dateOutWidget.move(x_offset + 155, y_offset + 16)
        self.dateOutWidget.setDisplayFormat("yyyy")
        self.dateOutWidget.setFixedWidth(240)
        font = self.dateOutWidget.font()
        font.setBold(True)
        self.dateOutWidget.setFont(font)
        self.dateOutWidget.dateChanged.connect(lambda x: self.dateOutWidget.setStyleSheet("QDateEdit{background-color: red; color:white}") if x.year() == 1752 else self.dateOutWidget.setStyleSheet("QDateEdit{background-color: white; color:default}"))
        self.dateOutWidget.clicked.connect(lambda: self.deactivateLineEdit("DateOut"))
        #aqui falta el activador del qdateedit
        
        #EDITION
        self.lblEdition = QLabel("N. EDICIÓN: ",self.tab_compItemData)
        self.lblEdition.adjustSize()
        self.lblEdition.move(x_offset + 86, y_offset + 40)
        self.lblEdition.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblEdition.setStyleSheet("background-color: lightblue")
        self.editionSpinBox = MySpinBox(self.tab_compItemData, minimum=0, maximum=99, value=0)
        self.editionSpinBox.move(x_offset + 155, y_offset + 37)
        self.editionSpinBox.setFixedWidth(240)
        self.editionSpinBox.clicked.connect(lambda: self.deactivateLineEdit("Edition"))
        
        #PAGES PART
        self.lblPages = QLabel("N. PÁGINAS: ",self.tab_compItemData)
        self.lblPages.adjustSize()
        self.lblPages.move(x_offset + 86, y_offset + 63)
        self.lblPages.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblPages.setStyleSheet("background-color: lightblue")
        self.pagesSpinBox = MySpinBox(self.tab_compItemData, minimum=0, maximum=9999, value=0)
        self.pagesSpinBox.move(x_offset + 155, y_offset + 60)
        self.pagesSpinBox.setFixedWidth(240)
        self.pagesSpinBox.clicked.connect(lambda: self.deactivateLineEdit("Pages"))

        # IDIOM PART
        self.lblIdiom = QLabel("IDIOMA: ",self.tab_compItemData)
        self.lblIdiom.adjustSize()
        self.lblIdiom.move(x_offset + 106, y_offset + 87)
        self.lblIdiom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblIdiom.setStyleSheet("background-color: lightblue")
        self.cmbIdiom = MyComboBox_Pop(self.tab_compItemData)
        self.cmbIdiom.move(x_offset + 155, y_offset + 83)
        self.cmbIdiom.setFixedWidth(240)
        self.cmbIdiom.popupAboutToBeShown.connect(lambda: self.deactivateLineEdit("CmbIdiom"))

        # COVER PART
        self.lblCover = QLabel("CUBIERTA: ",self.tab_compItemData)
        self.lblCover.adjustSize()
        self.lblCover.move(x_offset + 94, y_offset + 109)
        self.lblCover.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblCover.setStyleSheet("background-color: lightblue")
        self.cmbCover = MyComboBox_Pop(self.tab_compItemData)
        self.cmbCover.setFixedWidth(240)
        self.cmbCover.popupAboutToBeShown.connect(lambda: self.deactivateLineEdit("CmbCover"))
        self.cmbCover.move(x_offset + 155, y_offset + 105)
        self.cmbCover.addItems(["BLANDA", "DURA"])

        # DIMENTIONS PART
        self.lblWidth = QLabel("ANCHO:", self.tab_compItemData)
        self.lblWidth.move(x_offset + 111, y_offset + 132)
        self.lblWidth.setStyleSheet("background-color: lightblue")
        self.widthSpinBox = MySpinBox(self.tab_compItemData, minimum=0, maximum=100, value=0, suffix=' cm')
        self.widthSpinBox.clicked.connect(lambda: self.deactivateLineEdit("Width"))
        self.widthSpinBox.move(x_offset + 155, y_offset + 128)
        self.widthSpinBox.setFixedWidth(99)

        self.lblHeight = QLabel("ALTO:", self.tab_compItemData)
        self.lblHeight.move(x_offset + 262, y_offset + 132)
        self.lblHeight.setStyleSheet("background-color: lightblue")
        self.heightSpinBox = MySpinBox(self.tab_compItemData, minimum=0, maximum=100, value=0, suffix=' cm')
        self.heightSpinBox.clicked.connect(lambda: self.deactivateLineEdit("Height"))
        self.heightSpinBox.move(x_offset + 296, y_offset + 128)
        self.heightSpinBox.setFixedWidth(99)
        
        # CATEGORY PART
        self.lblCategory = QLabel("CATEGORÍA:", self.tab_compItemData)
        self.lblCategory.move(x_offset + 38, y_offset + 155)
        self.lblCategory.setStyleSheet("background-color: lightblue")
        self.cmbCategory1 = MyComboBox_Pop(self.tab_compItemData)
        self.cmbCategory1.setFixedWidth(95)
        self.cmbCategory1.setFixedHeight(20)
        self.cmbCategory1.move(x_offset + 104, y_offset + 151)
        # self.cmbCategory1.setModel(QStringListModel([">SUPERACION PERSONAL", ">GASTRONOMIA", ">EDUCACION", ">LITERATURA"]))
        font = self.cmbCategory1.font()
        font.setPointSize(7)
        self.cmbCategory1.setFont(font)
        listView = QListView()
        listView.setWordWrap(True)
        self.cmbCategory1.setView(listView)
        # self.cmbCategory1.setEditable(True)
        # self.cmbCategory1.setCurrentIndex(-1)
        # self.cmbCategory1.lineEdit().setPlaceholderText("NIVEL 1")
        self.cmbCategory1.currentIndexChanged.connect(lambda x: self.cmbCategory1.setEditable(False))
        self.cmbCategory1.popupAboutToBeShown.connect(lambda: self.deactivateLineEdit("Category1"))
        self.cmbCategory1.setEnabled(False)

        self.cmbCategory2 = MyComboBox_Pop(self.tab_compItemData)
        self.cmbCategory2.setFixedWidth(95)
        self.cmbCategory2.setFixedHeight(20)
        self.cmbCategory2.move(x_offset + 202, y_offset + 151)
        # self.cmbCategory2.setModel(QStringListModel([">SUPERACION PERSONAL", ">GASTRONOMIA", ">EDUCACION", ">LITERATURA"]))
        font = self.cmbCategory2.font()
        font.setPointSize(7)
        self.cmbCategory2.setFont(font)
        listView = QListView()
        listView.setWordWrap(True)
        self.cmbCategory2.setView(listView)
        self.cmbCategory2.setEditable(True)
        # self.cmbCategory2.setCurrentIndex(-1)
        # self.cmbCategory2.lineEdit().setPlaceholderText("NIVEL 2")
        self.cmbCategory2.currentIndexChanged.connect(lambda x: self.cmbCategory2.setEditable(False))
        self.cmbCategory2.popupAboutToBeShown.connect(lambda: self.deactivateLineEdit("Category2"))
        self.cmbCategory2.setEnabled(False)

        self.cmbCategory3 = MyComboBox_Pop(self.tab_compItemData)
        self.cmbCategory3.setFixedWidth(95)
        self.cmbCategory3.setFixedHeight(20)
        self.cmbCategory3.move(x_offset + 300, y_offset + 151)
        # self.cmbCategory3.setModel(QStringListModel([">SUPERACION PERSONAL", ">GASTRONOMIA", ">EDUCACION", ">LITERATURA"]))
        font = self.cmbCategory3.font()
        font.setPointSize(7)
        self.cmbCategory3.setFont(font)
        listView = QListView()
        listView.setWordWrap(True)
        self.cmbCategory3.setView(listView)
        self.cmbCategory3.setEditable(True)
        # self.cmbCategory3.setCurrentIndex(-1)
        # self.cmbCategory3.lineEdit().setPlaceholderText("NIVEL 3")
        self.cmbCategory3.currentIndexChanged.connect(lambda x: self.cmbCategory3.setEditable(False))
        self.cmbCategory3.popupAboutToBeShown.connect(lambda: self.deactivateLineEdit("Category3"))
        self.cmbCategory3.setEnabled(False)

        # CONTENT PART
        self.lblContent = QLabel("RESUMEN:", self.tab_compItemData)
        self.lblContent.move(x_offset + 50, y_offset + 180)
        self.lblContent.setStyleSheet("background-color: lightblue")
        self.contentTxtEdit = MyQTextEdit(self.tab_compItemData)
        self.contentTxtEdit.move(x_offset + 105, y_offset + 180)
        self.contentTxtEdit.setFixedSize(290,65)
        self.contentTxtEdit.setAcceptRichText(False)
        self.contentTxtEdit.setTabChangesFocus(True)
        font = self.contentTxtEdit.font()
        font.setPointSize(8)
        self.contentTxtEdit.setFont(font)
        self.contentTxtEdit.textChanged.connect(self.txtEditSignal)
        self.contentTxtEdit.clicked.connect(lambda: self.deactivateLineEdit("TextEdit"))

        # LABEL CARACTER
        self.lblCaracterCount = QLabel("CHARACTERS: 0", self.tab_compItemData)
        # self.lblCaracterCount.setFixedWidth(82)
        self.lblCaracterCount.move(x_offset + 105, y_offset + 245)
        self.lblCaracterCount.setStyleSheet("QLabel{background-color: lightgreen;}")

        # LABEL MAX CARACTER
        self.lblMaxCarecter = QLabel("MAX: 600 CHAR", self.tab_compItemData)
        self.lblMaxCarecter.move(x_offset + 205, y_offset + 245)
        self.lblMaxCarecter.setStyleSheet("QLabel{background-color: red; color: white;}")
        font = QFont()
        font.setBold(True)
        self.lblMaxCarecter.setFont(font)

    def setupWareItemData(self):
        x_offset = 10
        y_offset = 10
        flag1 = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable

         # -----------  wareTableItemData configuration  -----------
        self.wareTableItemData = QtWidgets.QTableWidget(self.tab_wareItemData)
        # self.wareTableItemData.setEditTriggers(QtWidgets.QTreeView.NoEditTriggers)
        self.wareTableItemData.setGeometry(QtCore.QRect(x_offset, y_offset, 355, 270))
        self.wareTableItemData.setMinimumHeight(100) ## esto se agrego
        self.wareTableItemData.setObjectName("wareTableItemData")

        self.wareTableItemData.setColumnCount(7)
        self.wareTableItemData.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem())
        self.wareTableItemData.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem())
        self.wareTableItemData.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem())
        self.wareTableItemData.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem())
        self.wareTableItemData.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem())
        self.wareTableItemData.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem())
        self.wareTableItemData.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem())
        
        self.wareTableItemData.setColumnWidth(0,49)
        self.wareTableItemData.setColumnWidth(1,50)
        self.wareTableItemData.setColumnWidth(2,107)
        self.wareTableItemData.setColumnWidth(3,59)
        self.wareTableItemData.setColumnWidth(4,58)
        self.wareTableItemData.setColumnWidth(5,58)
        self.wareTableItemData.setColumnWidth(6,43)

        self.wareTableItemData.horizontalHeader().setEnabled(False)
        self.wareTableItemData.verticalHeader().setEnabled(False)
        self.wareTableItemData.setSelectionBehavior(1)
        self.wareTableItemData.setSelectionMode(1)
        self.wareTableItemData.setStyleSheet("selection-background-color: rgb(0, 120, 255);selection-color: rgb(255, 255, 255);")
        self.wareTableItemData.itemChanged.connect(self.itemContentChanged)
        self.wareTableItemData.itemSelectionChanged.connect(self.saveCurrentItemSelection)
        # self.wareTableItemData.viewport().installEventFilter(self)
        # self.wareTableItemData.keyPressEvent = self.KeyPressed
        # self.wareTableItemData.doubleClicked.connect(self.tableWidget_doubleClicked)

        self.wareTableItemData.setHorizontalHeaderItem(0, QTableWidgetItem("¿Existe?"))
        self.wareTableItemData.setHorizontalHeaderItem(1, QTableWidgetItem("¿Activo?"))
        self.wareTableItemData.setHorizontalHeaderItem(2, QTableWidgetItem("Ubicación"))
        self.wareTableItemData.setHorizontalHeaderItem(3, QTableWidgetItem("Stock Min."))
        self.wareTableItemData.setHorizontalHeaderItem(4, QTableWidgetItem("PVP 1°"))
        self.wareTableItemData.setHorizontalHeaderItem(5, QTableWidgetItem("PVP 2°"))
        self.wareTableItemData.setHorizontalHeaderItem(6, QTableWidgetItem("DSCT."))

        verticalHeader_ = self.wareTableItemData.verticalHeader()
        verticalHeader_.setSectionResizeMode(QHeaderView.ResizeToContents)
        verticalHeader_.setFont(QFont("Times", 7, QFont.Bold))

        horizontalHeader_ = self.wareTableItemData.horizontalHeader()
        horizontalHeader_.setFrameStyle(QFrame.Box | QFrame.Plain)
        horizontalHeader_.setLineWidth(1)
        horizontalHeader_.setFont(QFont("Times", 7, QFont.Bold))

        font = self.wareTableItemData.font()
        font.setPointSize(8)
        self.wareTableItemData.setFont(font)
        
        tmp = PrefixDelegate()
        tmp.setSuffix(" %")
        tmp.setPrefix("S/. ")
        self.wareTableItemData.setItemDelegateForColumn(4,tmp)
        self.wareTableItemData.setItemDelegateForColumn(5,tmp)

        # -----------  user validation  -----------
    
    def userValidation(self):
        # isPressedOk: True or False
        # text: content
        text, isPressedOk = QInputDialog.getText(self, 'Validar usuario', 'Ingrese contraseña', QtWidgets.QLineEdit.Password)
        if(isPressedOk):
            with users_gestor() as a_:
                if a_.checkPSW(text)[0]:
                    # tmpData = a_.checkPSW(text)[1]
                    del a_ 
                    # return tmpData, "acepted"
                    return True, "acepted"
                elif not(a_.checkPSW(text)[0]):
                    del a_ 
                    return False, "denied"
        else:
            return False, "aborted"
    
    def setupUi(self):
        x_offset = 10
        y_offset = 10

        self.resize(340, 300)
        self.setFixedSize(400, 358)
        self.setObjectName("ui_EditNewItemDialog")
        self.setWindowTitle("Editar producto") if not(self.method) else self.setWindowTitle("Registrar nuevo producto")

        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

        self.tab_mainItemData = QWidget(self)
        self.tab_mainItemData.setFixedSize(360, 295)
        self.tab_mainItemData.move(0,0)
        self.tab_compItemData = QWidget(self)
        self.tab_compItemData.setFixedSize(370, 290)
        self.tab_compItemData.move(0,0)

        self.tab_wareItemData = QWidget(self)
        self.tab_wareItemData.setFixedSize(370, 290)
        self.tab_wareItemData.move(0,0)

        #create a tabWidget
        self.tabItem = QTabWidget(self)
        self.tabItem.addTab(self.tab_mainItemData, "Info. Principal")
        self.tabItem.addTab(self.tab_compItemData, "Info. Secundaria")
        self.tabItem.addTab(self.tab_wareItemData, "Info. Almacén")
        self.tabItem.currentChanged.connect(lambda x: self.cleanInputFields())

        self.btnSave = QPushButton("Guardar", self)
        self.btnSave.setAutoDefault(False)
        self.btnCancel = QPushButton("Cancelar", self)
        self.btnCancel.setAutoDefault(False)
        self.btnSave.clicked.connect(lambda: self.saveEvent(True))
        self.btnCancel.clicked.connect(lambda: self.close())

        self.main_layout.addWidget(self.tabItem, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.btnSave, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.btnCancel,2, 0, alignment=Qt.AlignmentFlag.AlignJustify)
        self.setupSecondItemData()
        self.setupWareItemData()

        warning_text = ">¡No ingresar tildes ni caracteres especiales (,', \", ´,)!"

        self.lblWarning = QLabel(warning_text,self.tab_mainItemData)
        self.lblWarning.adjustSize()
        self.lblWarning.move(55 + x_offset, 15 + y_offset) if not(self.method) else self.lblWarning.move(60 + x_offset, 5 + y_offset)
        self.lblWarning.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblWarning.setStyleSheet("background-color: red")

        self.lblWarning = QLabel(">(*): Campos obligatorios",self.tab_mainItemData) if self.method else False
        if bool(self.lblWarning):
            self.lblWarning.adjustSize()
            self.lblWarning.move(60 + x_offset, 20 + y_offset)
            self.lblWarning.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.lblWarning.setStyleSheet("background-color: red")

        self.lblId = QLabel("CÓDIGO:",self.tab_mainItemData) if not(self.method) else QLabel("CÓDIGO(*):",self.tab_mainItemData)
        self.lblId.adjustSize()
        self.lblId.move(43 + x_offset, 40 + y_offset) if not(self.method) else self.lblId.move(33 + x_offset, 40 + y_offset)
        self.lblId.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblId.setStyleSheet("background-color: lightgreen")
        self.txtId = MyLineEdit(self.tab_mainItemData)
        self.txtId.setFixedHeight(18)
        self.txtId.setFixedWidth(70)
        self.txtId.move(95 + x_offset, 37 + y_offset)
        self.txtId.setEnabled(False)
        self.defaultPalette = self.txtId.palette()  

        self.lblItem = QLabel("ITEM:",self.tab_mainItemData)
        self.lblItem.adjustSize()
        self.lblItem.move(175 + x_offset, 40 + y_offset) 
        self.lblItem.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblItem.setStyleSheet("background-color: lightgreen")

        self.cmbItem = MyComboBox_Pop(self.tab_mainItemData)
        self.cmbItem.setGeometry(210 + x_offset, 37 + y_offset, 115, 18)

        self.color = QColor(230,230,230)
        self.lblISBN = QLabel("ISBN:",self.tab_mainItemData)
        self.lblISBN.adjustSize()
        self.lblISBN.move(61 + x_offset, 60 + y_offset)
        self.lblISBN.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblISBN.setStyleSheet("background-color: lightblue")
        self.txtISBN = MyLineEdit(self.tab_mainItemData)
        self.txtISBN.setFixedHeight(18)
        self.txtISBN.setFixedWidth(230)
        self.txtISBN.move(95 + x_offset, 58 + y_offset)
        self.txtISBN.setReadOnly(True)
        palette = self.txtISBN.palette()
        palette.setColor(QtGui.QPalette.Base, self.color)
        self.txtISBN.setPalette(palette)
        self.txtISBN.clicked.connect(lambda: self.deactivateLineEdit("ISBN"))
        self.txtISBN.setMaxLength(15)

        self.lblTitle = QLabel("TÍTULO:",self.tab_mainItemData) if not(self.method) else QLabel("TÍTULO(*):",self.tab_mainItemData)
        self.lblTitle.adjustSize()
        self.lblTitle.move(48 + x_offset, 80 + y_offset) if not(self.method) else self.lblTitle.move(38 + x_offset, 80 + y_offset)
        self.lblTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblTitle.setStyleSheet("background-color: lightblue")
        self.txtTitle = MyLineEdit(self.tab_mainItemData)
        self.txtTitle.setFixedHeight(18)
        self.txtTitle.setFixedWidth(230)
        self.txtTitle.move(95 + x_offset, 78 + y_offset)
        self.txtTitle.setReadOnly(True)
        palette = self.txtTitle.palette()
        palette.setColor(QtGui.QPalette.Base, self.color)
        self.darkPalette = palette
        self.txtTitle.setPalette(self.darkPalette)
        self.txtTitle.clicked.connect(lambda: self.deactivateLineEdit("Title"))
        self.txtTitle.setMaxLength(90)

        self.lblAutor = QLabel("AUTOR:",self.tab_mainItemData) if not(self.method) else QLabel("AUTOR(*):",self.tab_mainItemData)
        self.lblAutor.adjustSize()
        self.lblAutor.move(49 + x_offset, 100 + y_offset) if not(self.method) else self.lblAutor.move(39 + x_offset, 100 + y_offset)
        self.lblAutor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblAutor.setStyleSheet("background-color: lightblue")
        self.txtAutor = MyLineEdit(self.tab_mainItemData)
        self.txtAutor.setFixedHeight(18)
        self.txtAutor.setFixedWidth(230)
        self.txtAutor.move(95 + x_offset, 98 + y_offset)
        self.txtAutor.setReadOnly(True)
        self.txtAutor.setPalette(self.darkPalette)
        self.txtAutor.clicked.connect(lambda: self.deactivateLineEdit("Autor"))
        self.txtAutor.setMaxLength(45)

        self.lblPublisher = QLabel("EDITORIAL:",self.tab_mainItemData) if not(self.method) else QLabel("EDITORIAL(*):",self.tab_mainItemData)
        self.lblPublisher.adjustSize()
        self.lblPublisher.move(31 + x_offset, 120 + y_offset) if not(self.method) else self.lblPublisher.move(21 + x_offset, 120 + y_offset)
        self.lblPublisher.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lblPublisher.setStyleSheet("background-color: lightblue")
        self.txtPublisher = MyLineEdit(self.tab_mainItemData)
        self.txtPublisher.setFixedHeight(18)
        self.txtPublisher.setFixedWidth(230)
        self.txtPublisher.move(95 + x_offset, 118 + y_offset)
        self.txtPublisher.setReadOnly(True)
        self.txtPublisher.setPalette(self.darkPalette)
        self.txtPublisher.clicked.connect(lambda: self.deactivateLineEdit("Publisher"))
        self.txtPublisher.setMaxLength(45)

        # self.lblPrice = QLabel("PRECIO:",self.tab_mainItemData) if not(self.method) else QLabel("PRECIO(*):",self.tab_mainItemData)
        # self.lblPrice.adjustSize()
        # self.lblPrice.move(47 + x_offset, 140 + y_offset) if not(self.method) else self.lblPrice.move(37 + x_offset, 140 + y_offset)
        # self.lblPrice.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.lblPrice.setStyleSheet("background-color: lightblue")
        # self.txtPrice = MyLineEdit(self.tab_mainItemData)
        # self.txtPrice.setPlaceholderText("Ingresar solo numeros")
        # self.txtPrice.setFixedHeight(18)
        # self.txtPrice.setFixedWidth(230)
        # self.txtPrice.move(95 + x_offset, 138 + y_offset)
        # self.txtPrice.setReadOnly(True)
        # self.txtPrice.setPalette(self.darkPalette)
        # self.txtPrice.clicked.connect(lambda: self.deactivateLineEdit("Price"))
        # self.txtPrice.setMaxLength(30)

        # self.spinInitStock = MySpinBox(self.tab_mainItemData)
        # self.spinInitStock.setGeometry(100 + x_offset, 100 + y_offset, 50, 20)
        # self.spinInitStock.move(95 + x_offset, 237 + y_offset)
        # self.spinInitStock.setReadOnly(True)
        # self.spinInitStock.setPalette(self.darkPalette)
        # self.spinInitStock.setEnabled(False) if not(self.method) else self.spinInitStock.setEnabled(True)
        # # self.spinInitStock.clicked.connect(lambda: self.deactivateLineEdit("Stock"))
        # self.spinInitStock.setEnabled(False)

        # LABEL BOTTOM IMAGE
        self.lblImage_ = QLabel(self.tab_mainItemData)
        self.lblImage_.setGeometry(QtCore.QRect(95 + x_offset, 150 + y_offset, 200, 105))
        self.lblImage_.setText("")
        # self.lblImage_.setStyleSheet("QLabel{background-color: red;}")
        pixMap = QtGui.QPixmap("C:/Users/IROJAS/Desktop/Genesis/genesis-system-admin/imgs/newBook.png")
        # pixMap = pixMap.scaled(600, 600, QtCore.Qt.IgnoreAspectRatio)
        self.lblImage_.setPixmap(pixMap)
        self.lblImage_.setScaledContents(True)

        # self.btnCancel = QPushButton('Cancelar', self)
        # self.btnCancel.adjustSize()
        # self.btnCancel.move(190, 185)
        # self.btnCancel.clicked.connect(lambda: self.submitclose())

        # self.btnOk = QPushButton(self)
        # self.btnOk.setText("Editar") if not(self.method) else self.btnOk.setText("Registrar")
        # self.btnOk.adjustSize()
        # self.btnOk.move(80, 185)
        # self.btnOk.clicked.connect(lambda: self.saveEvent(True))

    def deactivateLineEdit(self, widget: str = ""):
        if bool(widget):
            if widget == "ISBN":
                self.txtISBN.setReadOnly(False)
                self.txtISBN.setPalette(self.defaultPalette)

                #palette_
                # self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                # self.pagesSpinBox.setPalette(self.darkPalette)
                # self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.widthSpinBox.setPalette(self.darkPalette)
                # self.heightSpinBox.setPalette(self.darkPalette)
                # self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.contentTxtEdit.setPalette(self.darkPalette)

                self.txtTitle.setPalette(self.darkPalette)
                self.txtAutor.setPalette(self.darkPalette)
                self.txtPublisher.setPalette(self.darkPalette)
                # self.spinInitStock.setPalette(self.darkPalette)

                #readonly_
                # self.dateOutWidget.setReadOnly(True)
                # self.pagesSpinBox.setReadOnly(True)
                # self.widthSpinBox.setReadOnly(True)
                # self.cmbIdiom.readonly = True
                # self.cmbCover.readonly = True
                # self.heightSpinBox.setReadOnly(True)
                # self.cmbCategory1.readonly = True
                # self.cmbCategory2.readonly = True
                # self.cmbCategory3.readonly = True
                # self.contentTxtEdit.setReadOnly(True)
                self.txtTitle.setReadOnly(True)
                self.txtAutor.setReadOnly(True)
                self.txtPublisher.setReadOnly(True)
                # self.spinInitStock.setReadOnly(True)

            elif widget == "Title":
                self.txtTitle.setReadOnly(False)
                self.txtTitle.setPalette(self.defaultPalette)

                #palette_
                # self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                # self.pagesSpinBox.setPalette(self.darkPalette)
                # self.widthSpinBox.setPalette(self.darkPalette)
                # self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.heightSpinBox.setPalette(self.darkPalette)
                # self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.contentTxtEdit.setPalette(self.darkPalette)
                self.txtISBN.setPalette(self.darkPalette)
                self.txtAutor.setPalette(self.darkPalette)
                self.txtPublisher.setPalette(self.darkPalette)
                # self.spinInitStock.setPalette(self.darkPalette)

                #readonly_
                # self.dateOutWidget.setReadOnly(True)
                # self.pagesSpinBox.setReadOnly(True)
                # self.widthSpinBox.setReadOnly(True)
                # self.cmbIdiom.readonly = True
                # self.cmbCover.readonly = True
                # self.heightSpinBox.setReadOnly(True)
                # self.cmbCategory1.readonly = True
                # self.cmbCategory2.readonly = True
                # self.cmbCategory3.readonly = True
                # self.contentTxtEdit.setReadOnly(True)
                self.txtISBN.setReadOnly(True)
                self.txtAutor.setReadOnly(True)
                self.txtPublisher.setReadOnly(True)
                # self.spinInitStock.setReadOnly(True)

            elif widget == "Autor":
                self.txtAutor.setReadOnly(False)
                self.txtAutor.setPalette(self.defaultPalette)

                #palette_
                # self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                # self.pagesSpinBox.setPalette(self.darkPalette)
                # self.widthSpinBox.setPalette(self.darkPalette)
                # self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.heightSpinBox.setPalette(self.darkPalette)
                # self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.contentTxtEdit.setPalette(self.darkPalette)
                self.txtISBN.setPalette(self.darkPalette)
                self.txtTitle.setPalette(self.darkPalette)
                self.txtPublisher.setPalette(self.darkPalette)
                # self.spinInitStock.setPalette(self.darkPalette)

                #readonly_
                # self.dateOutWidget.setReadOnly(True)
                # self.pagesSpinBox.setReadOnly(True)
                # self.widthSpinBox.setReadOnly(True)
                # self.cmbIdiom.readonly = True
                # self.cmbCover.readonly = True
                # self.heightSpinBox.setReadOnly(True)
                # self.cmbCategory1.readonly = True
                # self.cmbCategory2.readonly = True
                # self.cmbCategory3.readonly = True
                # self.contentTxtEdit.setReadOnly(True)
                self.txtISBN.setReadOnly(True)
                self.txtTitle.setReadOnly(True)
                self.txtPublisher.setReadOnly(True)
                # self.spinInitStock.setReadOnly(True)

            elif widget == "Publisher":
                self.txtPublisher.setReadOnly(False)
                self.txtPublisher.setPalette(self.defaultPalette)

                #palette_
                # self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                # self.pagesSpinBox.setPalette(self.darkPalette)
                # self.widthSpinBox.setPalette(self.darkPalette)
                # self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.heightSpinBox.setPalette(self.darkPalette)
                # self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.contentTxtEdit.setPalette(self.darkPalette)
                self.txtISBN.setPalette(self.darkPalette)
                self.txtTitle.setPalette(self.darkPalette)
                self.txtAutor.setPalette(self.darkPalette)
                # self.spinInitStock.setPalette(self.darkPalette)
                

                #readonly_
                # self.dateOutWidget.setReadOnly(True)
                # self.pagesSpinBox.setReadOnly(True)
                # self.widthSpinBox.setReadOnly(True)
                # self.cmbIdiom.readonly = True
                # self.cmbCover.readonly = True
                # self.heightSpinBox.setReadOnly(True)
                # self.cmbCategory1.readonly = True
                # self.cmbCategory2.readonly = True
                # self.cmbCategory3.readonly = True
                # self.contentTxtEdit.setReadOnly(True)
                self.txtISBN.setReadOnly(True)
                self.txtTitle.setReadOnly(True)
                self.txtAutor.setReadOnly(True)
                # self.spinInitStock.setReadOnly(True)

            elif widget == "Stock":
                # self.spinInitStock.setReadOnly(False)
                # self.spinInitStock.setPalette(self.defaultPalette)

                #palette_
                # self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                # self.pagesSpinBox.setPalette(self.darkPalette)
                # self.widthSpinBox.setPalette(self.darkPalette)
                # self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.heightSpinBox.setPalette(self.darkPalette)
                # self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtPrice.setPalette(self.darkPalette)
                self.txtISBN.setPalette(self.darkPalette)
                self.txtTitle.setPalette(self.darkPalette)
                self.txtAutor.setPalette(self.darkPalette)
                self.txtPublisher.setPalette(self.darkPalette)

                #readonly_
                # self.dateOutWidget.setReadOnly(True)
                # self.pagesSpinBox.setReadOnly(True)
                # self.widthSpinBox.setReadOnly(True)
                # self.cmbIdiom.readonly = True
                # self.cmbCover.readonly = True
                # self.heightSpinBox.setReadOnly(True)
                # self.cmbCategory1.readonly = True
                # self.cmbCategory2.readonly = True
                # self.cmbCategory3.readonly = True
                # self.contentTxtEdit.setReadOnly(True)
                self.txtISBN.setReadOnly(True)
                self.txtTitle.setReadOnly(True)
                self.txtAutor.setReadOnly(True)
                self.txtPublisher.setReadOnly(True)

            elif widget == "DateOut":
                self.dateOutWidget.setReadOnly(False)
                self.dateOutWidget.setPalette(self.defaultPalette)
                #style
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.editionSpinBox.setPalette(self.darkPalette)
                self.widthSpinBox.setPalette(self.darkPalette)
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)

                #readonly
                
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.widthSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)

            elif widget == "Edition":
                self.editionSpinBox.setReadOnly(False)
                self.editionSpinBox.setPalette(self.defaultPalette)
                #style
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.widthSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)

                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.widthSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)

            elif widget == "Pages":
                self.pagesSpinBox.setReadOnly(False)
                self.pagesSpinBox.setPalette(self.defaultPalette)
                #style
                self.editionSpinBox.setPalette(self.darkPalette)
                self.widthSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)

                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.widthSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)

            elif widget == "CmbIdiom":
                self.cmbIdiom.readonly = False
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: white;}")

                #style
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.editionSpinBox.setPalette(self.darkPalette)
                self.widthSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)
                
                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.widthSpinBox.setReadOnly(True)
                self.cmbCover.readonly = True
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)
                
            
            elif widget == "CmbCover":
                self.cmbCover.readonly = False
                self.cmbCover.setStyleSheet("QComboBox{background-color: white;}")
                
                #style
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.editionSpinBox.setPalette(self.darkPalette)
                self.widthSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230, 230, 230);}")
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)
                
                #readonly                
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.widthSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)
            
            elif widget == "Width":
                self.widthSpinBox.setReadOnly(False)
                self.widthSpinBox.setPalette(self.defaultPalette)

                #style
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.editionSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)

                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)


            elif widget == "Height":
                self.heightSpinBox.setReadOnly(False)
                self.heightSpinBox.setPalette(self.defaultPalette)

                #style
                self.editionSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.widthSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)

                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.widthSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)

            elif widget == "Category1":
                self.cmbCategory1.readonly = False
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: white;}")

                #style
                self.editionSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.widthSpinBox.setPalette(self.darkPalette)
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)

                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.widthSpinBox.setReadOnly(True)
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)
            
            elif widget == "Category2":
                self.cmbCategory2.readonly = False
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: white;}")

                #style
                self.editionSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.widthSpinBox.setPalette(self.darkPalette)
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)

                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.widthSpinBox.setReadOnly(True)
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory3.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)
            
            elif widget == "Category3":
                self.cmbCategory3.readonly = False
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: white;}")

                #style
                self.editionSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.widthSpinBox.setPalette(self.darkPalette)
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.contentTxtEdit.setPalette(self.darkPalette)
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)

                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.widthSpinBox.setReadOnly(True)
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.contentTxtEdit.setReadOnly(True)
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)

            elif widget == "TextEdit":
                self.contentTxtEdit.setReadOnly(False)
                self.contentTxtEdit.setPalette(self.defaultPalette)

                # style
                self.editionSpinBox.setPalette(self.darkPalette)
                self.dateOutWidget.setStyleSheet("QDateEdit{background-color: rgb(230,230,230);}")
                self.pagesSpinBox.setPalette(self.darkPalette)
                self.cmbIdiom.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCover.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.widthSpinBox.setPalette(self.darkPalette)
                self.heightSpinBox.setPalette(self.darkPalette)
                self.cmbCategory1.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory2.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                self.cmbCategory3.setStyleSheet("QComboBox{background-color: rgb(230,230,230);}")
                # self.txtISBN.setPalette(self.darkPalette)
                # self.txtTitle.setPalette(self.darkPalette)
                # self.txtAutor.setPalette(self.darkPalette)
                # # self.txtPrice.setPalette(self.darkPalette)
                # # self.spinInitStock.setPalette(self.darkPalette)
                # self.txtPublisher.setPalette(self.darkPalette)

                #readonly
                self.dateOutWidget.setReadOnly(True)
                self.pagesSpinBox.setReadOnly(True)
                self.editionSpinBox.setReadOnly(True)
                self.cmbIdiom.readonly = True
                self.cmbCover.readonly = True
                self.widthSpinBox.setReadOnly(True)
                self.heightSpinBox.setReadOnly(True)
                self.cmbCategory1.readonly = True
                self.cmbCategory2.readonly = True
                self.cmbCategory3.readonly = True
                # self.txtISBN.setReadOnly(True)
                # self.txtTitle.setReadOnly(True)
                # self.txtAutor.setReadOnly(True)
                # # self.txtPrice.setReadOnly(True)
                # # self.spinInitStock.setReadOnly(True)
                # self.txtPublisher.setReadOnly(True)

    def show_window(self):
       self.show()

class MyDateEdit(QDateEdit):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QDateEdit.mousePressEvent(self, event)

class MySpinBox(QSpinBox):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QSpinBox.mousePressEvent(self, event)

class MyComboBox_Pop(QComboBox):
    popupAboutToBeShown  = QtCore.pyqtSignal()

    def __init__(self, parent) -> None:
        QComboBox.__init__(self, parent)
        self.readonly = False

    def showPopup(self) -> None:
        self.popupAboutToBeShown.emit()
        return super(MyComboBox_Pop, self).showPopup()
    
    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.readonly = False
        if not self.readonly:
            QComboBox.mousePressEvent(self, e)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if not self.readonly:
            QComboBox.keyPressEvent(self, e)
    
    def wheelEvent(self, e: QWheelEvent) -> None:
        if not self.readonly:
            QComboBox.wheelEvent(self,e)

class MyQTextEdit(QTextEdit):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QTextEdit.mousePressEvent(self, event)
        # self.textChanged.connect(self.text_changed)
    
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            return
        return super().keyPressEvent(e)
    
class PrefixDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.flag = True
        self.m_suffix = ""
        self.m_prefix = ""

    def displayText(self, value, locale):
        original_text = super().displayText(value, locale)
        return f"{self.m_prefix}{original_text}" if self.flag else f"{original_text}{self.m_suffix}"

    def setSuffix(self, val):
        self.m_suffix = val
        
    def setPrefix(self, val):
        self.m_prefix = val

    def Suffix(self):
        return self.m_suffix
    
    def Prefix(self):
        return self.m_prefix
    
    def setFlag(self, val: bool = True):
        self.flag = val

class MyLineEdit(QLineEdit):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)
        self.textChanged.connect(self.text_changed)

    def removeAccents(self, txt: str = ""):
        return ''.join(c for c in unicodedata.normalize('NFD', txt)
                  if unicodedata.category(c) != 'Mn')

    def text_changed(self):
        if self.text().isupper():
            # cursor = self.cursorPosition()
            # self.setText(self.removeAccents(self.text().upper()))
            # self.setCursorPosition(cursor)
            return
        else:
            cursor = self.cursorPosition()
            self.setText(self.text().upper())
            self.setCursorPosition(cursor)