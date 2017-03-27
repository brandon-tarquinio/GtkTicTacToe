import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Player:

    def __init__(self, name, shape, turn, playerType):
        self.name = name
        self.wins = 0
        self.loses = 0
        self.turn = turn

        self.playerType = playerType
        self.shape = shape 


class Game:

    def __init__(self, builder, gameId, player1, player2):
        # Wire Signals 
        signals = {
            "cell_clicked_cb" : self.cell_clicked_cb,
        }
        builder.connect_signals( signals)

        # Init attributes
        self.gameBoard = [ ["Blank", "Blank", "Blank"], 
                       ["Blank", "Blank", "Blank"],
                       ["Blank", "Blank", "Blank"] ]

        self.players = [player1, player2]
        self.curPlayer = self.players[0]
        self.builder = builder
        self.gameStr = "Game" + str(gameId)
        self.gameInfoBox = builder.get_object("Game" + str(gameId) + "GameInfoGrid")

        #Setup game grid
        self.updateGameInfo()

    def cell_clicked_cb(self, widget):
        if (self.getCurImage(widget) == "Blank"):
            self.setCurImage(widget)

            if (self.checkForWinner()):
                self.playerWon()  
            else: 
                self.updatePlayer()
                self.updateGameInfo()

    def playerWon(self):
        if (self.curPlayer == self.players[0]):
            self.players[0].wins += 1
            self.players[1].losses += 1
        else:
            self.players[0].wins += 1
            self.players[1].losses += 1
        self.curPlayer.wins += 1 

    # Returns true when a line contains all x or all o
    def checkLine(self, line):
        return (line[0] != "Blank") and (line[0] == line[1]) and (line[1] == line[2])

    # Returns true if a line is all the same 
    def checkForWinner(self):
        #check cols 
        for colNum in range(0,3):
            if ( self.checkLine([row[colNum] for row in self.gameBoard]) ):
                return True

        #check cols
        for row in self.gameBoard:
            if ( self.checkLine(row) ):
                return True

        #check diagonals
        return self.checkLine([self.gameBoard[i][i] for i in range(0,3)]) or self.checkLine( 
                [ self.gameBoard[2][0], self.gameBoard[1][1], self.gameBoard[0][2] ])

    def getCurImage(self, widget):
        row = int(widget.get_name()[-2])
        col = int(widget.get_name()[-1])
        return self.gameBoard[row][col]


    def setCurImage(self, widget):
        shape = self.curPlayer.shape
        row = int(widget.get_name()[-2])
        col = int(widget.get_name()[-1])

        widget.get_child().set_from_file(shape + "Tile.png")        
        self.gameBoard[row][col] = self.curPlayer.shape 


    def updatePlayer(self):
        if (self.curPlayer == self.players[0]):
            self.players[0].turn = False
            self.players[1].turn = True
            self.curPlayer = self.players[1]
        else:
            self.players[1].turn = False
            self.players[0].turn = True
            self.curPlayer = self.players[0]

    def updateGameInfo(self):
        for player in self.players:
            self.builder.get_object(self.gameStr + "Player" + player.shape + "Name").set_text(player.name)
            self.builder.get_object(self.gameStr + "Player" + player.shape + "Turn").set_text(str(player.turn))

class TicTacToeGui:
    
  def __init__( self ):
    self.builder = Gtk.Builder()
    self.builder.add_from_file("TicTacToeGui.glade")

    self.window = self.builder.get_object("MainWindow")
    self.window.connect("delete-event", Gtk.main_quit)

    player1 = Player("Brandon", "X", True, "local")
    player2 = Player("Other Brandon", "O", False, "local")
    gameId = 1
    self.Game1 = Game(self.builder, gameId, player1, player2)


ticTacToeGui = TicTacToeGui()
curWindow = ticTacToeGui.window
curWindow.show_all()

Gtk.main()
