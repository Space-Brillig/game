import pygame
import sys
import pygame_gui
import objects.variables as variables

MANAGER = pygame_gui.UIManager((variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 600), (400, 50)), manager=MANAGER, object_id="#main_text_entry")

def Input():
    while True:
        framerate = variables.clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                return event.text
            
            MANAGER.process_events(event)
        
        MANAGER.update(framerate)

        MANAGER.draw_ui(variables.screen)

        pygame.display.update()