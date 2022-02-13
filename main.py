from ghosts import Blinky, Pinky, Inky, Clyde, FRIGHTENED, CHASE, SCATTER, HOUSE
from load_data import field_background, screen_print, black
from logic import Field, LEFT, UP
from windows import main_menu
from pacman import Pacman
from time import sleep
import sqlite3
import pygame


size = width, height = 448, 576

pygame.init()

while True:
    old_screen = pygame.display.set_mode((800, 600))

    nick = main_menu(old_screen)

    del old_screen
    screen = pygame.display.set_mode(size)
    fps = 60
    speed = 2
    counter = 0
    animation_speed = fps // 20
    clock = pygame.time.Clock()
    level = 1
    escape = False

    field = Field(width, height)

    pacman = Pacman((224, 424), LEFT)
    blinky = Blinky((224, 232), LEFT)
    pinky = Pinky((224, 280), UP)
    inky = Inky((192, 280), UP)
    clyde = Clyde((256, 280), UP)

    pacman.set_field(field)
    blinky.set_field(field)
    pinky.set_field(field)
    inky.set_field(field)
    clyde.set_field(field)

    while level < 256:
        # Lo-ose
        if pacman.lives < 1:
            database = sqlite3.connect("./data/database.db")
            cursor = database.cursor()

            result = cursor.execute('''
                    SELECT nickname
                      FROM champions;
                    ''').fetchall()
            result = list(map(lambda x: str(x[0]), result))
            score = pacman.score

            if nick.lower() in result:
                result = cursor.execute(f'''
                SELECT score
                  FROM champions
                 WHERE nickname = "{nick.lower()}";
                ''').fetchall()[0][0]
                if result < score:
                    result = cursor.execute(f'''
                    UPDATE champions
                       SET score = {score}
                     WHERE nickname = "{nick}";
                    ''')
                    database.commit()
            else:
                result = cursor.execute(f'''
                INSERT INTO champions (
                                          nickname,
                                          score
                                      )
                                      VALUES (
                                          "{nick.lower()}",
                                          {score}
                                      );
                ''')
                database.commit()

            del pacman
            del blinky
            del pinky
            del inky

            del field

            field = Field(width, height)

            pacman = Pacman((224, 424), LEFT)
            blinky = Blinky((224, 232), LEFT)
            pinky = Pinky((224, 280), UP)
            inky = Inky((192, 280), UP)
            clyde = Clyde((256, 280), UP)

            pacman.set_field(field)
            blinky.set_field(field)
            pinky.set_field(field)
            inky.set_field(field)
            clyde.set_field(field)

            level = 1
        # Win?
        else:
            field.dead = False
            field.is_win = False

            pacman.position = 224, 424
            blinky.position = 224, 232
            pinky.position = 224, 280
            inky.position = 192, 280
            clyde.position = 256, 280

            pacman.set_field(field)
            blinky.set_field(field)
            pinky.set_field(field)
            inky.set_field(field)
            clyde.set_field(field)

            blinky.mode = HOUSE
            blinky.direction = UP
            inky.mode = HOUSE
            inky.direction = UP
            clyde.mode = HOUSE
            clyde.direction = UP

        pygame.display.set_caption(f"Pacman Classic ({nick}) {level} level")

        blinky.change_mode(SCATTER)

        blinky.counter = 7 * fps
        pinky.counter = 7 * fps
        inky.counter = 7 * fps
        clyde.counter = 7 * fps

        screen.fill(black)
        field_background.draw(screen)
        field.draw(screen)

        pacman.draw(screen)
        blinky.draw(screen)
        pinky.draw(screen)
        inky.draw(screen)
        clyde.draw(screen)

        screen_print(screen, "Ready!", (176, 320), (255, 255, 0, 255))
        screen_print(screen, "High Score", (144, 0), (255, 255, 255, 255))
        score = '00' if pacman.score == 0 else str(pacman.score)
        screen_print(screen, score,
                     ((7 - len(score)) * field.size[0], field.size[1]), (255, 255, 255, 255))

        width_, height_ = pacman.pacman.get_width(), pacman.pacman.get_height()

        for live in range(pacman.lives):
            pacman.pacman.move(live * field.size[0] * 2 + 3 * field.size[0] - width_ // 2,
                               35 * field.size[1] - height_ // 2)
            pacman.pacman.draw(screen)

        pygame.display.flip()
        counter = fps * 3  # 3 seconds

        while counter:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.K_ESCAPE:
                    escape = True
                    break

            if escape:
                break

            counter -= 1
            clock.tick(fps)

        if escape:
            break

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                        pacman.update(event.key)
                        pacman.time = 0
                    elif event.key == pygame.K_ESCAPE:
                        escape = True

            if escape:
                database = sqlite3.connect("./data/database.db")
                cursor = database.cursor()

                result = cursor.execute('''
                                    SELECT nickname
                                      FROM champions;
                                    ''').fetchall()
                result = list(map(lambda x: str(x[0]), result))
                score = pacman.score

                if nick.lower() in result:
                    result = cursor.execute(f'''
                                SELECT score
                                  FROM champions
                                 WHERE nickname = "{nick.lower()}";
                                ''').fetchall()[0][0]
                    if result < score:
                        result = cursor.execute(f'''
                                    UPDATE champions
                                       SET score = {score}
                                     WHERE nickname = "{nick}";
                                    ''')
                        database.commit()
                else:
                    result = cursor.execute(f'''
                                INSERT INTO champions (
                                                          nickname,
                                                          score
                                                      )
                                                      VALUES (
                                                          "{nick.lower()}",
                                                          {score}
                                                      );
                                ''')
                    database.commit()

                break

            screen.fill(black)
            field_background.draw(screen)
            field.draw(screen)

            width_, height_ = pacman.pacman.get_width(), pacman.pacman.get_height()

            for live in range(pacman.lives):
                pacman.pacman.move(live * field.size[0] * 2 + 3 * field.size[0] - width_ // 2,
                                   35 * field.size[1] - height_ // 2)
                pacman.pacman.draw(screen)

            # for y in range(field.height):
            #     for x in range(field.width):
            #         pygame.draw.rect(screen, 0xffffff,
            #                          (x * 16, y * 16,
            #                           16, 16), width=1)

            screen_print(screen, "High Score", (144, 0), (255, 255, 255, 255))
            score = '00' if pacman.score == 0 else str(pacman.score)
            screen_print(screen, score,
                         ((7 - len(score)) * field.size[0], field.size[1]), (255, 255, 255, 255))

            pacman.draw(screen)
            blinky.draw(screen)
            pinky.draw(screen)
            inky.draw(screen)
            clyde.draw(screen)

            if counter % animation_speed == 0:
                pacman.next()
                blinky.next()
                pinky.next()
                inky.next()
                clyde.next()

            pacman.forward(speed)

            pacman.pacman = pacman.pacman[pacman.direction]

            if blinky.mode != FRIGHTENED:
                blinky.ghost = blinky.ghost[blinky.direction]
            else:
                blinky.ghost = blinky.ghost[4 + ((counter % fps) // (fps // 4)) % 2]

            if pinky.mode != FRIGHTENED:
                pinky.ghost = pinky.ghost[pinky.direction]
            else:
                pinky.ghost = pinky.ghost[4 + ((counter % fps) // (fps // 4)) % 2]

            if inky.mode != FRIGHTENED:
                inky.ghost = inky.ghost[inky.direction]
            else:
                inky.ghost = inky.ghost[4 + ((counter % fps) // (fps // 4)) % 2]

            if clyde.mode != FRIGHTENED:
                clyde.ghost = clyde.ghost[inky.direction]
            else:
                clyde.ghost = clyde.ghost[4 + ((counter % fps) // (fps // 4)) % 2]

            pacman.time += 1

            blinky.update(pacman)
            pinky.update(pacman)
            inky.update(pacman, blinky)
            clyde.update(pacman)

            if blinky.mode == CHASE:
                blinky.counter -= 1
                if blinky.counter < 1:
                    blinky.change_mode(SCATTER)
                    blinky.counter = 7 * fps
            elif blinky.mode == SCATTER:
                blinky.counter -= 1
                if blinky.counter < 1:
                    blinky.change_mode(CHASE)
                    blinky.counter = 20 * fps
            elif blinky.mode == FRIGHTENED:
                blinky.counter -= 1
                if blinky.counter < 1:
                    blinky.change_mode(CHASE)
                    blinky.counter = 20 * fps

            if pinky.mode == CHASE:
                pinky.counter -= 1
                if pinky.counter < 1:
                    pinky.change_mode(SCATTER)
                    pinky.counter = 7 * fps
            elif pinky.mode == SCATTER:
                pinky.counter -= 1
                if pinky.counter < 1:
                    pinky.change_mode(CHASE)
                    pinky.counter = 20 * fps
            elif pinky.mode == FRIGHTENED:
                pinky.counter -= 1
                if pinky.counter < 1:
                    pinky.change_mode(CHASE)
                    pinky.counter = 20 * fps

            if inky.mode == CHASE:
                inky.counter -= 1
                if inky.counter < 1:
                    inky.change_mode(SCATTER)
                    inky.counter = 7 * fps
            elif inky.mode == SCATTER:
                inky.counter -= 1
                if inky.counter < 1:
                    inky.change_mode(CHASE)
                    inky.counter = 20 * fps
            elif inky.mode == FRIGHTENED:
                inky.counter -= 1
                if inky.counter < 1:
                    inky.change_mode(CHASE if inky.tmp else HOUSE)
                    inky.counter = 20 * fps

            if clyde.mode == CHASE:
                clyde.counter -= 1
                if clyde.counter < 1:
                    clyde.change_mode(SCATTER)
                    clyde.counter = 7 * fps
            elif clyde.mode == SCATTER:
                clyde.counter -= 1
                if clyde.counter < 1:
                    clyde.change_mode(CHASE)
                    clyde.counter = 20 * fps
            elif clyde.mode == FRIGHTENED:
                clyde.counter -= 1
                if clyde.counter < 1:
                    clyde.change_mode(CHASE if clyde.tmp else HOUSE)
                    clyde.counter = 20 * fps

            field.update(pacman, blinky, pinky, inky, clyde)

            pygame.display.flip()
            clock.tick(fps)

            counter = (counter + 1) % (fps ** 2)

            if field.is_win:
                field.is_win = False
                break
            elif field.dead:
                break

        if escape:
            break

        if field.dead:
            pacman.lives -= 1
            continue
        elif field.is_win:
            pacman.lives = 0

        sleep(3)

        level += 1

        del field
        field = Field(width, height)

    escape = False

    database = sqlite3.connect("./data/database.db")
    cursor = database.cursor()

    result = cursor.execute('''
        SELECT nickname
          FROM champions;
        ''').fetchall()

    if nick.lower() in result:
        result = cursor.execute(f'''
        SELECT score
          FROM champions
         WHERE nickname = "{nick.lower()}";
        ''').fetchall()[0][0]
        if result < score:
            result = cursor.execute(f'''
            UPDATE champions
               SET score = {score}
             WHERE nickname = "{nick}";
            ''')
            database.commit()
    else:
        result = cursor.execute(f'''
        INSERT INTO champions (
                                  nickname,
                                  score
                              )
                              VALUES (
                                  "{nick.lower()}",
                                  {score}
                              );
        ''')
        database.commit()

    del screen

    del field

    del pacman

    del blinky
    del pinky
    del inky
    del clyde
