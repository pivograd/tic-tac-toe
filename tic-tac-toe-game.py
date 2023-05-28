import random
import sys

import pygame


def set_game_settings():
    global current_player, current_move, empty_cells, cells_with_x, cells_with_o, playing_field, screen_size, cell_size, corner_cells

    screen_size = 800
    cell_size = screen_size // 3

    current_player = 'X'  # изменить на выбор первого хода, путём нажатия на кнопку

    current_move = 1
    empty_cells = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    cells_with_x = []
    cells_with_o = []
    corner_cells = [(0, 0), (2, 0), (0, 2), (2, 2)]
    playing_field = [['0,0', '0,1', '0,2'],
                     ['1,0', '1,1', '1,2'],
                     ['2,0', '2,1', '2,2']]


def create_game():
    global screen, font

    screen = pygame.display.set_mode((screen_size, screen_size + 100))
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Крестики-Нолики')
    font = pygame.font.SysFont('Arial', screen_size // 7)

    pygame.draw.line(surface=screen, color=(0, 0, 0), start_pos=(0, cell_size), end_pos=(screen_size, cell_size),
                     width=3)
    pygame.draw.line(surface=screen, color=(0, 0, 0), start_pos=(0, cell_size * 2),
                     end_pos=(screen_size, cell_size * 2),
                     width=3)
    pygame.draw.line(surface=screen, color=(0, 0, 0), start_pos=(cell_size, 0), end_pos=(cell_size, screen_size),
                     width=3)
    pygame.draw.line(surface=screen, color=(0, 0, 0), start_pos=(cell_size * 2, 0),
                     end_pos=(cell_size * 2, screen_size),
                     width=3)

    button_color = (60, 60, 60)
    button_rect = pygame.Rect(0, screen_size, screen_size, 100)
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Новая игра", True, (0, 0, 0))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)


def reset_game():
    global current_player, current_move, empty_cells, cells_with_x, cells_with_o, playing_field
    current_player = 'X'
    current_move = 1
    empty_cells = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    cells_with_x = []
    cells_with_o = []
    playing_field = [['0,0', '0,1', '0,2'],
                     ['1,0', '1,1', '1,2'],
                     ['2,0', '2,1', '2,2']]

    screen.fill((255, 255, 255))

    pygame.draw.line(surface=screen, color=(0, 0, 0), start_pos=(0, cell_size), end_pos=(screen_size, cell_size),
                     width=3)
    pygame.draw.line(surface=screen, color=(0, 0, 0), start_pos=(0, cell_size * 2),
                     end_pos=(screen_size, cell_size * 2), width=3)
    pygame.draw.line(surface=screen, color=(0, 0, 0), start_pos=(cell_size, 0), end_pos=(cell_size, screen_size),
                     width=3)
    pygame.draw.line(surface=screen, color=(0, 0, 0), start_pos=(cell_size * 2, 0),
                     end_pos=(cell_size * 2, screen_size), width=3)

    button_color = (60, 60, 60)
    button_rect = pygame.Rect(0, screen_size, screen_size, 100)
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Новая игра", True, (0, 0, 0))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)


def display_message(message):
    text_surface = font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_size // 2, screen_size // 3)
    screen.blit(text_surface, text_rect)


def make_move(position):
    if position[0] <= cell_size:
        center_x = cell_size // 2
        column_index = 0
    elif position[0] <= cell_size * 2:
        center_x = cell_size // 2 + cell_size
        column_index = 1
    else:
        center_x = cell_size // 2 + cell_size * 2
        column_index = 2

    if position[1] <= cell_size:
        center_y = cell_size // 2
        row_index = 0
    elif position[1] <= cell_size * 2:
        center_y = cell_size // 2 + cell_size
        row_index = 1
    else:
        center_y = cell_size // 2 + cell_size * 2
        row_index = 2

    if (column_index, row_index) not in empty_cells:
        raise ValueError
    else:
        pygame.draw.line(surface=screen, color=(0, 0, 0),
                         start_pos=(center_x - screen_size // 9, center_y - screen_size // 9),
                         end_pos=(center_x + screen_size // 9, center_y + screen_size // 9),
                         width=5)
        pygame.draw.line(surface=screen, color=(0, 0, 0),
                         start_pos=(center_x + screen_size // 9, center_y - screen_size // 9),
                         end_pos=(center_x - screen_size // 9, center_y + screen_size // 9),
                         width=5)

        empty_cells.remove((column_index, row_index))
        cells_with_x.append((column_index, row_index))
        playing_field[column_index][row_index] = current_player


def get_the_best_move():
    if current_move == 1:
        cell = (1, 1)
        return cell

    if current_move == 2:
        if (1, 1) not in cells_with_x:
            cell = (1, 1)
            return cell
        else:
            cell = random.choice(corner_cells)
            return cell

    if current_move == 3:
        for cell_ in corner_cells:
            if cell_ in cells_with_x:
                if cell_[0] == 0:
                    index_1 = 2
                else:
                    index_1 = 0
                if cell_[1] == 0:
                    index_2 = 2
                else:
                    index_2 = 0
                cell = (index_1, index_2)
                return cell
        cell = random.choice(corner_cells)
        return cell

    if current_move == 4:
        if (1, 1) in cells_with_o:
            if (0, 0) in cells_with_x and (2, 2) in cells_with_x:
                cell = random.choice(corner_cells)
                return cell
            elif (0, 2) in cells_with_x and (2, 0) in cells_with_x:
                cell = random.choice(corner_cells)
                return cell
            else:
                if cells_with_x[0][0] == cells_with_x[1][0] and cells_with_x[0][0] != 1:
                    for i in range(3):
                        if cells_with_x[0][1] != i and cells_with_x[1][1] != i:
                            cell = (cells_with_x[0][0], i)
                            return cell
                elif cells_with_x[0][1] == cells_with_x[1][1] and cells_with_x[0][1] != 1:
                    for i in range(3):
                        if cells_with_x[0][0] != i and cells_with_x[1][0] != i:
                            cell = (i, cells_with_x[0][1])
                            return cell
                else:
                    for cell_ in corner_cells:
                        if cell_ in cells_with_x:
                            if cell_[0] == 0:
                                index_1 = 2
                            else:
                                index_1 = 0
                            if cell_[1] == 0:
                                index_2 = 2
                            else:
                                index_2 = 0
                            cell = (index_1, index_2)
                            return cell
                    if abs(cells_with_x[0][0] - cells_with_x[1][0]) == 1 and abs(
                            cells_with_x[0][1] - cells_with_x[1][1]) == 1:
                        if cells_with_x[0][0] == cells_with_x[1][1] and cells_with_x[0][1] == cells_with_x[1][0]:
                            cell = random.choice([(2, 0), (0, 2)])
                            return cell
                        else:
                            cell = random.choice([(2, 2), (0, 0)])
                            return cell
                    else:
                        cell = random.choice(corner_cells)
                        return cell

        else:
            if cells_with_x[0][0] == cells_with_x[1][0]:
                for i in range(3):
                    if cells_with_x[0][1] != i and cells_with_x[1][1] != i:
                        cell = (cells_with_x[0][0], i)
                        return cell
            elif cells_with_x[0][1] == cells_with_x[1][1]:
                for i in range(3):
                    if cells_with_x[0][0] != i and cells_with_x[1][0] != i:
                        cell = (i, cells_with_x[0][1])
                        return cell
            else:
                for cell_ in cells_with_x:
                    if cell_ == (1, 1):
                        pass
                    else:
                        if abs(cells_with_o[0][0] - cell_[0]) == 2 and abs(cells_with_o[0][1] - cell_[1]) == 2:
                            intersection = [cell_ for cell_ in corner_cells if cell_ in empty_cells]
                            cell = random.choice(intersection)
                            return cell
                        else:
                            if cell_[0] == 0:
                                index_1 = 2
                            else:
                                index_1 = 0
                            if cell_[1] == 0:
                                index_2 = 2
                            else:
                                index_2 = 0
                            cell = (index_1, index_2)
                            return cell

    if current_move == 5:
        for cell_ in cells_with_o:
            if cell_ == (1, 1):
                pass
            else:
                if cell_[0] == 0:
                    index_1 = 2
                else:
                    index_1 = 0
                if cell_[1] == 0:
                    index_2 = 2
                else:
                    index_2 = 0
                if (index_1, index_2) not in cells_with_x:
                    cell = (index_1, index_2)
                    return cell

        if cells_with_x[0][0] == cells_with_x[1][0]:
            for i in range(3):
                if cells_with_x[0][1] != i and cells_with_x[1][1] != i:
                    cell = (cells_with_x[0][0], i)
                    return cell
        elif cells_with_x[0][1] == cells_with_x[1][1]:
            for i in range(3):
                if cells_with_x[0][0] != i and cells_with_x[1][0] != i:
                    cell = (i, cells_with_x[0][1])
                    return cell
        else:
            intersection = [cell_ for cell_ in corner_cells if cell_ in empty_cells]
            cell_x = [cell_x for cell_x in cells_with_x if cell_x not in corner_cells]
            for cell in intersection:
                if abs(cell[0] - cell_x[0][0]) == 2 or abs(cell[1] - cell_x[0][1]) == 2:
                    return cell

    if current_move == 6:

        if cells_with_o[0][0] == cells_with_o[1][0]:
            for i in range(3):
                if cells_with_o[0][1] != i and cells_with_o[1][1] != i:
                    cell = (cells_with_o[0][0], i)
                    if cell in empty_cells:
                        return cell
        elif cells_with_o[0][1] == cells_with_o[1][1]:
            for i in range(3):
                if cells_with_o[0][0] != i and cells_with_o[1][0] != i:
                    cell = (i, cells_with_o[0][1])
                    if cell in empty_cells:
                        return cell

        for cell_ in cells_with_x:
            for cell_1 in cells_with_x:
                if cell_ == cell_1:
                    pass
                else:
                    if cell_[0] == cell_1[0]:
                        for i in range(3):
                            if cell_[1] != i and cell_1[1] != i:
                                cell = (cell_[0], i)
                                if cell in empty_cells:
                                    return cell

                    elif cell_[1] == cell_1[1]:
                        for i in range(3):
                            if cell_[0] != i and cell_1[0] != i:
                                cell = (i, cell_[1])
                                if cell in empty_cells:
                                    return cell

        for cell_ in cells_with_o:
            if cell_ in corner_cells:
                cells = [cel for cel in empty_cells if cel in corner_cells]
                cel_g = (abs(cell_[0] - 2), abs(cell_[1] - 2))
                for cel in cells:
                    if cel != cel_g:
                        return cel

    if current_move == 7:

        cells_y = [cell for cell in cells_with_o if cell != (1, 1)]
        if cells_y[0][0] == cells_y[1][0]:
            for i in range(3):
                if cells_y[0][1] != i and cells_y[1][1] != i:
                    cell = (cells_y[0][0], i)
                    if cell in empty_cells:
                        return cell
        elif cells_y[0][1] == cells_y[1][1]:
            for i in range(3):
                if cells_y[0][0] != i and cells_y[1][0] != i:
                    cell = (i, cells_y[0][1])
                    if cell in empty_cells:
                        return cell
        else:
            for cell_ in cells_y:
                if cell_[0] == 1:
                    if cell_[1] == 0:
                        cell = (1, 2)
                        if cell in empty_cells:
                            return cell
                    else:
                        cell = (1, 0)
                        if cell in empty_cells:
                            return cell
                if cell_[1] == 1:
                    if cell_[0] == 0:
                        cell = (2, 1)
                        if cell in empty_cells:
                            return cell
                    else:
                        cell = (0, 1)
                        if cell in empty_cells:
                            return cell

        for cell_ in corner_cells:
            if cell_ in empty_cells:
                return cell_

    if current_move == 8:

        for cell_ in cells_with_o:
            for cell_1 in cells_with_o:
                if cell_ == cell_1:
                    pass
                else:
                    if cell_[0] == cell_1[0]:
                        for i in range(3):
                            if cell_[1] != i and cell_1[1] != i:
                                cell = (cell_[0], i)
                                if cell in empty_cells:
                                    return cell

                    elif cell_[1] == cell_1[1]:
                        for i in range(3):
                            if cell_[0] != i and cell_1[0] != i:
                                cell = (i, cell_[1])
                                if cell in empty_cells:
                                    return cell

        for cell_ in cells_with_x:
            for cell_1 in cells_with_x:
                if cell_ == cell_1:
                    pass
                else:
                    if cell_[0] == cell_1[0]:
                        for i in range(3):
                            if cell_[1] != i and cell_1[1] != i:
                                cell = (cell_[0], i)
                                if cell in empty_cells:
                                    return cell

                    elif cell_[1] == cell_1[1]:
                        for i in range(3):
                            if cell_[0] != i and cell_1[0] != i:
                                cell = (i, cell_[1])
                                if cell in empty_cells:
                                    return cell

        for cell_ in cells_with_o:
            if cell_ in corner_cells:
                cells = [cel for cel in empty_cells if cel in corner_cells]
                cel_g = (abs(cell_[0] - 2), abs(cell_[1] - 2))
                for cel in cells:
                    if cel != cel_g:
                        return cel

    if current_move == 9:
        cell = empty_cells[0]
        return cell


def make_computer_move():
    best_move = get_the_best_move()

    try:
        if best_move[0] == 0:
            center_x = cell_size // 2
            column_index = 0
        elif best_move[0] == 1:
            center_x = cell_size // 2 + cell_size
            column_index = 1
        else:
            center_x = cell_size // 2 + cell_size * 2
            column_index = 2

        if best_move[1] == 0:
            center_y = cell_size // 2
            row_index = 0
        elif best_move[1] == 1:
            center_y = cell_size // 2 + cell_size
            row_index = 1
        else:
            center_y = cell_size // 2 + cell_size * 2
            row_index = 2

        pygame.draw.circle(surface=screen, color=(0, 0, 0), center=(center_x, center_y), radius=screen_size // 9,
                           width=5)
        empty_cells.remove((column_index, row_index))
        cells_with_o.append((column_index, row_index))
        playing_field[column_index][row_index] = current_player

    except:
        pass


def game_is_over():
    if playing_field[0][0] == playing_field[0][1] and playing_field[0][0] == playing_field[0][2]:
        return True
    elif playing_field[1][0] == playing_field[1][1] and playing_field[1][0] == playing_field[1][2]:
        return True
    elif playing_field[2][0] == playing_field[2][1] and playing_field[2][0] == playing_field[2][2]:
        return True
    elif playing_field[0][0] == playing_field[1][0] and playing_field[0][0] == playing_field[2][0]:
        return True
    elif playing_field[0][1] == playing_field[1][1] and playing_field[0][1] == playing_field[2][1]:
        return True
    elif playing_field[0][2] == playing_field[1][2] and playing_field[0][2] == playing_field[2][2]:
        return True
    elif playing_field[0][0] == playing_field[1][1] and playing_field[0][0] == playing_field[2][2]:
        return True
    elif playing_field[0][2] == playing_field[1][1] and playing_field[0][2] == playing_field[2][0]:
        return True
    else:
        return False


def main():
    global current_player, current_move

    pygame.init()

    set_game_settings()
    create_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if current_player == 'X':
                    try:
                        make_move(pygame.mouse.get_pos())
                        if game_is_over():
                            display_message(f'Победил {current_player}')
                        current_player = 'O'
                        current_move += 1
                    except ValueError:
                        pass

            if current_player == 'O':
                make_computer_move()
                if game_is_over():
                    display_message(f'Победил {current_player}')
                current_player = 'X'
                current_move += 1
            if current_move > 9:
                display_message('НИЧЬЯ!')
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[1] > screen_size:
                    reset_game()

            pygame.display.flip()


if __name__ == '__main__':
    main()
