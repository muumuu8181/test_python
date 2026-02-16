import unittest
import sys
from unittest.mock import MagicMock
sys.modules['curses'] = MagicMock()

from shooting_game import Bullet, Enemy, Boss, PowerUp, Player, check_collision

class TestShootingGameLogic(unittest.TestCase):
    def test_collision(self):
        b = Bullet(10, 10, -1)
        e = Enemy(10, 10, 1)
        self.assertTrue(check_collision(b, e))

    def test_boss_inheritance(self):
        boss = Boss(10, 0)
        self.assertIsInstance(boss, Enemy)
        self.assertEqual(boss.hp, 50)

    def test_powerup_collision(self):
        p = Player(10, 10)
        pu = PowerUp(10, 10)
        self.assertTrue(check_collision(p, pu))

    def test_player_shoot_powerup(self):
        p = Player(10, 10)
        bullets = p.shoot()
        self.assertEqual(len(bullets), 1)

        p.power = 2
        bullets = p.shoot()
        self.assertEqual(len(bullets), 3)

if __name__ == '__main__':
    unittest.main()
