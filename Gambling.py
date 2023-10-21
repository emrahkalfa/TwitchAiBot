import random
import csv

class Game:

  def __init__(self, usr, amount):
    self.usr = usr
    self.amount = amount

class BankController:

  def __init__(self,bankLocation):
    self.bankLocation = bankLocation


  def CheckAmount(self, usr, amount):
    csv_file = self.bankLocation
    with open(csv_file, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
          if(row[0] == usr):
            if(int(row[1]) < int(amount)):
              return False
            return True

  def GetAmount(self, usr):
    csv_file = self.bankLocation
    with open(csv_file, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
          if(row[0] == usr):
            return row[1]


  def Trade(self, winner, loser):
    return "Trade Operations"

class GamblingHandler():

  matchOwners = []

  def __init__(self,path):
    self.matchOwners = []
    self.bank = BankController(path)

  def SetGame(self, game):
    if(not self.ControlBank(game.usr, int(game.amount))):
      return "Yetersiz Bakiye! Mevcut Bakiyen: " + self.bank.GetAmount(game.usr)
    if any(game.usr == match.usr for match in self.matchOwners):
      return "Kullanıcı zaten maç bekliyor!"
    self.matchOwners.append(game)
    return "Maç Hazır!"

  def CancelGame(self, usr):
    if(usr not in self.matchOwners.usr):
      print("Kullanıcının bekleyen maçı bulunmamaktadır!")
      return
    self.matchOwners.remove(game)

  def JoinGame(self, usr, guest):
    if (usr == guest):
      return "Kendine Meydan Okuyamazsın!"

    if(not self.ControlBank(guest, self.FindGame(usr).amount)):
      return "Yetersiz Bakiye! Mevcut Bakiyen: " + self.bank.GetAmount(guest)

    if all(match.usr != usr for match in self.matchOwners):
      return "Kullanıcının bekleyen maçı bulunmamaktadır, Kullanıcıya meydan okuyabilirsin!"
    return self.PlayGame(usr, guest)

  def PlayGame(self, usr, guest):
    self.matchOwners.remove(self.FindGame(usr))
    if(random.randint(1, 100) >= 50):
      return usr + " Kazandı!"
    return guest + " Kazandı!"

  def ControlBank(self, usr, amount):
    if(self.bank.CheckAmount(usr,amount)):
      return True
    return False
  
  def FindGame(self, usr)->Game:
    for user in self.matchOwners:
      if user.usr == usr:
        return user
