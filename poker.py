import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

bb, sb, dealer = 0, 1, 2

class Player:
  chips, email, name, c1, c2 = 0, '', '', '', ''
  def __init__(self, n, e):
    self.chips = 1000
    self.email = e.rstrip()
    self.name = n.rstrip()
  
  def info(self):
    print('********\n', 'Chips:', self.chips, '\n********\n')
  
  def set(self, card1, card2):
    self.c1 = card1
    self.c2 = card2

  def show_c1(self):
    print(self.name + ' has ' + self.c1[0] + ' of ' + self.c1[1])

  def show_c2(self):
    print(self.name + ' has ' + self.c2[0] + ' of ' + self.c2[1])
  
  def show_both(self):
    print(self.name + ' has ' + self.c1[0] + ' of ' + self.c1[1] + ' and ' + self.c2[0] + ' of ' + self.c2[1])

  def pay(self, x):
    self.chips -= x

def send(email, card1, card2):
  me, my_password, msg = "haimingericxu@gmail.com", "nVWRD679!", MIMEMultipart('alternative')
  msg['To'] = email 
  msg['Subject'] = card1[0] + " of " + card1[1] + ", " + card2[0] + " of " + card2[1] 
  msg['From'] = me
  html = '<html><body><p>Your Hand!!!!!</p></body></html>'
  part2 = MIMEText(html, 'html')
  msg.attach(part2)
  s = smtplib.SMTP_SSL('smtp.gmail.com')
  s.login(me, my_password)
  s.sendmail(me, email, msg.as_string())
  s.quit()

def play(players, turn, p, f, end):
  while (True):
    if ((max(p) - p[sb] > 0 or not turn[sb]) and not f[sb]):
      turn[sb] = True
      print('\nAction on ' + players[sb].name + '...')
      action = input(str(max(p) - p[sb]) + ' to call, ' + str(players[sb].chips) + ' chips\n')
      if action == 'call':
        players[sb].chips -= (max(p) - p[sb])
        print(players[sb].name + ' -' + str(max(p) - p[sb]) + ' : ' + str(players[sb].chips))
        p[sb] += (max(p) - p[sb])
      elif action == 'fold':
        f[sb] = True
        counter = 0
        for i in range(3):
          if f[i]:
            counter += 1
        if counter == 2:
          end = True
          break
      else:
        p[sb] += int(action)
        players[sb].chips -= int(action)
        print(players[sb].name + ' -' + action + ' : ' + str(players[sb].chips))
    if ((max(p) - p[bb] > 0 or not turn[bb]) and not f[bb]):
      turn[bb] = True
      print('\nAction on ' + players[bb].name + '...')
      action = input(str(max(p) - p[bb]) + ' to call, ' + str(players[bb].chips) + ' chips\n')
      if action == 'call':
        players[bb].chips -= (max(p) - p[bb])
        print(players[bb].name + ' -' + str(max(p) - p[bb]) + ' : ' + str(players[bb].chips))
        p[bb] += (max(p) - p[bb])
      elif action == 'fold':
        f[bb] = True
        counter = 0
        for i in range(3):
          if f[i]:
            counter += 1
        if counter == 2:
          end = True
          break
      else:
        p[bb] += int(action)
        players[bb].chips -= int(action)
        print(players[bb].name + ' -' + action + ' : ' + str(players[bb].chips))
    if ((max(p) - p[dealer] > 0 or not turn[dealer]) and not f[dealer]):
      turn[dealer] = True
      print('\nAction on ' + players[dealer].name + '...')
      action = input(str(max(p) - p[dealer]) + ' to call, ' + str(players[dealer].chips) + ' chips\n')
      if action == 'call':
        players[dealer].chips -= (max(p) - p[dealer])
        print(players[dealer].name + ' -' + str(max(p) - p[dealer]) + ' : ' + str(players[dealer].chips))
        p[dealer] += (max(p) - p[dealer])
      elif action == 'fold':
        f[dealer] = True
        counter = 0
        for i in range(3):
          if f[i]:
            counter += 1
        if counter == 2:
          end = True
          break
      else:
        p[dealer] += int(action)
        players[dealer].chips -= int(action)
        print(players[dealer].name + ' -' + action + ' : ' + str(players[dealer].chips))
    if not con(p, f):
      break
  if end:
    for i in range(3):
      if not f[i]:
        players[i].chips += sum(p)
        break
    print('\n' + p1.name + ': ' + str(p1.chips) + '\n' + p2.name + ': ' + str(p2.chips) + '\n' + p3.name + ': ' + str(p3.chips))
    if input('New hand? ') == 'y':
      return 1
    return

