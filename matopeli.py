
# 'pip install PySide6' tarvitaan
# Rasmus
# Joakim 
# Markus
# Miika
import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QTimer

# vakiot
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        
        # pelin aloitus nappia painamalla
        self.game_started = False  # logiikka pelin aloitukseen nappia painamalla
        self.init_screen()  # Näytä aloitusruutu
    
    # metodi aloitusruudun tekstiin
    def init_screen(self):
        start_text = self.scene().addText("Paina jotain nappia aloittaaksesi pelin", QFont("Arial", 16)) #Peinennin fonttia jotta näyttää vähän paremmalta T Markus
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)

    def keyPressEvent(self, event):
        key = event.key()  # napin painamisen assignaaminen
        
        # pelin aloitus nappia painamalla (jos ei ole vielä aloitettu)
        if not self.game_started:  # varmistus että pelin aloitus onnistuu
            # Estetään nuolinäppäinten käyttö pelin uudelleenaloitukseen
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                return  # Ei tehdä mitään nuolinäppäimillä

            #Poistetaan "Game over" teksti ja aloitetaan uusi peli
            self.game_started = True
            self.scene().clear()
            self.start_game()
            return
        
        # Ei Tarvitse Muokata, Tämä liikuttaa matoa nuolinäppäimillä
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            # päivitetään suunta vain jos se ei ole vastakkainen valitulle suunnalle
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key

    def update_game(self):
        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        # Tarkistetaan osuma pelialueen rajoihin tai matoon itseensä
        if (new_head in self.snake or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT)): # Mato osuu itseensä, vasemmalle/oikealle seinälle tai ylä/ala seinälle

            self.timer.stop() #Pysäyttää pelin
            
            # "Game over" teksti
            game_over_text = self.scene().addText("Game Over\nAloita uusi peli painamalla mitä tahansa näppäintä", QFont("Arial", 12)) #Pienennin fonttia jotta saa tekstin mahtumaan T Markus
            text_width = game_over_text.boundingRect().width()
            text_x = (self.width() - text_width) / 2 # Keskittää vaakasuunassa
            game_over_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2) # Asetetaan pystysuunassa

            #Asetetaan peli uudelleenaloitus tilaan
            self.game_started = False
            return


        self.snake.insert(0, new_head)
        
        self.snake.pop()

        self.print_game()

    def print_game(self):
        self.scene().clear()

        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.black))
        
    def start_game(self):
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.timer.start(300)
        
        self.print_game()




def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
