# ex14-main

from dataclasses import dataclass, field
import pygame

FPS = 60

ROW = 3  # ROWを変えたらCOLORSも変えるべし。
COL = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTBLUE = (157, 204, 224)
COLORS = [(240, 67, 90), (143, 201, 70), (0, 123, 193)]

state = 0
difficulty = 1

score = 0
del_count = 0
life_point = 3
first = True


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float

    def draw(self):
        self.move()
        return pygame.draw.circle(screen, WHITE, (self.x, self.y), 5, width=0)

    def move(self):
        self.wall_collision()
        self.x += self.vx
        self.y += self.vy

    def wall_collision(self):
        global life_point
        if self.x < 0 or self.x > screen.get_width():
            self.vx = -self.vx
        if self.y < 0 or self.y > screen.get_height():
            self.vy = -self.vy
            if self.y > screen.get_height():
                life_point -= 1


@dataclass
class Block:
    x: int
    y: int
    breaking: bool
    color: tuple


@dataclass
class Paddle:
    x: float
    y: float
    vx: float
    width: int

    def draw(self, left, right):
        self.move(left, right)
        return pygame.draw.rect(screen, LIGHTBLUE, (int(self.x), int(self.y), self.width, 10), width=0)

    def move(self, left, right):
        if left:
            self.x -= self.vx
        if right:
            self.x += self.vx


@dataclass
class Text:
    center_x: int
    center_y: int
    font_size: int
    color: tuple

    # @return texts: list = [text, text_rect]
    # blitで使えるようなtextと座標を返す。
    def make_text(self, word, justify="center"):
        texts = []

        font = pygame.font.Font("UDDigiKyokashoN-R.ttc", self.font_size)
        text = font.render(word, True, self.color)
        text_rect = text.get_rect()
        if justify == "center":
            text_rect.center = (self.center_x, self.center_y)
        elif justify == "top-left":
            text_rect.topleft = (self.center_x, self.center_y)
        elif justify == "top-right":
            text_rect.topright = (self.center_x, self.center_y)

        texts.append(text)
        texts.append(text_rect)
        return texts


@dataclass
class Button:
    x: int
    y: int
    width: int
    height: int

    # @return buttons: list = [rect, [text, text_rect]]
    # Rectを作って、真ん中の座標を指定し、ボタン内テキストを書けるようにして入れ子配列を返す。
    def make_button(self, center_x, center_y, word):
        buttons = []

        button = pygame.Rect((self.x, self.y, self.width, self.height))
        button.center = (center_x, center_y)
        buttons.append(button)

        text = Text(center_x, center_y, 24, WHITE).make_text(word)
        buttons.append(text)

        return buttons


@dataclass
class MainMenu:
    start: list = field(init=False, default_factory=list)
    difficulty: list = field(init=False, default_factory=list)
    end: list = field(init=False, default_factory=list)

    click: bool = field(init=False, default=False)
    mouse_x: int = field(init=False, default=0)
    mouse_y: int = field(init=False, default=0)

    def setup(self):
        self.start = Button(50, 50, 200, 50).make_button(300, 250, "Start")
        self.difficulty = Button(50, 50, 200, 50).make_button(300, 350, "Difficulty")
        self.end = Button(50, 50, 200, 50).make_button(300, 450, "Quit")

    def draw_menu(self):
        global state, difficulty, first

        screen.fill(BLACK)

        if self.start[0].collidepoint(self.mouse_x, self.mouse_y):
            state = 1
            self.click = False
            self.mouse_x = 0
            self.mouse_y = 0
            first = True
        elif self.difficulty[0].collidepoint(self.mouse_x, self.mouse_y):
            if 1 <= difficulty < 3:
                difficulty += 1
            else:
                difficulty = 1
            self.click = False
            self.mouse_x = 0
            self.mouse_y = 0
        elif self.end[0].collidepoint(self.mouse_x, self.mouse_y):
            exit()

        title = Text(300, 100, 48, WHITE).make_text("ブロック崩し ver.2")

        dif_text = ""
        if difficulty == 1:
            dif_text = "easy"
        elif difficulty == 2:
            dif_text = "normal"
        elif difficulty == 3:
            dif_text = "hard"
        dif_texts = Text(350, 150, 24, WHITE).make_text("difficulty: " + dif_text, "top-left")

        screen.blit(title[0], title[1])
        screen.blit(dif_texts[0], dif_texts[1])

        for button in [self.start, self.difficulty, self.end]:
            pygame.draw.rect(screen, WHITE, button[0], width=4)
            screen.blit(button[1][0], button[1][1])


