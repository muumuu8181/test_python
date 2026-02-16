import curses
import random
import time

class Bullet:
    def __init__(self, x, y, dy, dx=0, char='|'):
        self.x = x
        self.y = y
        self.dy = dy
        self.dx = dx
        self.char = char

    def update(self):
        self.y += self.dy
        self.x += self.dx

    def draw(self, stdscr):
        try:
            if self.y >= 0:
                stdscr.addch(int(self.y), int(self.x), self.char)
        except curses.error:
            pass

class Enemy:
    def __init__(self, x, y, dy, hp=1, char='V'):
        self.x = x
        self.y = y
        self.dy = dy
        self.hp = hp
        self.char = char

    def update(self, max_x):
        self.y += self.dy

    def draw(self, stdscr):
        try:
            if self.y >= 0:
                stdscr.addch(int(self.y), int(self.x), self.char)
        except curses.error:
            pass

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 0.1, hp=50, char='W')
        self.move_dir = 1
        self.move_timer = 0
        self.shoot_timer = 0

    def update(self, max_x):
        self.y += self.dy

        if self.y > 5:
            self.dy = 0

        self.move_timer += 1
        if self.move_timer > 5:
            self.x += self.move_dir
            self.move_timer = 0
            if self.x <= 2 or self.x >= max_x - 3:
                self.move_dir *= -1

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0.5
        self.char = 'P'

    def update(self):
        self.y += self.dy

    def draw(self, stdscr):
        try:
            stdscr.addch(int(self.y), int(self.x), self.char)
        except curses.error:
            pass

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 5
        self.chars = ['.', 'o', 'O', '@', '*']

    def update(self):
        self.life -= 1

    def draw(self, stdscr):
        if self.life > 0:
            char = self.chars[min(len(self.chars)-1, self.life)]
            try:
                stdscr.addch(int(self.y), int(self.x), char)
            except curses.error:
                pass

class Player:
    def __init__(self, x, y, char='^'):
        self.x = x
        self.y = y
        self.char = char
        self.power = 1
        self.bombs = 2

    def move(self, dx, dy, max_x, max_y):
        self.x = max(0, min(max_x - 1, self.x + dx))
        self.y = max(0, min(max_y - 1, self.y + dy))

    def shoot(self):
        bullets = []
        bullets.append(Bullet(self.x, self.y - 1, -1, 0, '|'))
        if self.power >= 2:
            bullets.append(Bullet(self.x - 1, self.y - 1, -1, -0.3, '/'))
            bullets.append(Bullet(self.x + 1, self.y - 1, -1, 0.3, '\\'))
        return bullets

    def draw(self, stdscr):
        try:
            stdscr.addch(int(self.y), int(self.x), self.char)
        except curses.error:
            pass

def check_collision(obj1, obj2):
    return int(obj1.x) == int(obj2.x) and int(obj1.y) == int(obj2.y)

