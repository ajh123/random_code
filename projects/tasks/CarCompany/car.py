from abc import abstractmethod, ABCMeta
from datetime import date

class Customer(metaclass=ABCMeta):
    def __init__(self, firstName: str, surName: str, dob: 'date', licenseNo: str):
        self.firstName = firstName
        self.surName = surName
        self.dob = dob
        self.licenseNo = licenseNo

    def viewCar(self):
        print("Custom view car")

    def searchForCar(self):
        print("Customer search car")

    @abstractmethod
    def rentCar(self):
        pass

class Guest(Customer):
    def rentCar():
        print("Guest rent car")

class Member(Customer):
    def __init__(self, firstName: str, surName: str, dob: date, licenseNo: str, username: str, password: str):
        super().__init__(firstName, surName, dob, licenseNo)
        self.username = username
        self.password = password

    def login(self):
        print("Member login")

    def editProfile(self):
        print("Member edit profile")

    def viewProfile(self):
        print("Member view profile")

    def rentCar(self):
        print("Member rent car")

    def logout(self):
        print("Member logout")

class Payment():
    def __init__(self, paymentDate: 'date', creditCardType: str, creditCardNo: str, nameOnCreditCard: str, creditExpirationDate: 'date') -> None:
        self.paymentDate = paymentDate
        self.creditCardType = creditCardType
        self.creditCardNo = creditCardNo
        self.nameOnCreditCard = nameOnCreditCard
        self.creditExpirationDate = creditExpirationDate