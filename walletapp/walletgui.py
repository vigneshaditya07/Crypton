import sys
import threading
import base58
from wallet import Wallet, WalletData
from PyQt5.QtCore import QAbstractListModel, QObject, Qt,pyqtProperty, pyqtSlot,QModelIndex
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from random import choice



class ContactModel(QAbstractListModel):

    Name = Qt.UserRole + 1
    Address = Qt.UserRole + 2
    IconColor = Qt.UserRole + 3
    IconColors = ["#f23e02","#ef476f","#7400b8","#ae0c3e","#06d6a0","#118ab2","#073b4c"]

    def __init__(self,contacts,parent=None) -> None:
        super().__init__(parent=parent)
        self.contacts = contacts

    def data(self, index, role: int):
        r=index.row()
        if role==self.Name:
            return self.contacts[r].get("name","#No Name#")
        if role==self.Address:
            return self.contacts[r].get("address","#No Addresss#")
        if role==self.IconColor:
            return self.contacts[r].get("iconcolor","#4a4e69")

    def rowCount(self,parent=None) -> int:
        return len(self.contacts)

    def roleNames(self):
        return {
            Qt.UserRole + 1 : b'name',
            Qt.UserRole + 2 : b'address',
            Qt.UserRole + 3 : b'iconcolor'
        }

    @pyqtSlot(str, str)
    def addContact(self, name, address):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.contacts.append({"name":name,"address":address,"iconcolor":choice(self.IconColors)})
        self.endInsertRows()

class WalletUI(QObject):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)


    def load_wallet(self,wallet:Wallet):
        self.wallet = wallet
        self.contact_model =ContactModel(self.wallet.walletdata.contacts)

    @pyqtProperty('QString')
    def balance(self):
        return str(round(self.wallet.walletdata.balance/10000,4))

    @pyqtProperty('QVariant')
    def contactModel(self):
        return self.contact_model

    @pyqtSlot('QString','QString')
    def addContact(self,name,address):
        print("Contact : {",name,",",address,"} added")
        self.contact_model.addContact(name,address)

    @pyqtSlot('QString','QString',result='QVariant')
    def checkPay(self,address,samount):
        payvalid=[False,False]    #  [address,amount]
        try:
            base58.b58decode_check(address)
            payvalid[0] = True
        except ValueError:
            payvalid[0] = False
        try:
            amount = int(float(samount)*10000)
        except:
            payvalid[1] = False
            return payvalid
        if amount>self.wallet.walletdata.balance:
            payvalid[1] = False
        else:
            payvalid[1] = True
        if(payvalid[0] and payvalid[1]):
            self.payment = (address,amount)
        return payvalid
        

QGuiApplication.setAttribute(Qt.AA_UseOpenGLES)
app = QGuiApplication(sys.argv)

walletdata = WalletData()
walletdata.add_contact({"name":"test","address":"addr1"})
walletdata.add_contact({"name":"test2","address":"addr2"})
walletdata.balance = 100000
wallet = Wallet(walletdata)
walletui = WalletUI()
walletui.load_wallet(wallet)
engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("Wallet",walletui)
engine.load('walletapp/ui/main.qml')
engine.quit.connect(app.quit)

sys.exit(app.exec())