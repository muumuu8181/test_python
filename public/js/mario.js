const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const GRAVITY = 0.5;
const FRICTION = 0.8;
const JUMP_FORCE = -10;
const SPEED = 4;
const TILE_SIZE = 40;

class Entity {
    constructor(x, y, width, height, color) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.color = color;
        this.vx = 0;
        this.vy = 0;
        this.markedForDeletion = false;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
    }

    draw(ctx, scrollX) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x - scrollX, this.y, this.width, this.height);
    }

    getBounds() {
        return {
            left: this.x,
            right: this.x + this.width,
            top: this.y,
            bottom: this.y + this.height
        };
    }

    checkCollision(other) {
        const a = this.getBounds();
        const b = other.getBounds();
        return (
            a.left < b.right &&
            a.right > b.left &&
            a.top < b.bottom &&
            a.bottom > b.top
        );
    }
}

class Player extends Entity {
    constructor(x, y) {
        super(x, y, 30, 30, '#ff0000'); // Red Mario
        this.grounded = false;
        this.isDead = false;
        this.win = false;
    }

    update(input, blocks, enemies) {
        if (this.isDead || this.win) return;

        // Horizontal Movement
        if (input.keys.ArrowRight) {
            this.vx = SPEED;
        } else if (input.keys.ArrowLeft) {
            this.vx = -SPEED;
        } else {
            this.vx *= FRICTION;
        }

        // Jump
        if (input.keys.ArrowUp && this.grounded) {
            this.vy = JUMP_FORCE;
            this.grounded = false;
        } else if (input.keys.Space && this.grounded) { // Alternative jump key
             this.vy = JUMP_FORCE;
             this.grounded = false;
        }

        // Apply Physics
        this.vy += GRAVITY;
        this.x += this.vx;
        this.checkHorizontalCollisions(blocks);
        this.y += this.vy;
        this.grounded = false;
        this.checkVerticalCollisions(blocks);

        // Screen boundary (left)
        if (this.x < 0) this.x = 0;

        // Check Fall Death
        if (this.y > canvas.height) {
            this.isDead = true;
        }

        // Check Enemy Collisions
        enemies.forEach(enemy => {
            if (this.checkCollision(enemy)) {
                // Stomp check: Player must be falling and above the enemy
                if (this.vy > 0 && this.y + this.height - this.vy <= enemy.y + enemy.height * 0.5) {
                    enemy.markedForDeletion = true;
                    this.vy = JUMP_FORCE * 0.5; // Bounce
                } else {
                    this.isDead = true;
                }
            }
        });
    }

    checkHorizontalCollisions(blocks) {
        for (const block of blocks) {
            if (this.checkCollision(block)) {
                if (this.vx > 0) {
                    this.x = block.x - this.width;
                } else if (this.vx < 0) {
                    this.x = block.x + block.width;
                }
                this.vx = 0;
            }
        }
    }

    checkVerticalCollisions(blocks) {
        for (const block of blocks) {
            if (this.checkCollision(block)) {
                if (this.vy > 0) {
                    this.y = block.y - this.height;
                    this.grounded = true;
                    this.vy = 0;
                } else if (this.vy < 0) {
                    this.y = block.y + block.height;
                    this.vy = 0;
                }
            }
        }
    }

    draw(ctx, scrollX) {
        if (this.isDead) return;
        super.draw(ctx, scrollX);
        // Add simple eyes to look like a face
        ctx.fillStyle = '#fff';
        if (this.vx >= 0) {
             ctx.fillRect(this.x - scrollX + 20, this.y + 5, 5, 5);
        } else {
             ctx.fillRect(this.x - scrollX + 5, this.y + 5, 5, 5);
        }
    }
}

class Enemy extends Entity {
    constructor(x, y) {
        super(x, y, 30, 30, '#8b4513'); // Brown Goomba
        this.vx = -2;
        this.patrolStart = x;
    }

    update(blocks) {
        this.vy += GRAVITY;
        this.x += this.vx;

        // Simple horizontal collision for turning around
        for (const block of blocks) {
             if (this.checkCollision(block)) {
                if (this.vx > 0) {
                    this.x = block.x - this.width;
                    this.vx *= -1;
                } else if (this.vx < 0) {
                    this.x = block.x + block.width;
                    this.vx *= -1;
                }
             }
        }

        this.y += this.vy;
        let grounded = false;
        // Vertical collision
        for (const block of blocks) {
            if (this.checkCollision(block)) {
                if (this.vy > 0) {
                    this.y = block.y - this.height;
                    this.vy = 0;
                    grounded = true;
                }
            }
        }

        // Turn around at edges if grounded
        // (Simplified AI: just patrol back and forth for now, or just move until wall)
    }
}

