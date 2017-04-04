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

    def __init__( self, gameBoardGui, gameInfoGui, player1, player2):
        self.players = [player1, player2]
        self.curPlayerNum = 0
        self.chatWindow = ChatGui()

        # Make middle game area
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        hbox.set_homogeneous(False)
        hbox.pack_start(self.gameBoardGui.mainBox, True, False, 0)
        hbox.pack_start(Gtk.Separator(orientation = Gtk.Orientation.VERTICAL), True, False, 0)
        hbox.pack_start(self.gameInfoGui.mainBox, True, False, 0)

        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.mainBox.set_homogeneous(False)
        self.mainBox.pack_start(hbox, False, False, 0)
        self.mainBox.pack_start(Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL), False, False, 0)
        self.mainBox.pack_start(self.chatWindow.mainBox, False, False, 0)


    def updatePlayer(self):
        self.players[self.curPlayerNum].turn = False
        self.curPlayerNum = (self.curPlayerNum + 1) % 2
        self.players[self.curPlayerNum].turn = True 


class TicTacToeGame(Game):

    def __init__(self, player1, player2):
        self.gameBoardGui = TicTacToeBoard() 
        self.gameInfoGui = TicTacToeInfoGui()
        Game.__init__(self, self.gameBoardGui, self.gameInfoGui, player1, player2)
        
        self.gameBoard = [ ["Blank", "Blank", "Blank"], 
                       ["Blank", "Blank", "Blank"],
                       ["Blank", "Blank", "Blank"] ]
        self.setFreshBoard()
        self.gameBoardGui.connectButtonSignal(self.tile_clicked_cb)
        self.gameInfoGui.connectAcceptSignal(self.rematchAccepted_clicked_cb)
        self.gameInfoGui.connectRejectSignal(self.rematchRejected_clicked_cb)

        self.mainBox.show_all()
        self.gameInfoGui.showMessageBox(False)


    def tile_clicked_cb(self, widget):
        if (self.getCurShape(widget) == "Blank"):
            self.setCurShape(widget)

            if (self.checkForWinner()):
                self.playerWon(widget)  
            else: 
                self.updatePlayer()
                self.gameInfoGui.updateGameInfo(self.players)


    def rematchAccepted_clicked_cb(self, widget):
        self.setFreshBoard()

        #rehide the message box
        self.gameInfoGui.showMessageBox(False)


    def rematchRejected_clicked_cb(self, widget):
        print("blah 2")


    def playerWon(self, widget):
        winner = self.players[self.curPlayerNum]
        winner.wins += 1

        loser = self.players[(self.curPlayerNum + 1) % 2]
        loser.losses += 1

        winnerMesg = winner.name + " should be ashamed of that \n crushing defeat from "
        winnerMesg += loser.name + ".\n Want to redeem yourself with a rematch?"
        self.gameInfoGui.updateMessage(winnerMesg)

        self.gameInfoGui.updateGameInfo(self.players)

        #show the message box
        self.gameInfoGui.showMessageBox(True)


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


    def setFreshBoard(self):
        print("Making Game Board")
        self.gameBoard = [ ["Blank", "Blank", "Blank"], 
                       ["Blank", "Blank", "Blank"],
                       ["Blank", "Blank", "Blank"] ]


        
class GameBoardGui:
    
    def __init__( self ):
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        self.mainBox.set_homogeneous(False)



class TicTacToeBoard(GameBoardGui):
    tileDic = {
            "X" : GdkPixbuf.Pixbuf.new_from_file_at_scale("Images/XTile.png", width=200,
                height=200,preserve_aspect_ratio=True ),
            "O" : GdkPixbuf.Pixbuf.new_from_file_at_scale("Images/OTile.png", width=200,
                height=200,preserve_aspect_ratio=True ),
            "Blank" : GdkPixbuf.Pixbuf.new_from_file_at_scale("Images/BlankTile.png", width=200,
                height=200,preserve_aspect_ratio=True ),
    }


    def __init__(self):
        GameBoardGui.__init__( self )

        self.gameBoard = Gtk.Grid(orientation = Gtk.Orientation.HORIZONTAL)
        self.mainBox.pack_start(self.gameBoard, False, False, 0)
        self.board = [[col for col in range(0,3)] for row in range(0,3)]

        for i in range(0, 3):
            for j in range(0,3):
                button = Gtk.Button()
                button.set_relief(Gtk.ReliefStyle.NONE)
                button.set_name( str(j) + str(i))
                self.board[j][i] =  button

                image = Gtk.Image()
                image.set_from_pixbuf(TicTacToeBoard.tileDic["Blank"])
                button.add(image)

                self.gameBoard.attach(button,i, j, 1, 1) 


    def connectButtonSignal(self, callback_func):
        for rowOfButton in self.board:
            for button in rowOfButton:
                button.connect("clicked", callback_func)


    def setImageShape(self, widget, shape):
        widget.get_child().set_from_pixbuf(TicTacToeBoard.tileDic[shape])


    def refreshGui():
        for i in range(0,3):
            for j in range(0, 3):
                self.builder.get_object(self.gameStr + "Button" + str(i) + str(j) +
                        "Tile").set_from_file("Blank" + "Tile.png")



class GameInfoGui:
    
    def __init__( self):
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.mainBox.set_homogeneous(True)

        self.gameStatsBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.gameStatsBox.set_homogeneous(False)
        self.gameStatsBoxLabel = Gtk.Label( "Game Info" )
        self.gameStatsBox.pack_start(self.gameStatsBoxLabel, True,
                False, 0)

        self.gameMessageBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.gameMessageBox.set_homogeneous(False)

        self.mainBox.pack_start(self.gameStatsBox, True, False, 0)
        self.mainBox.pack_start(self.gameMessageBox, True, False, 0)


