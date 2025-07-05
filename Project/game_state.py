import pygame

def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.click(pygame.mouse.get_pos()) == True:
                    print("Start button clicked")
                    game()
                if settings_button.click(pygame.mouse.get_pos()) == True:
                    print("Settings button clicked")
                if quit_button.click(pygame.mouse.get_pos()) == True:
                    pygame.quit()

        screen.blit(menu_background_surface,(0,0))

        start_button.update()
        settings_button.update()
        quit_button.update()

        start_button.change_color(pygame.mouse.get_pos())
        settings_button.change_color(pygame.mouse.get_pos())
        quit_button.change_color(pygame.mouse.get_pos())

        pygame.display.update()

def game():
    while True:
        for i in GRID[0]:
            if i == 1:
                print("Game Over")
                game_over()

        current_time = pygame.time.get_ticks() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    print("Escape button clicked")
                    pause()
        screen.blit(GRID_BACKGROUND, (WIDTH_OFFSET, HEIGHT_OFFSET))
        draw_shape(current_shape, current_pos[0], current_pos[1])
        draw_next_shape(next_shape)
        movement(current_shape)
        drop_shape(current_shape)
        draw_final_shape()
        remove_rows()
        info_bar()

        column(COLUMNS)
        row(ROWS)
        rotate()
        pygame.display.update()
        clock.tick(120)

def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if p_home_button.click(pygame.mouse.get_pos()) == True:
                    print("Home button clicked")
                if p_resume_button.click(pygame.mouse.get_pos()) == True:
                    print("Resume button clicked")
                if p_restart_button.click(pygame.mouse.get_pos()) == True:
                    print("Restart button clicked")
                if p_settings_button.click(pygame.mouse.get_pos()) == True:
                    print("Settings button clicked")

    p_home_button.update()
    p_resume_button.update()
    p_restart_button.update()
    p_settings_button.update()

    pygame.display.update()

def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if g_home_button.click(pygame.mouse.get_pos()) == True:
                    print("Home button clicked")
                    menu()
                if g_restart_button.click(pygame.mouse.get_pos()) == True:
                    print("Restart button clicked")
                    game()
        g_home_button.update()
        g_restart_button.update()

        pygame.display.update()
