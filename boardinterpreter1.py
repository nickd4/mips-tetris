import subprocess, pygame, random

clock = pygame.time.Clock()
#spim = subprocess.Popen(['spim', '-file', 'tetris.s'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)
spim = subprocess.Popen(['../emu_mips_alt', 'tetris.hex'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)

PROMPT_TICK  = "1\n"
PROMPT_PIECE = "8\n"
END_GAME     = "9\n"

MOVE_LEFT  = "1\n"
MOVE_RIGHT = "2\n"
ROTATE     = "3\n"
DO_NOTHING = "4\n"

PIPE_PIECE   = "1\n"
SQUARE_PIECE = "2\n"
Z_PIECE      = "3\n"
BZ_PIECE     = "4\n"
L_PIECE      = "5\n"
BL_PIECE     = "6\n"
T_PIECE      = "7\n"

PIECES = [PIPE_PIECE, SQUARE_PIECE, Z_PIECE, BZ_PIECE, T_PIECE, BL_PIECE]
#PIECES = [L_PIECE]

BLACK = pygame.Color(0,0,0)
RED   = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE  = pygame.Color(0,0,255)
ORANGE = pygame.Color(255,165,0)
PURPLE = pygame.Color(160,32,240)
YELLOW = pygame.Color(255,255,0)
CYAN = pygame.Color(0,255,255)

WIDTH  = 320
HEIGHT = 640

def run_spim():
     # Launch our file in spim and hijack STDOUT and STDIN

    # Just read in the first several lines which are all copyright info
    #s = spim.stdout.readline()
    #s = spim.stdout.readline()
    #s = spim.stdout.readline()
    #s = spim.stdout.readline()
    #s = spim.stdout.readline()
    pass

def init_pygame():
    pygame.init()
    pygame.display.init()
    pygame.display.set_caption("MIPS Tetris!")
    size = WIDTH, HEIGHT

    screen = pygame.display.set_mode(size)


def main_loop():
    while True:
        clock.tick(8)
        data = spim.stdout.readline()
        print "data: ",data
        spim.stdout.flush()

        tick_event = DO_NOTHING      # Our default

        if data == PROMPT_PIECE:
            print "prompted for piece"
            spim.stdin.write(random.choice(PIECES))

        if data == PROMPT_TICK:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "goodbye"
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print "goodbye"
                        return
                    elif event.key == pygame.K_RIGHT:
                        print "right arrow hit"
                        tick_event = MOVE_RIGHT
                    elif event.key == pygame.K_LEFT:
                        print "left arrow hit"
                        tick_event = MOVE_LEFT
                    elif event.key == pygame.K_UP:
                        print "up arrow hit"
                        tick_event = ROTATE

            print "ticking"
            print "sending: " + tick_event
            spim.stdin.write(tick_event)

        if data == END_GAME:
            print "game ending"
            while True:
                clock.tick(8)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print "goodbye"
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print "goodbye"
                            return

        if len(data) == 129:
            for x in range(0,16):
                for y in range(0,8):
                    d = data[x * 8 + y]
                    if d == "0":
                        display_block(x,y, BLACK)
                    elif d == "1":
                        display_block(x,y, RED)
                    elif d == "2":
                        display_block(x,y, GREEN)
                    elif d == "3":
                        display_block(x,y, BLUE)
                    elif d == "4":
                        display_block(x,y, ORANGE)
                    elif d == "5":
                        display_block(x,y, PURPLE)
                    elif d == "6":
                        display_block(x,y, YELLOW)
                    elif d == "7":
                        display_block(x,y, CYAN)

        pygame.display.update()


def display_block(r,c, color):
    BLOCK_X = WIDTH / 8
    BLOCK_Y = HEIGHT / 16
    BORDER_SIZE = 5

    left = c * BLOCK_X
    top = r * BLOCK_Y

    surface = pygame.display.get_surface()

    rect = pygame.Rect(left + BORDER_SIZE, top + BORDER_SIZE, BLOCK_X - BORDER_SIZE, BLOCK_Y - BORDER_SIZE)
    surface.fill(color, rect)


if __name__ == "__main__":
    run_spim()
    init_pygame()
    main_loop()
    print "terminating spim subprocess..."
    spim.terminate()