class TicTacToeInfoGui(GameInfoGui):

    def __init__(self):
        GameInfoGui.__init__(self)

        self.gameInfoGrid = Gtk.Grid(orientation = Gtk.Orientation.HORIZONTAL,
                hexpand=True)
        self.gameInfoGrid.set_row_homogeneous(True)
        self.gameInfoGrid.set_row_spacing(10)
        self.gameInfoGrid.set_column_homogeneous(True)
        self.gameInfoGrid.set_column_spacing(10)

        self.XnameLabel = Gtk.Label("playerX")
        self.XturnLabel = Gtk.Label("yes")
        self.XwinsLabel = Gtk.Label("0")
        self.XlossesLabel = Gtk.Label("0")

        self.OnameLabel = Gtk.Label("playerO")
        self.OturnLabel = Gtk.Label("No")
        self.OwinsLabel = Gtk.Label("0")
        self.OlossesLabel = Gtk.Label("0")

        self.infoDic = {
            "X" : { "name" : self.XnameLabel,
                    "turn" : self.XturnLabel,
                    "wins" : self.XwinsLabel,
                    "losses" : self.XlossesLabel 
                },
            "O" : { "name" : self.OnameLabel,
                    "turn" : self.OturnLabel,
                    "wins" : self.OwinsLabel,
                    "losses" : self.OlossesLabel
                }
            }

        self.height = 1
        self.width = 1

        self.gameInfoGrid.attach(Gtk.Label("name"), 0, 0, self.height, self.width) 
        self.gameInfoGrid.attach(Gtk.Label("turn"), 1, 0, self.height, self.width) 
        self.gameInfoGrid.attach(Gtk.Label("wins"), 2, 0, self.height, self.width) 
        self.gameInfoGrid.attach(Gtk.Label("losses"), 4, 0, self.height, self.width) 

        self.gameInfoGrid.attach(self.infoDic["X"]["name"], 0, 1, self.height, self.width) 
        self.gameInfoGrid.attach(self.infoDic["X"]["turn"], 1, 1, self.height, self.width) 
        self.gameInfoGrid.attach(self.infoDic["X"]["wins"], 2, 1, self.height, self.width) 
        self.gameInfoGrid.attach(self.infoDic["X"]["losses"], 4, 1, self.height, self.width) 

        self.gameInfoGrid.attach(self.infoDic["O"]["name"], 0, 2, self.height, self.width) 
        self.gameInfoGrid.attach(self.infoDic["O"]["turn"], 1, 2, self.height, self.width) 
        self.gameInfoGrid.attach(self.infoDic["O"]["wins"], 2, 2, self.height, self.width) 
        self.gameInfoGrid.attach(self.infoDic["O"]["losses"], 4, 2, self.height, self.width) 
       
        # Set up Message Area
        self.gameMessageArea = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.gameMessageArea.set_homogeneous(False) 

        self.gameMessage = Gtk.Label("Here is my message")
        self.gameMessage.set_line_wrap(True)
        self.gameMessage.set_justify(Gtk.Justification.FILL)
        self.gameMessageArea.pack_start(self.gameMessage, False, False, 0)

        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        hbox.set_homogeneous(True) 
        self.gameMessageArea.pack_start(hbox, False, False, 0)

        self.rejectButton = Gtk.Button( label = "Reject" )
        hbox.pack_start(self.rejectButton, True, False, 0)

        self.acceptButton = Gtk.Button( label = "Accept" ) 
        hbox.pack_start(self.acceptButton, True, False, 0)

        self.gameStatsBox.pack_start(self.gameInfoGrid, True, False, 0)
        self.gameMessageBox.pack_start(self.gameMessageArea, False, False, 0)

    #TODO: Make dictionary of signals to attach in one go
    def connectAcceptSignal(self, callback_func):
        self.acceptButton.connect("clicked", callback_func)


    def connectRejectSignal(self, callback_func):
        self.rejectButton.connect("clicked", callback_func)

    
    def updateMessage(self, messageText):
        self.gameMessage.set_text(messageText)


    def showMessageBox(self, showBool):
        if (showBool):
            self.gameMessageBox.show()
        else:
            self.gameMessageBox.hide()


    def updateGameInfo(self, players):
        for player in players:
            self.infoDic[player.shape]["name"].set_text(player.name)
            self.infoDic[player.shape]["turn"].set_text(str(player.turn))
            self.infoDic[player.shape]["wins"].set_text(str(player.wins))
            self.infoDic[player.shape]["losses"].set_text(str(player.losses))

    

class ChatGui:

    def __init__( self ):
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.mainBox.set_homogeneous(False)
        self.mainBox.pack_start(Gtk.Label( "Chat box here"), True, False, 0)



class GameFactory:
    games = { "TicTacToe" : TicTacToeGame }

    def constructGame(gameType, gameId, player1, player2):
        gameId = gameId

        game =  GameFactory.games[gameType](player1, player2) 
        return game 



class ApplicationGui:
    tabGames = []   

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


    def add_tab_cb(self, widget):
        gameNum = str(self.notebookLastPage + 1)

        player1 = Player("Brandon", "X", True, "local")
        player2 = Player("Other Brandon", "O", False, "local")
        gameId = "game" + gameNum
        self.tabGames.append(GameFactory.constructGame("TicTacToe", gameId, player1, player2))
        self.notebook.insert_page(self.tabGames[-1].mainBox, Gtk.Label(gameId), self.notebookLastPage)

        self.notebookLastPage += 1



applicationGui = ApplicationGui()
curWindow = applicationGui.window
curWindow.show_all()

Gtk.main()
