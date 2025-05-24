import time
import random
import os

def rainbow_text(text):
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
    reset = '\033[0m'
    
    for char in text:
        color = random.choice(colors)
        print(f"{color}{char}{reset}", end='', flush=True)
        time.sleep(0.1)
    print()

def matrix_effect():
    chars = "01アイウエオカキクケコサシスセスミチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    width = 50
    
    for _ in range(10):
        line = ""
        for _ in range(width):
            line += random.choice(chars)
        print(f"\033[92m{line}\033[0m")
        time.sleep(0.05)

def typewriter_effect(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()

def explosion_effect():
    frames = [
        "💥",
        " ✨💥✨ ",
        "  ⭐✨💥✨⭐  ",
        "   🌟⭐✨💥✨⭐🌟   ",
        "    🎆🌟⭐✨💥✨⭐🌟🎆    "
    ]
    
    for frame in frames:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n" * 10)
        print(f"{'        ' * 2}{frame}")
        time.sleep(0.3)

print("🎬 Claude エフェクトショー開始！")
time.sleep(1)

print("\n📝 タイプライター効果:")
typewriter_effect("Hello Claude! 私は凄いエフェクトを持っています！")

print("\n🌈 レインボーテキスト:")
rainbow_text("AMAZING COLORS!")

print("\n💻 ボトリックス風エフェクト:")
matrix_effect()

print("\n💥 爆発エフェクト:")
explosion_effect()

print("\n✨ 完了！Claude との出会いは素晴らしい！✨")