def con(pot, fold):
  b, s = -1, 100000000000
  for i in range(3):
    if not fold[i]:
      s = min(s, pot[i])
      b = max(b, pot[i]) 
  return s - b != 0

def new_hand(p1, p2, p3):
  global bb, sb, dealer
  bb, sb, dealer = (bb + 1) % 3, (sb + 1) % 3, (dealer + 1) % 3
  values, suites, total = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"], ["Hearts", "Spades", "Diamonds", "Clubs"], []
  for i in range(2, 15):
    for j in range(4):
      total.append([values[i - 2], suites[j]])
  players, table = [p1, p2, p3], []
  for i in range(3):
    temp1 = total.pop(random.randint(0, len(total) - 1))
    temp2 = total.pop(random.randint(0, len(total) - 1))
    players[i].set(temp1, temp2)
    send(players[i].email, players[i].c1, players[i].c2) 
  p, f, end, turn = [0, 0, 0], [False, False, False], False, [False, False, False]
  print('********\nPre-flop\nBig blind ante of 10 chips, small blind ante of 5 chips')
  players[bb].pay(10)
  players[sb].pay(5)
  p[bb], p[sb] = 10, 5
  print(players[bb].name + ' -10: ' + str(players[bb].chips) + '\n' + players[sb].name + ' -5: ' + str(players[sb].chips))
  while (con(p, f)):
    print('\nAction on ' + players[dealer].name + '...') 
    if (max(p) - p[dealer] > 0 and not f[dealer]):
      action = input(str(max(p) - p[dealer]) + ' to call, ' + str(players[dealer].chips) + ' chips\n')
      if action == 'call':
        players[dealer].chips -= (max(p) - p[dealer])
        print(players[dealer].name + ' -' + str(max(p) - p[dealer]) + ' : ' + str(players[dealer].chips))
        p[dealer] += (max(p) - p[dealer])
      elif action == 'fold':
        f[dealer] = True 
        counter = 0
        for i in range(3):
          if f[i]:
            counter += 1
        if counter == 2:
          end = True
          break
      else:
        p[dealer] += int(action)
        players[dealer].chips -= int(action)
        print(players[dealer].name + ' -' + action + ' : ' + str(players[dealer].chips))
    if (max(p) - p[sb] > 0 and not f[sb]):
      print('\nAction on ' + players[sb].name + '...')
      action = input(str(max(p) - p[sb]) + ' to call, ' + str(players[sb].chips) + ' chips\n')
      if action == 'call':
        players[sb].chips -= (max(p) - p[sb])
        print(players[sb].name + ' -' + str(max(p) - p[sb]) + ' : ' + str(players[sb].chips))
        p[sb] += (max(p) - p[sb])
      elif action == 'fold':
        f[sb] = True
        counter = 0
        for i in range(3):
          if f[i]:
            counter += 1
        if counter == 2:
          end = True
          break
      else:
        p[sb] += int(action)
        players[sb].chips -= int(action) 
        print(players[sb].name + ' -' + action + ' : ' + str(players[sb].chips))
    if ((max(p) - p[bb] > 0 or not turn[bb]) and not f[bb]):
      print('\nAction on ' + players[bb].name + '...')
      turn[bb] = True
      action = input(str(max(p) - p[bb]) + ' to call, ' + str(players[bb].chips) + ' chips\n')
      if action == 'call':
        players[bb].chips -= (max(p) - p[bb])
        print(players[bb].name + ' -' + str(max(p) - p[bb]) + ' : ' + str(players[bb].chips))
        p[bb] += (max(p) - p[bb])
      elif action == 'fold':
        f[bb] = True
        counter = 0
        for i in range(3):
          if f[i]:
            counter += 1
        if counter == 2:
          end = True
          break
      else:
        p[bb] += int(action)
        players[bb].chips -= int(action)
        print(players[bb].name + ' -' + action + ' : ' + str(players[bb].chips))
  if end:
    for i in range(3):
      if not f[i]:
        players[i].chips += sum(p)
        break
    if input('New hand? ') == 'y':
      new_hand(p1, p2, p3)
    return
  print('\n********\nFlop')
  for i in range(3):
    table.append(total.pop(random.randint(0, len(total) - 1)))
    print(table[-1][0] + " of " + table[-1][1])
  print('\n' + p1.name + ': ' + str(p1.chips) + '\n' + p2.name + ': ' + str(p2.chips) + '\n' + p3.name + ': ' + str(p3.chips))
  turn = [False, False, False]
  if play(players, turn, p, f, end) == 1:
    for i in range(3):
      if not f[i]:
        players[i].chips += sum(p)
        break
    print('\n' + p1.name + ': ' + str(p1.chips) + '\n' + p2.name + ': ' + str(p2.chips) + '\n' + p3.name + ': ' + str(p3.chips))
    if input('New hand? ') == 'y':
      new_hand(p1, p2, p3)
    return
  print('\n' + p1.name + ': ' + str(p1.chips) + '\n' + p2.name + ': ' + str(p2.chips) + '\n' + p3.name + ': ' + str(p3.chips) + '\n********\nTurn')
  table.append(total.pop(random.randint(0, len(total) - 1)))
  for i in range(len(table)):
    print(table[i][0] + " of " + table[i][1])
  turn = [False, False, False]
  if play(players, turn, p, f, end) == 1:
    for i in range(3):
      if not f[i]:
        players[i].chips += sum(p)
        break
    print('\n' + p1.name + ': ' + str(p1.chips) + '\n' + p2.name + ': ' + str(p2.chips) + '\n' + p3.name + ': ' + str(p3.chips))
    if input('New hand? ') == 'y':
      new_hand(p1, p2, p3)
    return
  print('\n' + p1.name + ': ' + str(p1.chips) + '\n' + p2.name + ': ' + str(p2.chips) + '\n' + p3.name + ': ' + str(p3.chips) + '\n********\nRiver')
  table.append(total.pop(random.randint(0, len(total) - 1)))
  for i in range(len(table)):
    print(table[i][0] + " of " + table[i][1])
  if play(players, turn, p, f, end) == 1:
    for i in range(3):
      if not f[i]:
        players[i].chips += sum(p)
        break
    print('\n' + p1.name + ': ' + str(p1.chips) + '\n' + p2.name + ': ' + str(p2.chips) + '\n' + p3.name + ': ' + str(p3.chips) + '\n')
    if input('New hand? ') == 'y':
      new_hand(p1, p2, p3)
    return
  for i in range(3):
    if not f[i]:
      players[i].show_both()
  winner = input("Who is the winner? ")
  for i in range(3):
    if players[i].name == winner:
      players[i].chips += sum(p)
      print('\n' + p1.name + ': ' + str(p1.chips) + '\n' + p2.name + ': ' + str(p2.chips) + '\n' + p3.name + ': ' + str(p3.chips) + '\n')
      break
  if input('New hand? ')[0] == 'y':
    new_hand(p1, p2, p3) 
     
f = open("players.txt", "r")
p1 = Player(f.readline(), f.readline())
p2 = Player(f.readline(), f.readline())
p3 = Player(f.readline(), f.readline())
new_hand(p1, p2, p3)