class Block extends Entity {
    constructor(x, y, type) {
        let color = '#a0522d'; // Ground
        if (type === '?') color = '#ffd700'; // Gold block
        if (type === 'P') color = '#008000'; // Pipe
        if (type === 'G') color = '#ffdf00'; // Goal pole

        super(x, y, TILE_SIZE, TILE_SIZE, color);
        this.type = type;

        if (type === 'P') {
            this.height = TILE_SIZE * 2;
            this.y -= TILE_SIZE; // Adjust position for height
        }
        if (type === 'G') {
            this.height = TILE_SIZE * 8;
            this.y -= TILE_SIZE * 7;
            this.width = 10;
        }
    }
}

class InputHandler {
    constructor() {
        this.keys = {};
        window.addEventListener('keydown', e => {
            this.keys[e.code] = true;
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(e.code)) {
                e.preventDefault();
            }
            if (e.code === 'KeyR') {
                game.restart();
            }
        });
        window.addEventListener('keyup', e => {
            this.keys[e.code] = false;
        });
    }
}

class Game {
    constructor() {
        this.input = new InputHandler();
        this.restart();
    }

    restart() {
        this.player = null;
        this.blocks = [];
        this.enemies = [];
        this.particles = [];
        this.cameraX = 0;
        this.levelWidth = 0;
        this.loadLevel(level1);
        this.gameOver = false;
        this.gameWon = false;
    }

    loadLevel(layout) {
        layout.forEach((row, rowIndex) => {
            [...row].forEach((symbol, colIndex) => {
                const x = colIndex * TILE_SIZE;
                const y = rowIndex * TILE_SIZE;

                if (symbol === '#') {
                    this.blocks.push(new Block(x, y, '#'));
                } else if (symbol === '?') {
                    this.blocks.push(new Block(x, y, '?'));
                } else if (symbol === 'P') {
                    this.blocks.push(new Block(x, y, 'P'));
                } else if (symbol === 'M') {
                    this.player = new Player(x, y);
                } else if (symbol === 'E') {
                    this.enemies.push(new Enemy(x, y));
                } else if (symbol === 'G') {
                    this.blocks.push(new Block(x, y, 'G'));
                }
            });
            this.levelWidth = row.length * TILE_SIZE;
        });
    }

    update() {
        if (!this.player) return;

        if (this.player.isDead) {
            this.gameOver = true;
            return;
        }

        // Check win condition
        const goal = this.blocks.find(b => b.type === 'G');
        if (goal && this.player.checkCollision(goal)) {
            this.gameWon = true;
            this.player.win = true;
            return;
        }

        this.player.update(this.input, this.blocks, this.enemies);
        this.enemies.forEach(enemy => enemy.update(this.blocks));
        this.enemies = this.enemies.filter(enemy => !enemy.markedForDeletion);

        // Camera follow
        this.cameraX = this.player.x - canvas.width / 4;
        if (this.cameraX < 0) this.cameraX = 0;
        if (this.cameraX > this.levelWidth - canvas.width) this.cameraX = this.levelWidth - canvas.width;
    }

    draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw background elements (clouds, hills could be added here)

        this.blocks.forEach(block => block.draw(ctx, this.cameraX));
        this.enemies.forEach(enemy => enemy.draw(ctx, this.cameraX));
        if (this.player) this.player.draw(ctx, this.cameraX);

        // UI
        if (this.gameOver) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#fff';
            ctx.font = '40px "Press Start 2P"';
            ctx.textAlign = 'center';
            ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2);
            ctx.font = '20px "Press Start 2P"';
            ctx.fillText('Press R to Restart', canvas.width / 2, canvas.height / 2 + 50);
        } else if (this.gameWon) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#ffdf00';
            ctx.font = '40px "Press Start 2P"';
            ctx.textAlign = 'center';
            ctx.fillText('COURSE CLEAR!', canvas.width / 2, canvas.height / 2);
            ctx.font = '20px "Press Start 2P"';
            ctx.fillText('Press R to Play Again', canvas.width / 2, canvas.height / 2 + 50);
        }
    }
}

const level1 = [
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                   ???                                                                 G            ",
    "                                       ???      ?                                      #            ",
    "                                              # # #                                    #            ",
    "         E                 E                 # # # #                                   #            ",
    "        ###    P     ####    P     ####     # # # # #                                  #            ",
    "              ###           ###            # # # # # #                                 #            ",
    "M            #####         #####          # # # # # # #                                #            ",
    "####################################################################################################",
    "####################################################################################################"
];

const game = new Game();

function animate() {
    game.update();
    game.draw();
    requestAnimationFrame(animate);
}

animate();