@dataclass
class Breakout:
    k_up: bool = field(init=False, default=False)
    k_down: bool = field(init=False, default=False)
    k_left: bool = field(init=False, default=False)
    k_right: bool = field(init=False, default=False)
    mode: int = field(init=False, default=0)
    ball: pygame.Rect = field(init=False, default=None)
    paddle: pygame.Rect = field(init=False, default=None)
    line: pygame.Rect = field(init=False, default=None)
    blocks: list = field(init=False, default_factory=list)

    ball_c: Ball = field(init=False, default=None)
    paddle_c: Paddle = field(init=False, default=None)

    del_all = True
    block_width = 0
    text = Text(10, 10, 24, WHITE)
    del_txt = Text(590, 10, 24, WHITE)
    life = Text(300, 25, 24, WHITE)

    def setup(self):
        vx = 2 * difficulty
        vy = 3 * difficulty
        width = 35 * 3 / difficulty
        self.ball_c = Ball(300, 300, vx, vy)
        self.paddle_c = Paddle(400, 500, 8, int(width))
        self.line = pygame.draw.rect(screen, WHITE, (0, 50, 600, 2), width=0)
        self.make_blocks()

    def draw_breakout(self):
        global del_count, score, life_point, state, first
        if first:
            self.setup()
            first = False

        screen.fill(BLACK)
        score_text = self.text.make_text(f"スコア: {score}", "top-left")
        del_text = self.del_txt.make_text(f"全消し: {del_count}", "top-right")
        life_text = self.life.make_text(f"残機: {life_point}", "center")
        self.ball = self.ball_c.draw()
        self.paddle = self.paddle_c.draw(self.k_left, self.k_right)

        pygame.draw.rect(screen, WHITE, (0, 50, 600, 2), width=0)
        screen.blit(score_text[0], score_text[1])
        screen.blit(del_text[0], del_text[1])
        screen.blit(life_text[0], life_text[1])

        for blocks in self.blocks:
            for block in blocks:
                if not block.breaking:
                    self.del_all = False
                    block_c = pygame.draw.rect(screen, block.color, (block.x + 2.5, block.y, self.block_width - 5, 15), width=0)
                    if self.ball.colliderect(block_c):
                        self.ball_c.vy = -self.ball_c.vy
                        score += 10 * difficulty
                        block.breaking = True

        if self.del_all:
            self.make_blocks()
            self.del_all = True
            del_count += 1
            life_point += 1
            score += 100 * del_count * difficulty
            self.ball_c.y = 200
            self.ball_c.vy += .1 * difficulty
            self.ball_c.vx += .1 * difficulty
        else:
            self.del_all = True

        if self.ball.colliderect(self.paddle):
            self.ball_c.vy = -self.ball_c.vy
        if self.ball.colliderect(self.line):
            self.ball_c.vy = -self.ball_c.vy

        if life_point < 0:
            state = 2

    def make_blocks(self):
        self.blocks = []
        self.block_width = screen.get_width() / COL

        for i in range(ROW):
            block = []
            for j in range(COL):
                x = self.block_width * j
                y = 55 + (i * 15) + i * 5
                block.append(Block(int(x), int(y), False, COLORS[i]))
            self.blocks.append(block)


@dataclass
class QuitMenu:
    gameOver_text = Text(300, 200, 72, WHITE)
    score_text = Text(300, 300, 32, WHITE)
    all_text = Text(300, 400, 32, WHITE)
    goTitle = Text(580, 540, 14, WHITE)
    click = False

    def draw_quit(self):
        global state, score, del_count, life_point
        screen.fill(BLACK)
        go_text = self.gameOver_text.make_text("Game Over!")
        sc_text = self.score_text.make_text(f"スコア: {score}")
        a_text = self.all_text.make_text(f"全消し回数: {del_count}")
        gt_text = self.goTitle.make_text("画面クリックでタイトルに戻る...", "top-right")
        screen.blit(go_text[0], go_text[1])
        screen.blit(sc_text[0], sc_text[1])
        screen.blit(a_text[0], a_text[1])
        screen.blit(gt_text[0], gt_text[1])
        if self.click:
            state = 0
            score = 0
            del_count = 0
            life_point = 3
            self.click = False


@dataclass
class Main:
    menu: MainMenu = field(init=False, default=None)
    breakout: Breakout = field(init=False, default=None)
    quitMenu: QuitMenu = field(init=False, default=None)

    is_exit: bool = field(init=False, default=False)

    def start_game(self):
        self.menu = MainMenu()
        self.breakout = Breakout()
        self.quitMenu = QuitMenu()

        self.menu.setup()

        while not self.is_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.breakout.k_right = True
                    if event.key == pygame.K_LEFT:
                        self.breakout.k_left = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.breakout.k_right = False
                    if event.key == pygame.K_LEFT:
                        self.breakout.k_left = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if state == 0:
                        x, y = event.pos
                        self.menu.click = True
                        self.menu.mouse_x = x
                        self.menu.mouse_y = y
                    if state == 2:
                        self.quitMenu.click = True

            if state == 0:
                self.menu.draw_menu()
            elif state == 1:
                self.breakout.draw_breakout()
            elif state == 2:
                self.quitMenu.draw_quit()

            pygame.display.update()
            clock.tick(FPS)


pygame.font.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('ex14-main-ブロック崩し')

game = Main()
game.start_game()
