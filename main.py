from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint

Window.size = (800, 600)

CHICKEN_SIZE = (50, 50)
CAR_SIZE = (100, 50)

class Chicken(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 0)
            self.rect = Rectangle(pos=(Window.width/2, 0), size=CHICKEN_SIZE)
        self.size = CHICKEN_SIZE
        self.pos = self.rect.pos

    def move(self, direction):
        x, y = self.rect.pos
        if direction == "up":
            y += 10
        elif direction == "down":
            y -= 10
        elif direction == "left":
            x -= 10
        elif direction == "right":
            x += 10
        x = max(0, min(Window.width - self.width, x))
        y = max(0, min(Window.height - self.height, y))
        self.rect.pos = (x, y)

class Car(Widget):
    def __init__(self, y_pos, speed, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 0, 0)
            self.rect = Rectangle(pos=(randint(-200, -50), y_pos), size=CAR_SIZE)
        self.speed = speed
        self.size = CAR_SIZE

    def move(self):
        x, y = self.rect.pos
        x += self.speed
        if x > Window.width:
            x = randint(-200, -50)
        self.rect.pos = (x, y)

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chicken = Chicken()
        self.add_widget(self.chicken)

        self.cars = [Car(y, randint(4, 8)) for y in range(100, 500, 100)]
        for car in self.cars:
            self.add_widget(car)

        Clock.schedule_interval(self.update, 1.0/60.0)

    def on_touch_up(self, touch):
        x, y = touch.pos
        cx, cy = self.chicken.rect.pos
        if abs(x - cx) > abs(y - cy):
            if x > cx:
                self.chicken.move("right")
            else:
                self.chicken.move("left")
        else:
            if y > cy:
                self.chicken.move("up")
            else:
                self.chicken.move("down")

    def update(self, dt):
        for car in self.cars:
            car.move()
            if self.chicken.rect.collide_widget(car):
                print("Game Over")
                self.reset_game()

        if self.chicken.rect.pos[1] >= Window.height - CHICKEN_SIZE[1]:
            print("You Win!")
            self.reset_game()

    def reset_game(self):
        self.chicken.rect.pos = (Window.width / 2, 0)

class ChickenRoadApp(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    ChickenRoadApp().run()