def draw_title(stdscr, sh, sw):
    stdscr.clear()
    title = "ULTIMATE PYTHON SHOOTER"
    try:
        stdscr.addstr(sh // 2 - 2, sw // 2 - len(title) // 2, title, curses.A_BOLD)
        msg = "Press SPACE to Start"
        stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
    except curses.error:
        pass
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord(' '):
            return True
        elif key == ord('q'):
            return False
        time.sleep(0.05)

def draw_gameover(stdscr, sh, sw, score):
    stdscr.clear()
    msg = "GAME OVER"
    try:
        stdscr.addstr(sh // 2 - 2, sw // 2 - len(msg) // 2, msg, curses.A_BOLD)
        score_msg = f"Final Score: {score}"
        stdscr.addstr(sh // 2, sw // 2 - len(score_msg) // 2, score_msg)
        retry_msg = "Press SPACE to Restart or 'q' to Quit"
        stdscr.addstr(sh // 2 + 2, sw // 2 - len(retry_msg) // 2, retry_msg)
    except curses.error:
        pass
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord(' '):
            return True
        elif key == ord('q'):
            return False
        time.sleep(0.05)

def game_loop(stdscr, sh, sw):
    player = Player(sw // 2, sh - 2)
    bullets = []
    enemies = []
    powerups = []
    explosions = []

    score = 0
    lives = 3
    level = 1
    enemies_spawned = 0
    boss_spawned = False

    enemy_spawn_timer = 0

    running = True
    while running:
        stdscr.clear()

        # Spawn enemies
        if not boss_spawned:
            enemy_spawn_timer += 1
            if enemy_spawn_timer > max(5, 25 - level * 2):
                enemies.append(Enemy(random.randint(1, sw - 2), 0, 0.2 + random.random() * 0.1 * level, hp=1 + level//2))
                enemies_spawned += 1
                enemy_spawn_timer = 0

            if enemies_spawned > 10 * level and len(enemies) == 0:
                boss = Boss(sw // 2, -3)
                enemies.append(boss)
                boss_spawned = True

        # Update entities
        player.draw(stdscr)

        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(stdscr)
            if bullet.y < 0 or bullet.y >= sh or bullet.x < 0 or bullet.x >= sw:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.update(sw)
            enemy.draw(stdscr)
            if enemy.y >= sh:
                enemies.remove(enemy)

            # Collision with Player
            if check_collision(player, enemy):
                lives -= 1
                explosions.append(Explosion(enemy.x, enemy.y))
                enemies.remove(enemy)
                if isinstance(enemy, Boss):
                    boss_spawned = False
                    enemies_spawned = 0
                    level += 1
                    score += 500

                if lives <= 0:
                    running = False

        # Collision: Bullets vs Enemies
        for bullet in bullets[:]:
            hit = False
            for enemy in enemies[:]:
                if check_collision(bullet, enemy):
                    enemy.hp -= 1
                    hit = True
                    explosions.append(Explosion(bullet.x, bullet.y))
                    if enemy.hp <= 0:
                        if enemy in enemies: enemies.remove(enemy)
                        score += 10 * level
                        explosions.append(Explosion(enemy.x, enemy.y))
                        if isinstance(enemy, Boss):
                            score += 1000
                            level += 1
                            enemies_spawned = 0
                            boss_spawned = False
                            lives += 1
                        elif random.random() < 0.1:
                            powerups.append(PowerUp(enemy.x, enemy.y))
                    break
            if hit:
                bullets.remove(bullet)

        # Update and Draw PowerUps
        for pu in powerups[:]:
            pu.update()
            pu.draw(stdscr)
            if pu.y >= sh:
                powerups.remove(pu)
            elif check_collision(player, pu):
                player.power = min(3, player.power + 1)
                powerups.remove(pu)
                score += 50
                player.bombs = min(5, player.bombs + 1)

        # Update and Draw Explosions
        for exp in explosions[:]:
            exp.update()
            exp.draw(stdscr)
            if exp.life <= 0:
                explosions.remove(exp)

        # UI
        try:
            stdscr.addstr(0, 0, f"Score: {score} | Lives: {lives} | Level: {level} | Bombs: {player.bombs}")
            if boss_spawned:
                 stdscr.addstr(0, sw - 10, "BOSS!!", curses.A_BLINK)
            stdscr.addstr(1, 0, "Move: Arrows | Shoot: Space | Bomb: 'b' | Quit: 'q'")
        except curses.error:
            pass

        stdscr.refresh()

        # Input Handling
        key = stdscr.getch()

        if key == ord('q'):
            return score # Quit game but show score? Or just exit? Let's show score.
            # running = False
        elif key == curses.KEY_LEFT:
            player.move(-1, 0, sw, sh)
        elif key == curses.KEY_RIGHT:
            player.move(1, 0, sw, sh)
        elif key == curses.KEY_UP:
            player.move(0, -1, sw, sh)
        elif key == curses.KEY_DOWN:
            player.move(0, 1, sw, sh)
        elif key == ord(' '):
            bullets.extend(player.shoot())
        elif key == ord('b'):
            if player.bombs > 0:
                player.bombs -= 1
                for e in enemies[:]:
                    e.hp -= 10
                    explosions.append(Explosion(e.x, e.y))
                    if e.hp <= 0:
                        enemies.remove(e)
                        score += 10
                        if isinstance(e, Boss):
                            score += 1000
                            level += 1
                            enemies_spawned = 0
                            boss_spawned = False
                            lives += 1

        time.sleep(0.02)

    return score

def main(stdscr):
    # Initial Setup
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50)

    sh, sw = stdscr.getmaxyx()

    if not draw_title(stdscr, sh, sw):
        return

    while True:
        score = game_loop(stdscr, sh, sw)
        if not draw_gameover(stdscr, sh, sw, score):
            break

if __name__ == "__main__":
    curses.wrapper(main)
