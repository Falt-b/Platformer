import pygame


def get_image(
    original_image: pygame.Surface,
    row: int,
    col: int,
    width: int,
    height: int,
    color_key: tuple = (0, 0, 0),
):
    new_img = pygame.Surface((width, height))
    new_img.set_colorkey(color_key)
    new_img.blit(
        original_image,
        (0, 0),
        (col * width, row * height, (col * width) + width, (row * height) + height),
    )
    return new_img


def load_animation(
    sprite_sheet: str,
    row: int,
    col: int,
    stop: int,
    width: int,
    height: int,
    color_key: tuple = (0, 0, 0),
):
    return [
        get_image(
            pygame.image.load(sprite_sheet), row, col + i[1], width, height, color_key
        )
        for i in enumerate(range(stop - col))
    ]


class State():
    def __init__(self, state: str, start_frame: int, hold: bool, num_frames: int, interrupt: bool, interrupt_states: list[str]):
        self.state = state
        self.start_frame = start_frame
        self.current_frame = start_frame
        self.hold = hold
        self.num_frames = num_frames
        self.interrupt = interrupt
        self.interrupt_states = interrupt_states

class Animator():
    def __init__(self, cooldown: int):
        self.cooldown = cooldown
        self.last_update = 0

        self.animation_index = {}
        self.last_state = None
        self.current_state = None
        self.requested_state = None

    def init_state(
        self,
        state: str,
        sprite_sheet: str,
        row: int,
        col: int,
        stop: int,
        width: int,
        height: int,
        color_key: tuple = (0, 0, 0),
    ):
        self.animation_index[state] = load_animation(
            sprite_sheet, row, col, stop, width, height, color_key
        )

    def update_frame(self):
        ct = pygame.time.get_ticks()
        if ct - self.last_update < self.cooldown:
            return False
        self.last_update = ct
        return True

    def switch_states(self):
        # checks if a frame is needed to be held
        if not self.current_state.hold:
            self.last_state = self.current_state
            self.current_state = self.requested_state
            return
        # if held for required frames go to requested state
        if self.current_state.num_frames > 0:
            self.last_state = self.current_state
            self.current_state = self.requested_state
            return
        # check if interrupt can be done
        if not self.current_state.interrupt:
            return
        # check if requested state can interrupt current state
        if self.requested_state.state in self.current_state.interrupt_states:
            self.last_state = self.current_state
            self.current_state = self.requested_state
            return

    def update(self):
        if self.update_frame():
            self.switch_states()
        else:
            return self.last_state
        self.current_state.current_frame += 1
        if self.current_state.hold:
            self.current_state.num_frames -= 1
            self.current_state.current_frame = self.current_state.start_frame
        if self.frame > len(self.animation_index[self.current_state.state]) - 1:
            self.frame = 0
        return self.last_state

    def get_frame(self):
        if self.current_state.current_frame > len(self.animation_index[self.current_state.state]) - 1:
            self.current_state.current_frame = 0
        return self.animation_index[self.current_state.state][self.current_state.current_frame]




# class Animator:
#     def __init__(self, cooldown: int):
#         self.cooldown = cooldown
#         self.last_update = 0

#         self.frame = 0
#         self.current_state = None
#         self.last_state = None
#         self.animation_index = {}

#         self.hold = False
#         self.hold_frame = 0
#         self.hold_state = None
#         self.next_states = []
#         self.timer = 0
#         self.time = 0

#         self.requested_state = []

#     def init_state(
#         self,
#         state: str,
#         sprite_sheet: str,
#         row: int,
#         col: int,
#         stop: int,
#         width: int,
#         height: int,
#         color_key: tuple = (0, 0, 0),
#     ):
#         self.animation_index[state] = load_animation(
#             sprite_sheet, row, col, stop, width, height, color_key
#         )

#     def request_state(
#         self, state: str, hold: bool, frame: int, time: int, next_states: list[str]
#     ):
#         self.requested_state = [state, hold, frame, time, next_states]

#     def update_frame(self):
#         ct = pygame.time.get_ticks()
#         if ct - self.last_update < self.cooldown:
#             return self.last_state
#         self.current_state = self.requested_state[0]

#         if self.requested_state[1] and not self.hold:
#             self.hold = True
#             self.hold_state = self.requested_state[0]
#             self.hold_frame = self.requested_state[2]
#             self.next_states = self.requested_state[4]
#             self.timer = self.requested_state[3]
#             self.time = 0

#         self.last_update = ct
#         self.frame += 1
#         self.time += 1

#         if self.frame > len(self.animation_index[self.current_state]) - 1:
#             self.frame = 0

#         if self.hold:
#             self.state = self.hold_state
#             self.frame = self.hold_frame
#         if self.time > self.timer:
#             self.hold = False
#         if (
#             self.hold
#             and self.current_state != self.hold_state
#             and self.current_state not in self.next_states
#         ):
#             self.hold = False

#         self.last_state = self.current_state
#         return self.last_state

#     def get_frame(self):
#         if self.frame > len(self.animation_index[self.current_state]) - 1:
#             self.frame = 0
#         return self.animation_index[self.current_state][self.frame]
