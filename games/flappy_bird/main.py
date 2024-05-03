import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

from user_db import *

def run_game(game_id: int, user_id: int):
    pygame.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird Game v1.0.2")
    img = pygame.image.load('games/flappy_bird/assets/icons/red_bird.png')
    pygame.display.set_icon(img)
    clock = pygame.time.Clock()
    column_create_event = pygame.USEREVENT
    running = True
    gameover = False
    gamestarted = False

    assets.load_sprites()
    assets.load_audios()

    sprites = pygame.sprite.LayeredUpdates()

    def create_sprites():
        Background(0, sprites)
        Background(1, sprites)
        Floor(0, sprites)
        Floor(1, sprites)
        return Bird(sprites), GameStartMessage(sprites), Score(sprites)

    bird, game_start_message, score = create_sprites()
    show_game_over_message = False

    # Добавляем переменную для отслеживания события завершения игры
    game_over_event = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == column_create_event:
                Column(sprites)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                    gamestarted = True
                    game_start_message.kill()
                    pygame.time.set_timer(column_create_event, 1500)
                if event.key == pygame.K_ESCAPE and gameover:
                    gameover = False
                    gamestarted = False
                    show_game_over_message = False
                    sprites.empty()
                    bird, game_start_message, score = create_sprites()

            if not gameover:
                bird.handle_event(event)

        screen.fill(0)
        sprites.draw(screen)

        if gamestarted and not gameover:
            sprites.update()

        if bird.check_collision(sprites) and not gameover:
            game_over_event = True  # Устанавливаем флаг события завершения игры
            gameover = True
            gamestarted = False
            show_game_over_message = True
            pygame.time.set_timer(column_create_event, 0)
            assets.play_audio("hit")

        if show_game_over_message:
            font = pygame.font.Font(None, 32)
            highest_score = get_score(user_id, game_id)
            print(score.value, highest_score)  # перемещаем сюда
            text = ''
            if score.value > highest_score:
                text = font.render(f"New highest score {score.value}!", True, (255, 255, 255))
                update_score(user_id, game_id, score.value)
            else:
                text = font.render(f"Game over.", True, (255, 255, 255))
            text_rect = text.get_rect(center=(configs.SCREEN_WIDTH // 2, configs.SCREEN_HEIGHT // 3))
            screen.blit(text, text_rect)

            # Добавляем сообщение о перезапуске игры
            font = pygame.font.Font(None, 24)
            restart_text = font.render("Press ESC to restart", True, (255, 255, 255))
            restart_text_rect = restart_text.get_rect(
                center=(configs.SCREEN_WIDTH // 2, configs.SCREEN_HEIGHT // 3 + 50))
            screen.blit(restart_text, restart_text_rect)

            # Обработка событий только если игра завершена
            while game_over_event:
                pygame.display.flip()
                clock.tick(configs.FPS)
                for ev in pygame.event.get():
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                        game_over_event = False  # Сбрасываем флаг события завершения игры
                        show_game_over_message = False
                        gameover = False
                        gamestarted = False
                        sprites.empty()
                        bird, game_start_message, score = create_sprites()


        for sprite in sprites:
            if type(sprite) is Column and sprite.is_passed():
                score.value += 1
                assets.play_audio("point")

        pygame.display.flip()
        clock.tick(configs.FPS)

    pygame.quit()


def run_flappy_bird(game_id: int, user_id: int):
    run_game(game_id, user_id)
