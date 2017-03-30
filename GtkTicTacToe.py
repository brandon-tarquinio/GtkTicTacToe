import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class Player:

    def __init__(self, name, shape, turn, playerType):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.turn = turn

        self.playerType = playerType
        self.shape = shape 


class Game:

    def __init__(self, builder, gameId, player1, player2):
        # Wire Signals 
        signals = {
            "cell_clicked_cb" : self.cell_clicked_cb,
            "RematchAccepted_clicked_cb" : self.rematchAccepted_clicked_cb,
            "RematchRejected_clicked_cb" : self.rematchRejected_clicked_cb,
            "create-window_cb"             : self.create_window_cb
        }
        builder.connect_signals( signals)

        # Init attributes
        self.players = [player1, player2]
        self.curPlayer = self.players[0]
        self.builder = builder
        self.gameStr = "Game" + str(gameId)
        self.gameInfoBox = builder.get_object("Game" + str(gameId) + "GameInfoGrid")

        #Setup game grid
        self.setFreshBoard()
        self.updateGameInfo()

    def create_window_cb(self, widget):
        print("asdfasdf")

    def cell_clicked_cb(self, widget):
        if (self.getCurImage(widget) == "Blank"):
            self.setCurImage(widget)

            if (self.checkForWinner()):
                self.playerWon(widget)  
            else: 
                self.updatePlayer()
                self.updateGameInfo()

    def rematchAccepted_clicked_cb(self, widget):
        self.setFreshBoard()

        #rehide the box
        self.builder.get_object("WinEventBox").set_opacity(0)

    def rematchRejected_clicked_cb(self, widget):
        print("blah 2")


    def playerWon(self, widget):
        if (self.curPlayer == self.players[0]):
            self.players[0].wins += 1
            self.players[1].losses += 1
            self.builder.get_object("WinnerMesg").set_text(self.players[1].name +
                    " should be ashamed of that\n crushing defeat from " +
                    self.players[0].name + ".\n Want to redeem yourself with a rematch?")
        else:
            self.players[1].wins += 1
            self.players[0].losses += 1
            self.builder.get_object("WinnerMesg").set_text(self.players[0].name +
                    " should be ashamed of that\n crushing defeat from " +
                    self.players[1].name + ".\n Want to redeem yourself with a rematch?")

        self.updateGameInfo()
        self.builder.get_object("WinnerMesg").set_line_wrap(True)
        #self.builder.get_object("WinnerMesg").set_justify(Gtk.Justification.FILL)
        
        #Unhide the box
        self.builder.get_object("WinEventBox").set_opacity(1.0)


    def setFreshBoard(self):
        self.gameBoard = [ ["Blank", "Blank", "Blank"], 
                       ["Blank", "Blank", "Blank"],
                       ["Blank", "Blank", "Blank"] ]
        for i in range(0,3):
            for j in range(0, 3):
                self.builder.get_object(self.gameStr + "Button" + str(i) + str(j) +
                        "Tile").set_from_file("Blank" + "Tile.png")


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

        widget.get_child().set_from_pixbuf(tileDic[shape])
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
            self.builder.get_object(self.gameStr + "Player" + player.shape + "Wins").set_text(str(player.wins))
            self.builder.get_object(self.gameStr + "Player" + player.shape +
                    "Losses").set_text(str(player.losses))


tileDic = {
        "X" : GdkPixbuf.Pixbuf.new_from_file_at_scale("XTile.png", width=200,
            height=200,preserve_aspect_ratio=True ),
        "O" : GdkPixbuf.Pixbuf.new_from_file_at_scale("OTile.png", width=200,
            height=200,preserve_aspect_ratio=True ),
        "Blank" : GdkPixbuf.Pixbuf.new_from_file_at_scale("BlankTile.png", width=200,
            height=200,preserve_aspect_ratio=True ),
}


class TicTacToeGame:

    def __init__(self, gameBoardGui, gameInfoGui, player1, player2 ):
        self.gameBoardGui = gameBoardGui
        self.gameInfoGui = GameInfoGui
        self.players = [player1, player2]
        self.curPlayerNum = 0

        self.setFreshBoard()
        self.gameBoardGui.connectButtonSignal(self.tile_clicked_cb)

    def tile_clicked_cb(self, widget):
        if (self.getCurShape(widget) == "Blank"):
            self.setCurShape(widget)

            if (self.checkForWinner()):
                self.playerWon(widget)  
            else: 
                self.updatePlayer()
