import subprocess, pygame

clock = pygame.time.Clock()


def run_spim():
    # Launch our file in spim and hijack STDOUT and STDIN
    spim = subprocess.Popen(['spim', '-file', 'tetris.s'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)

    # Just read in the first several lines which are all copyright info
    s = spim.stdout.readline()
    s = spim.stdout.readline()
    s = spim.stdout.readline()
    s = spim.stdout.readline()
    s = spim.stdout.readline()
    s = spim.stdout.readline()
    spim.stdout.flush()

    # This loop is just temporary to make sure the handoff is working correctly
    x = 1
    while x < 6:
        print s

        # Strip out our new line
        s = s.rstrip()
        final = ''

        # Convert each character in our string to an integer, increment it and write it to the pipe
        for c in s:
            i = int(c)
            i = i + 1
            c = str(i) + '\n'
            spim.stdin.write(c)

        # Send a 9 to spim to let it know we are done
        spim.stdin.write('9\n')

        # Wait for a response from SPIM
        s = spim.stdout.readline()
        spim.stdout.flush()

        x = x + 1


def init_pygame():
    pygame.init()

    size = width, height = 320, 640

    screen = pygame.display.set_mode(size)
    return screen

def main_loop():
    while True:
        clock.tick(60);

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print "goodbye"
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                print "right arrow hit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                print "left arrow hit"


if __name__ == "__main__":
    run_spim()
    init_pygame()
    main_loop()

