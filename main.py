import pygame
import pygame.freetype
from pygame.locals import *
from button import SpriteButton
import color
from windows import QuizWindow, ResultWindow, TitleWindow
from questions import QUESTIONS, RESULTS
import questions

pygame.mixer.init()  # Initialize the mixer for sound
pygame.font.init()  # Initialize the font module
pygame.init()


pygame.mixer.music.load("sounds/dargolan-elevator.mp3")
pygame.mixer.music.set_volume(0.3)  # Set the volume to 50%
pygame.mixer.music.play(-1)  # Play the music indefinitely



width, height = 800, 600
pygame.display.set_caption("What type of music are you?")  # Set the window title

FPS = 60


screen = pygame.display.set_mode((width, height), RESIZABLE)  # Create a resizable window

window = TitleWindow(width, height)
quiz_windows = []
current_question_index = None

def restart():
    global window
    global current_question_index
    global quiz_windows
    
    current_question_index = None
    quiz_windows.clear()  # Clear the list of quiz windows
    window = TitleWindow(width, height)  # Reset to the title window
    window.on_start(on_start)  # Re-register the start callback

    # Reset the music from channel 1
    pygame.mixer.Channel(1).stop()  # Stop the music on channel 1
    pygame.mixer.music.stop()  # Stop the music
    pygame.mixer.music.play(-1)  # Restart the music





def prev_question():
    global window
    global current_question_index
    global quiz_windows
    if current_question_index is not None and current_question_index > 0:
        current_question_index -= 1
        window = quiz_windows[current_question_index] 
        window.resize(width, height)  # Resize the existing window

def next_question():
    global window
    global current_question_index
    if current_question_index is not None and current_question_index < len(QUESTIONS) - 1:
        current_question_index += 1

        if current_question_index < len(quiz_windows):
            # If the quiz window for the current question already exists, reuse it
            window = quiz_windows[current_question_index]
            window.resize(width, height)  # Resize the existing window
        else:
            window = QuizWindow(width, height, QUESTIONS[current_question_index], current_question_index)
            window.on_next(next_question)  # Register the next question callback
            window.on_prev(prev_question)
            quiz_windows.append(window)  # Add the new quiz window to the list


    elif current_question_index == len(QUESTIONS) - 1:
        responses = [quiz_window.selected_choice for quiz_window in quiz_windows]
        result = questions.get_result(responses)
        window = ResultWindow(width, height, result)
        window.on_restart(restart)

def on_start():
    global window
    global current_question_index
    current_question_index = 0 
    quiz_window = QuizWindow(width, height, QUESTIONS[0], current_question_index)
    quiz_window.on_next(next_question)
    quiz_windows.append(quiz_window)
    window = quiz_windows[0]  # Transition to the first quiz window

    # Here you can add the logic to start the quiz or transition to the next screen

window.on_start(on_start)  # Set the callback for the start button
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == VIDEORESIZE:
            width, height = event.w, event.h
            window.resize(width, height)

            
    window.show(screen)  # Show the title window



    if  window.register_mouse_events(pygame.mouse):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else: 
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    pygame.display.update()  # Update the display
    pygame.time.Clock().tick(FPS)  # Maintain the frame rate
