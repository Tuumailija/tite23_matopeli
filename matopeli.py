
# 'pip install PySide6' tarvitaan
# Rasmus
# Joakim 
# Markus
# Miika

# Tuodaan tarvittavat riippuvuudet ja kirjastot, joita tarvitaan
import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QTimer

# Vakiot
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Luokka, joka sisältää matopelin metodit
class SnakeGame(QGraphicsView):

    # Init-metodi aloitusruudulle
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.score = 0
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        
        # Pelin aloitus nappia painamalla
        self.game_started = False  # Logiikka pelin aloitukseen nappia painamalla
        self.init_screen()  # Näytä aloitusruutu
    
    # Metodi aloitusruudun tekstiin
    def init_screen(self):
        start_text = self.scene().addText("Paina näppäintä aloittaaksesi", QFont("Arial", 16))
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)

    # Metodi pelin uudelleenaloitukseen ja madon liikuttamiseen
    def keyPressEvent(self, event):
        key = event.key()  # Napin painamisen assignaaminen
        
        # Pelin aloitus nappia painamalla (jos ei ole vielä aloitettu)
        if not self.game_started:  # Varmistus että pelin aloitus onnistuu
            # Estetään nuolinäppäinten käyttö pelin uudelleenaloitukseen
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                return  # Ei tehdä mitään nuolinäppäimillä

            # Poistetaan "Game over" teksti ja aloitetaan uusi peli
            self.game_started = True
            self.scene().clear()
            self.start_game()
            return
        
        # Tämä liikuttaa matoa nuolinäppäimillä
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            # Päivitetään suunta vain jos se ei ole vastakkainen valitulle suunnalle
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key    

    # Metodi madon päivitykseen
    def update_game(self):
        head_x, head_y = self.snake[0]

        # Tarkistetaan madon suunta ja päivitetään se jos se muuttuu
        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        # Tarkistetaan osuuko mato pelialueen rajoihin tai itseensä
        if (new_head in self.snake or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT)): # Mato osuu itseensä, vasemmalle/oikealle seinälle tai ylä/ala seinälle

            self.timer.stop() #Pysäyttää pelin
            
            # "Game over" ja "Aloita uusi peli" tekstit
            game_over_text = self.scene().addText("Game Over\nAloita uusi peli painamalla mitä tahansa näppäintä", QFont("Arial", 12)) #Pienennin fonttia jotta saa tekstin mahtumaan T Markus
            text_width = game_over_text.boundingRect().width()
            text_x = (self.width() - text_width) / 2 # Keskittää vaakasuunassa
            game_over_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2) # Asetetaan pystysuunassa

            #Asetetaan peli uudelleenaloitustilaan
            self.game_started = False
            return


        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 1 # Laskuri pisteiden laskentaan
            self.food = self.spawn_food() # Uuden ruokapallon ilmestyminen

            if self.score == self.level_limit: # Vaikeustason asetukset
                self.level_limit += 5
                self.timer_delay -= 50
                self.timer.setInterval(self.timer_delay)
        else:
            self.snake.pop()

        self.print_game()
        


    #Uusi metodi pallojen luomiseen
    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            #Varmistaa ettei pallot ilmesty madon päälle
            if (x, y) not in self.snake:
                return x, y


    def print_game(self):
        self.scene().clear()

        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.yellow))

        # Piirretään pallot
        fx, fy = self.food
        self.scene().addText(f'Pisteet: {self.score}', QFont('Arial', 12))
        self.scene().addRect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.red))
        
    def start_game(self):

        #Vaikeustasot
        self.level_limit = 5
        self.timer_delay = 300
        self.timer.start(self.timer_delay)


        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.food = self.spawn_food() # luodaan pallot
        self.timer.start(300)
        
        self.print_game()
        self.score = 0
        



# Main-metodi
def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
