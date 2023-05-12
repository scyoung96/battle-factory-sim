from glob import glob
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from random import randint, choice
import signal
import sys
import os

from common.define import *

MEGAS = False
ALOLAN = False
GALARIAN = False
HISUIAN = False

class GUI(QMainWindow):
	def __init__(self):
		super(GUI,self).__init__()

		self.INACTIVE_STYLE = "background-color: rgb(200, 200, 200)"
		self.ACTIVE_STYLE = "background-color: none"

		self.mainWidget = None
		self.mainVbox = None

		self.mode = None
		self.pokedex = None

		self.teamRows = []
		self.currTeamRow = None
		self.loadedTeams = {}

		self.team = []
		self.teamIDs = []

		self.initUI()

	def initUI(self):
		self.setWindowTitle('Battle Factory Sim')
		self.setWindowIcon(QIcon('img/icon/favicon.png'))

		self.statusBar = QStatusBar()
		self.setStatusBar(self.statusBar)

		widget = QWidget()
		self.mainWidget = widget
		vbox = QVBoxLayout()
		self.mainVbox = vbox
		widget.setLayout(vbox)
		self.setCentralWidget(widget)

# SECTION: Choices Row
		self.choicesRow = self.createNewChoicesRow()
		vbox.addLayout(self.choicesRow)

# SECTION: Choose Button Row
		# container for row of buttons
		self.chooseButtonRow = self.createNewChooseButtonRow()
		vbox.addLayout(self.chooseButtonRow)

		self.chooseButtonRow.setContentsMargins(0,0,0,25)

# SECTION: Team Row
		newTeamRow = self.createNewTeamRow()
		self.teamRows.append(newTeamRow)
		self.currTeamRow = newTeamRow
		vbox.addLayout(newTeamRow)

# SECTION: Utility Button Row
		self.utilityButtonRow = self.createNewUtilityButtonRow()
		vbox.addLayout(self.utilityButtonRow)

		self.show()


