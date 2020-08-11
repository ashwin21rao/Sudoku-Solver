import pygame
import numpy as np

pygame.init()
clock = pygame.time.Clock()
font_large = pygame.font.Font("extras/OpenSans-Bold.ttf", 25)
font_small = pygame.font.Font("extras/OpenSans-Bold.ttf", 20)
screen_width = 600
screen_height = 600
side_length = 405
margin = (screen_width - side_length) / 2
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku")
icon = pygame.image.load("extras/icon.png")
pygame.display.set_icon(icon)

COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (92, 92, 92)
COLOR_ACTIVE = (40, 111, 156)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)


def clear(values, mask):
    values[np.logical_not(mask)] = 0


def solve(array, i, j, cells, mask, start_time):
    if j > 8:
        j = 0
        i += 1
    if i > 8:
        return True
    if array[i, j] != 0:
        return solve(array, i, j + 1, cells, mask, start_time)

    active_cell = cells[i][j]
    for value in range(1, 10):
        array[i, j] = value

        drawBoard(cells, array, mask, active_cell, start_time, True)
        drawButtons()
        pygame.display.flip()
        pygame.time.delay(5)

        if validCell(array, i, j, value):
            if solve(array, i, j + 1, cells, mask, start_time):
                return True

    array[i, j] = 0
    return False


def validCell(array, i, j, value):
    return np.count_nonzero(array[i, :] == value) == 1 and \
           np.count_nonzero(array[:, j] == value) == 1 and \
           np.count_nonzero(array[i // 3 * 3: i // 3 * 3 + 3, j // 3 * 3: j // 3 * 3 + 3] == value) == 1


def sudokuValues(game_number):
    data = np.loadtxt("games.txt", delimiter=", ", dtype=np.int).reshape((-1, 9, 9))
    array = data[game_number]
    mask = (array != 0)
    return array, mask


def updateTime(start_time):
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    time = ""

    for i in range(3):
        if current_time > 0:
            value = "0" + str(current_time % 60) if (current_time % 60) < 10 else str(current_time % 60)
            time = ":" + value + time
            current_time //= 60
        else:
            time = (":00" if i != 2 else "00") + time

    return time


def getCells():
    cell_side = side_length / 9
    cells = [[pygame.Rect(0, 0, 0, 0) for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            cells[i][j] = pygame.Rect(margin + cell_side * j, margin + cell_side * i, cell_side, cell_side)

    return cells


def drawButtons():
    new_game_text = font_small.render("New Game", False, (255, 0, 0))
    new_game_button = new_game_text.get_rect(bottomleft=(margin, margin))
    screen.blit(new_game_text, new_game_button)

    solve_text = font_small.render("Solve", False, (0, 255, 0))
    solve_button = solve_text.get_rect(topleft=(margin, margin + side_length))
    screen.blit(solve_text, solve_button)

    clear_text = font_small.render("Clear", False, (0, 0, 255))
    clear_button = clear_text.get_rect(topright=(screen_width - margin, margin + side_length))
    screen.blit(clear_text, clear_button)

    return {"new game": new_game_button,
            "solve": solve_button,
            "clear": clear_button}


def drawBoard(cells, values, mask, active_cell, start_time, solving=False):
    screen.fill((255, 255, 255))

    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            pygame.draw.rect(screen, (125, 130, 130), cell, 1)

            if values[i, j] != 0:
                if mask[i, j]:
                    text = font_large.render(str(values[i, j]), False, COLOR_BLACK)
                else:
                    text = font_large.render(str(values[i, j]), False, COLOR_GRAY
                                             if not solving and validCell(values, i, j, values[i, j])
                                             else COLOR_GREEN if solving and validCell(values, i, j, values[i, j])
                                             else COLOR_RED)

                center = text.get_rect(center=cell.center)
                screen.blit(text, center)

    pygame.draw.rect(screen, COLOR_BLACK, (margin, margin, side_length, side_length), 4)
    for i in range(1, 3):
        pygame.draw.line(screen, COLOR_BLACK, (margin, margin + side_length * i / 3),
                         (margin + side_length, margin + side_length * i / 3), 3)
        pygame.draw.line(screen, COLOR_BLACK, (margin + side_length * i / 3, margin),
                         (margin + side_length * i / 3, margin + side_length), 3)

    if active_cell:
        pygame.draw.rect(screen, COLOR_ACTIVE, active_cell, 3)

    time = updateTime(start_time)
    time_text = font_large.render(time, False, COLOR_BLACK)
    pos = time_text.get_rect(bottomright=(screen_width - margin, margin))
    screen.blit(time_text, pos)


def initializeGame(game_number):
    values, mask = sudokuValues(game_number)
    original_array = values.copy()
    solved_array = values.copy()
    return values, mask, original_array, solved_array


def gameloop():
    start_time = pygame.time.get_ticks()
    game_number = 0
    total_games = 5

    cells = getCells()
    active_cell = None
    active_cell_index = None
    values, mask, original_array, solved_array = initializeGame(game_number)

    running = True
    while running:

        drawBoard(cells, values, mask, active_cell, start_time)
        buttons = drawButtons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if '1' <= chr(event.key) <= '9' and active_cell:
                    if not mask[active_cell_index]:
                        values[active_cell_index] = chr(event.key)
                if (event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE) and active_cell:
                    if not mask[active_cell_index]:
                        values[active_cell_index] = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, row in enumerate(cells):
                    for j, cell in enumerate(row):
                        if cell.collidepoint(event.pos[0], event.pos[1]):
                            active_cell = cell
                            active_cell_index = (i, j)
                if buttons["solve"].collidepoint(event.pos[0], event.pos[1]):
                    solve(solved_array, 0, 0, cells, mask, start_time)
                    values = solved_array.copy()
                    solved_array = original_array.copy()
                if buttons["clear"].collidepoint(event.pos[0], event.pos[1]):
                    clear(values, mask)
                if buttons["new game"].collidepoint(event.pos[0], event.pos[1]):
                    start_time = pygame.time.get_ticks()
                    game_number = (game_number + 1) % total_games
                    values, mask, original_array, solved_array = initializeGame(game_number)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


gameloop()