#                self.updateGameInfo()

    def rematchAccepted_clicked_cb(self, widget):
        self.setFreshBoard()

        #rehide the box
        #self.builder.get_object("WinEventBox").set_opacity(0)

    def rematchRejected_clicked_cb(self, widget):
        print("blah 2")

    def playerWon(self, widget):
        winner = self.players[self.curPlayerNum]
        winner.wins += 1

        loser = self.players[(self.curPlayerNum + 1) % 2]
        loser.losses += 1

        winnerMesg = winner.name + " should be ashamed of that \n crushing defeat from "
        winnerMesg += loser.name + ".\n Want to redeem yourself with a rematch?"
        print(winnerMesg)
        #self.builder.get_object("WinnerMesg").set_text

        #self.updateGameInfo()

        #self.builder.get_object("WinnerMesg").set_line_wrap(True)
        #self.builder.get_object("WinnerMesg").set_justify(Gtk.Justification.FILL)
        
        #Unhide the box
        #self.builder.get_object("WinEventBox").set_opacity(1.0)

    # Returns true when a line contains all x or all o
    def checkLine(self, line):
        return (line[0] != "Blank") and (line[0] == line[1]) and (line[1] == line[2])

    # Returns true if a line is all the same 
    def checkForWinner(self):
        #check cols 
        for colNum in range(0,3):
            if ( self.checkLine([row[colNum] for row in self.gameBoard]) ):
                return True

        #check rows
        for row in self.gameBoard:
            if ( self.checkLine(row) ):
                return True

        #check diagonals
        return self.checkLine([self.gameBoard[i][i] for i in range(0,3)]) or self.checkLine( 
                [ self.gameBoard[2][0], self.gameBoard[1][1], self.gameBoard[0][2] ])


    def getCurShape(self, widget):
        print(widget.get_name())
        row = int(widget.get_name()[-2])
        col = int(widget.get_name()[-1])
        return self.gameBoard[row][col]

    def setCurShape(self, widget):
        row = int(widget.get_name()[-2])
        col = int(widget.get_name()[-1])
        self.gameBoard[row][col] = self.players[self.curPlayerNum].shape
        self.gameBoardGui.setImageShape(widget, self.players[self.curPlayerNum].shape)

    def updatePlayer(self):
        self.players[self.curPlayerNum].turn = False
        self.curPlayerNum = (self.curPlayerNum + 1) % 2
        self.players[self.curPlayerNum].turn = True 
        
    def setFreshBoard(self):
        self.gameBoard = [ ["Blank", "Blank", "Blank"], 
                       ["Blank", "Blank", "Blank"],
                       ["Blank", "Blank", "Blank"] ]

        

class GameBoardGui:
    
    def __init__( self ):
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        self.mainBox.set_homogeneous(False)

class TicTacToeBoard(GameBoardGui):

    def __init__(self):
        GameBoardGui.__init__( self )

        self.GameBoard = Gtk.Grid(orientation = Gtk.Orientation.HORIZONTAL)
        self.mainBox.pack_start(self.GameBoard, False, False, 0)
        self.board = [[col for col in range(0,3)] for row in range(0,3)]
        print(self.board)

        for i in range(0, 3):
            for j in range(0,3):
                button = Gtk.Button()
                button.set_relief(Gtk.ReliefStyle.NONE)
                button.set_name( str(j) + str(i))
                self.board[j][i] =  button

                image = Gtk.Image()
                image.set_from_pixbuf(tileDic["Blank"])
                button.add(image)

                self.GameBoard.attach(button,i, j, 1, 1) 

    def connectButtonSignal(self, callback_func):
        for rowOfButton in self.board:
            for button in rowOfButton:
                button.connect("clicked", callback_func)

    #def getCurImage(self, widget):
        #print(widget.get_name())
        #row = int(widget.get_name()[-2])
        #col = int(widget.get_name()[-1])
    #    return self.board[row][col]

    def setImageShape(self, widget, shape):
        widget.get_child().set_from_pixbuf(tileDic[shape])



class GameInfoGui:
    
    def __init__( self):
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.mainBox.set_homogeneous(True)

        self.gameStatsBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.gameStatsBox.set_homogeneous(False)
        self.gameStatsBox.pack_start(Gtk.Label( "This is the game stats box" ), True,
                False, 0)
        
        self.messageArea = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.messageArea.set_homogeneous(False)
        self.messageArea.pack_start(Gtk.Label( "This is the secret message area" ),
                True, False, 0)

        self.mainBox.pack_start(self.gameStatsBox, True, False, 0)
        self.mainBox.pack_start(self.messageArea, True, False, 0)


class ChatGui:

    def __init__( self ):
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.mainBox.set_homogeneous(False)
        self.mainBox.pack_start(Gtk.Label( "Chat box here"), True, False, 0)

class GameGui:

    def __init__( self, gameId, gameGui, gameInfoGui, chatGui):
        self.gameId = gameId
        players1 = Player("Brandon", "X", True, "local")
        players2 = Player("Other Brandon", "O", False, "local")
        self.gameLogic = TicTacToeGame(gameGui, gameInfoGui, players1, players2)  
        self.gameGui = gameGui
        self.gameInfoGui = gameInfoGui
        self.chatGui = chatGui
        


        # Make middle game area
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        hbox.set_homogeneous(False)
        hbox.pack_start(self.gameGui.mainBox, True, False, 0)
        hbox.pack_start(Gtk.Separator(orientation = Gtk.Orientation.VERTICAL), True, False, 0)
        hbox.pack_start(self.gameInfoGui.mainBox, True, False, 0)

        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.mainBox.set_homogeneous(False)
        self.mainBox.pack_start(hbox, False, False, 0)
        self.mainBox.pack_start(Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL), False, False, 0)
        self.mainBox.pack_start(self.chatGui.mainBox, False, False, 0)

class ApplicationGui:
    
    def __init__( self ):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("TicTacToeGui.glade")

        self.window = self.builder.get_object("MainWindow")
        self.window.connect("delete-event", Gtk.main_quit)

        self.notebook = self.builder.get_object("GameNotebook")

        # add next tab button
        addButton = Gtk.Button(label = "Add Game!")
        addButton.connect("clicked", self.add_tab_cb)
        self.notebook.append_page(Gtk.Box(), addButton)
        self.notebookLastPage = 1 


        player1 = Player("Brandon", "X", True, "local")
        player2 = Player("Other Brandon", "O", False, "local")
        gameId = 1
        self.Game1 = Game(self.builder, gameId, player1, player2)

    def add_tab_cb(self, widget):
        gameNum = str(self.notebookLastPage + 1)
        self.notebook.insert_page(GameGui( "game" + gameNum, TicTacToeBoard(),
            GameInfoGui(), ChatGui()).mainBox, Gtk.Label("Game" + gameNum),
            self.notebookLastPage)
        self.notebook.show_all()
        self.notebookLastPage += 1

applicationGui = ApplicationGui()
curWindow = applicationGui.window
curWindow.show_all()

Gtk.main()