# SECTION: Button Functions
	def createNewChoicesRow(self):
		choicesRow = QHBoxLayout()
		img = QPixmap('img/sprites/0 XY.png')

		choiceImgArr = [QLabel() for i in range(5)]

		for i in range(5):
			choiceImgArr[i].setFixedSize(100,100)
			choiceImgArr[i].setPixmap(img.scaled(100,100))
			choicesRow.addWidget(choiceImgArr[i])

		choicesRow.choiceImgArr = choiceImgArr
		
		return choicesRow


	def initChoices(self):
		img = QPixmap('img/sprites/0 XY.png')

		for image in self.choicesRow.choiceImgArr:
			image.setPixmap(img.scaled(100,100))


	def createNewChooseButtonRow(self):
		chooseButtonRow = QHBoxLayout()

		chooseButtons = [QPushButton() for i in range(5)]

		for i in range(5):
			chooseButtons[i].setFixedWidth(100)
			chooseButtonRow.addWidget(chooseButtons[i])

			if i == 2:
				chooseButtons[i].setText('Begin')
				chooseButtons[i].clicked.connect(self.startSim)
			else:
				chooseButtons[i].setVisible(False)

		chooseButtons[0].clicked.connect(self.chooseOption0)
		chooseButtons[1].clicked.connect(self.chooseOption1)
		chooseButtons[3].clicked.connect(self.chooseOption3)
		chooseButtons[4].clicked.connect(self.chooseOption4)
			
		chooseButtonRow.chooseButtons = chooseButtons

		return chooseButtonRow


	def initChooseButtons(self, finish=False):
		try:
			for button in self.chooseButtonRow.chooseButtons:
				button.clicked.disconnect()
		except:
			pass

		self.chooseButtonRow.chooseButtons[0].setVisible(False)
		self.chooseButtonRow.chooseButtons[0].clicked.connect(self.chooseOption0)
		self.chooseButtonRow.chooseButtons[1].setVisible(False)
		self.chooseButtonRow.chooseButtons[1].clicked.connect(self.chooseOption1)
		self.chooseButtonRow.chooseButtons[2].setText('Begin')
		self.chooseButtonRow.chooseButtons[2].clicked.connect(self.startSim)
		if finish:
			self.chooseButtonRow.chooseButtons[2].setEnabled(False)
		else:
			self.chooseButtonRow.chooseButtons[2].setEnabled(True)
		self.chooseButtonRow.chooseButtons[3].setVisible(False)
		self.chooseButtonRow.chooseButtons[3].clicked.connect(self.chooseOption3)
		self.chooseButtonRow.chooseButtons[4].setVisible(False)
		self.chooseButtonRow.chooseButtons[4].clicked.connect(self.chooseOption4)


	def createNewTeamRow(self):
		teamRow = QHBoxLayout()

		teamImgArr = [QLabel() for i in range(6)]

		for i in range(6):
			teamImgArr[i].setFixedSize(100,100)
			teamImgArr[i].setPixmap(QPixmap('img/none.png'))
			teamImgArr[i].setStyleSheet(self.INACTIVE_STYLE)
			teamImgArr[i].pixmap = None
			teamRow.addWidget(teamImgArr[i])

		teamRow.teamImgArr = teamImgArr

		teamRow.setContentsMargins(0,0,0,25)

		return teamRow

	
	def initTeamImgs(self):
		for img in self.currTeamRow.teamImgArr:
			img.setStyleSheet(self.INACTIVE_STYLE)
			img.setPixmap(QPixmap('img/none.png'))
			img.pixmap = None


	def addChoiceToTeam(self, choice):
		# populate next open slot
		for img in self.currTeamRow.teamImgArr:
			if img.pixmap == None:
				img.setPixmap(self.choicesRow.choiceImgArr[choice].pixmap())
				img.pixmap = 1
				break

		self.shuffleChoices()
		
		if len(self.team) == 6:
			self.initChoices()
			self.initChooseButtons(True)
			self.utilityButtonRow.saveButton.setEnabled(True)


	def populateAllTeamImgs(self, imgArr, ids):
		for i in range(len(ids)):
			img = QPixmap('img/sprites/' + ids[i])
			imgArr[i].setPixmap(img.scaled(100,100))
			imgArr[i].pixmap = 1


	def createNewUtilityButtonRow(self):
		utilityButtonRow = QHBoxLayout()

		utilityButtonsArr = [QPushButton() for i in range(3)]
		utilityButtonsArr.append(QComboBox())

		for i in range(4):
			if i == 0:
				utilityButtonsArr[i].setText('Save')
				utilityButtonsArr[i].clicked.connect(self.saveTeam)
				utilityButtonsArr[i].setEnabled(False)
			elif i == 1:
				utilityButtonsArr[i].setText('Load')
				utilityButtonsArr[i].clicked.connect(self.loadTeam)
				utilityButtonsArr[i].setEnabled(True)
			elif i == 2:
				utilityButtonsArr[i].setText('Reset')
				utilityButtonsArr[i].clicked.connect(self.reset)
			else:
				utilityButtonsArr[i].addItems(["National", "Paldea", "Paldea - Unique", "Paldea - Basic"])

			utilityButtonsArr[i].setFixedWidth(100)
			utilityButtonRow.addWidget(utilityButtonsArr[i])

		utilityButtonRow.utilityButtonsArr = utilityButtonsArr
		utilityButtonRow.saveButton = utilityButtonsArr[0]
		utilityButtonRow.loadButton = utilityButtonsArr[1]
		utilityButtonRow.resetButton = utilityButtonsArr[2]
		utilityButtonRow.modeButton = utilityButtonsArr[3]

		return utilityButtonRow


	def startSim(self):
		self.chooseButtonRow.chooseButtons[0].setVisible(True)
		self.chooseButtonRow.chooseButtons[1].setVisible(True)
		self.chooseButtonRow.chooseButtons[2].setText('')
		self.chooseButtonRow.chooseButtons[2].clicked.disconnect()
		self.chooseButtonRow.chooseButtons[2].clicked.connect(self.chooseOption2)
		self.chooseButtonRow.chooseButtons[3].setVisible(True)
		self.chooseButtonRow.chooseButtons[4].setVisible(True)

		self.mode = self.utilityButtonRow.modeButton.currentText()
		self.pokedex = POKEDEXES[self.mode]

		self.shuffleChoices()


	def shuffleChoices(self):
		seen = [int(i) for i in self.teamIDs]

		for i in range(5):
			rand = randint(0, len(self.pokedex)-1)
			while rand in seen:
				rand = randint(0, len(self.pokedex)-1)
			seen.append(rand)

			id = str(self.pokedex[rand]).zfill(4)
			img = QPixmap(self.getValidImgs(id))
			# img = QPixmap(img)
			self.choicesRow.choiceImgArr[i].setPixmap(img.scaled(100,100))
			self.choicesRow.choiceImgArr[i].setStyleSheet(self.INACTIVE_STYLE)

			self.chooseButtonRow.chooseButtons[i].setText(natdex_ref[id])
			self.chooseButtonRow.chooseButtons[i].id = id


	def getValidImgs(self, id):
		imgs = glob(f'img/sprites/{id}*.png')
		if not MEGAS:
			imgs = [img for img in imgs if 'M' not in img]
		if not ALOLAN:
			imgs = [img for img in imgs if 'A' not in img]
		if not GALARIAN and id != '0931':
			imgs = [img for img in imgs if 'G' not in img]
		if not HISUIAN:
			imgs = [img for img in imgs if 'H' not in img]
		try:
			ret = choice(imgs)
		except IndexError:
			ret = 'img/none.png'
		return ret


	def setButtonText(self, button, text):
		button.setText(text)


	def chooseOption0(self):
		self.team.append(self.chooseButtonRow.chooseButtons[0].text())
		self.teamIDs.append(self.chooseButtonRow.chooseButtons[0].id)
		self.addChoiceToTeam(0)


	def chooseOption1(self):
		self.team.append(self.chooseButtonRow.chooseButtons[1].text())
		self.teamIDs.append(self.chooseButtonRow.chooseButtons[1].id)
		self.addChoiceToTeam(1)


	def chooseOption2(self):
		self.team.append(self.chooseButtonRow.chooseButtons[2].text())
		self.teamIDs.append(self.chooseButtonRow.chooseButtons[2].id)
		self.addChoiceToTeam(2)


	def chooseOption3(self):
		self.team.append(self.chooseButtonRow.chooseButtons[3].text())
		self.teamIDs.append(self.chooseButtonRow.chooseButtons[3].id)
		self.addChoiceToTeam(3)


	def chooseOption4(self):
		self.team.append(self.chooseButtonRow.chooseButtons[4].text())
		self.teamIDs.append(self.chooseButtonRow.chooseButtons[4].id)
		self.addChoiceToTeam(4)


	def reset(self):
		self.initChoices()
		self.initChooseButtons()
		self.initTeamImgs()
		self.team = []
		self.teamIDs = []
		self.loadedTeams = {}
		self.utilityButtonRow.saveButton.setEnabled(False)


	def clearUI(self):
		self.mainWidget = QWidget()
		self.mainVbox = QVBoxLayout()
		self.mainWidget.setLayout(self.mainVbox)
		self.setCentralWidget(self.mainWidget)

		self.show()


	def saveTeam(self):
		if not os.path.exists('battle_factory_teams'):
			os.makedirs('battle_factory_teams')
		fileName = QFileDialog.getSaveFileName(self, 'Save File', 'battle_factory_teams/', 'bft')[0]
		with open(fileName + '.bft', 'w') as f_out:
			for pokemon in self.teamIDs:
				print(pokemon, file=f_out)


	def loadTeam(self):
		self.clearUI()

		fileName = QFileDialog.getOpenFileName(self, 'Open File')[0]
		with open(fileName, 'r') as f_in:
			count = 0
			shortName = fileName.split('/')[-1][:-4]
			self.teamIDs = []

			for line in f_in:
				pokemon = line.strip()
				self.teamIDs.append(pokemon)
				self.team.append(natdex_ref[pokemon])
				count += 1

				if count == 6:
					break

			self.loadedTeams[shortName] = [self.teamIDs, self.team]

			teamName = QLineEdit(shortName)
			teamName.setEnabled(False)
			self.mainVbox.addWidget(teamName)

			newTeamRow = self.createNewTeamRow()
			self.populateAllTeamImgs(newTeamRow.teamImgArr, self.teamIDs)
			self.mainVbox.addLayout(newTeamRow)


if __name__ == '__main__':
	# Allows CTRL+C in the terminal to kill the program
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	app = QApplication(sys.argv)
	window = GUI()
	sys.exit(app.exec())
