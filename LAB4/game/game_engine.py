import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.score = 0
        self.total_attempts = 0

        # Streak system
        self.streak = 0

        # Timer settings
        self.time_limit = 10
        self.time_remaining = self.time_limit
        self.last_update_time = pygame.time.get_ticks()

        self.feedback_msg = "Solve the card and press Enter!"
        self.feedback_color = (200, 205, 215)

        self.num_a = 0
        self.num_b = 0
        self.operator = "+"

        # Input box
        box_w, box_h = 130, 44

        self.input_box = TextBox(
            width // 2 - 110,
            230,
            box_w,
            box_h
        )

        # Submit button
        self.submit_btn = pygame.Rect(
            width // 2 + 30,
            230,
            90,
            box_h
        )

        # Fonts
        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_card = pygame.font.SysFont(None, 56)
        self.font_btn = pygame.font.SysFont(None, 24)

        # Generate first question
        self.generate_new_card()

    def generate_new_card(self):
        """
        Generate a new arithmetic question.

        Division questions are generated so that the answer
        is always a clean integer with no remainder.
        """

        self.operator = random.choice(["+", "-", "*", "/"])

        if self.operator == "/":
            # Generate a clean division question
            self.num_b = random.randint(2, 12)

            quotient = random.randint(2, 12)

            self.num_a = self.num_b * quotient

        else:
            # Generate normal addition, subtraction,
            # and multiplication questions
            self.num_a = random.randint(3, 15)
            self.num_b = random.randint(2, 12)

            # Avoid negative subtraction results
            if self.operator == "-" and self.num_a < self.num_b:
                self.num_a, self.num_b = self.num_b, self.num_a

        # Clear previous answer
        self.input_box.clear()

        # Reset timer for the new question
        self.time_remaining = self.time_limit
        self.last_update_time = pygame.time.get_ticks()

    def compute_expected_answer(self):
        """
        Calculate the correct answer based on the operator.
        """

        if self.operator == "+":
            return self.num_a + self.num_b

        elif self.operator == "-":
            return self.num_a - self.num_b

        elif self.operator == "*":
            return self.num_a * self.num_b

        elif self.operator == "/":
            # Division questions are guaranteed
            # to have no remainder.
            return self.num_a // self.num_b

    def submit_answer(self):
        """
        Check the user's answer and update score/streak.
        """

        val_str = self.input_box.text.strip()

        if not val_str or val_str == "-":
            self.feedback_msg = "Type an answer first!"
            self.feedback_color = (240, 175, 40)
            return

        user_answer = int(val_str)

        expected = self.compute_expected_answer()

        # Count this attempt
        self.total_attempts += 1

        if user_answer == expected:

            # Increase streak
            self.streak += 1

            # Streak multiplier
            # 1st correct = +1
            # 2nd correct = +2
            # 3rd correct = +3
            # etc.
            self.score += self.streak

            self.feedback_msg = (
                f"CORRECT! {self.num_a} {self.operator} "
                f"{self.num_b} = {expected}"
            )

            self.feedback_color = (80, 230, 110)

            # Generate next question
            self.generate_new_card()

        else:

            # Reset streak after wrong answer
            self.streak = 0

            self.feedback_msg = (
                f"WRONG! Expected {expected}."
            )

            self.feedback_color = (240, 75, 75)

            # Clear entered answer
            self.input_box.clear()

    def handle_event(self, event):
        """
        Handle keyboard and mouse events.
        """

        # Send event to input box
        self.input_box.handle_event(event)

        # Press Enter to submit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_answer()

        # Click Submit button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.submit_btn.collidepoint(event.pos):
                    self.submit_answer()

    def update(self):
        """
        Update the countdown timer.
        """

        current_time = pygame.time.get_ticks()

        elapsed = (
            current_time - self.last_update_time
        ) / 1000

        # Update timer every second
        if elapsed >= 1:

            self.time_remaining -= int(elapsed)

            self.last_update_time = current_time

            # Time has expired
            if self.time_remaining <= 0:

                self.time_remaining = 0

                # Timeout counts as an attempt
                self.total_attempts += 1

                # Reset streak after timeout
                self.streak = 0

                self.feedback_msg = "TIME OUT!"

                self.feedback_color = (240, 75, 75)

                # Generate a new question
                self.generate_new_card()

    def render(self, screen):
        """
        Draw the complete game screen.
        """

        screen.fill((25, 29, 37))

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title_surf = self.font_title.render(
            "Math Flashcards Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                18
            )
        )

        # --------------------------------------------------
        # SCORE
        # --------------------------------------------------

        score_surf = self.font_hud.render(
            f"Score: {self.score} / {self.total_attempts}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                self.width // 2 - score_surf.get_width() // 2,
                58
            )
        )

        # --------------------------------------------------
        # STREAK
        # --------------------------------------------------

        streak_surf = self.font_hud.render(
            f"Streak: {self.streak}",
            True,
            (255, 180, 80)
        )

        screen.blit(
            streak_surf,
            (
                self.width // 2 - streak_surf.get_width() // 2,
                82
            )
        )

        # --------------------------------------------------
        # QUESTION CARD
        # --------------------------------------------------

        card_rect = pygame.Rect(
            self.width // 2 - 130,
            110,
            260,
            110
        )

        # Card background
        pygame.draw.rect(
            screen,
            (240, 242, 245),
            card_rect,
            border_radius=12
        )

        # Card border
        pygame.draw.rect(
            screen,
            (85, 120, 175),
            card_rect,
            width=3,
            border_radius=12
        )

        # Question text
        card_str = (
            f"{self.num_a}  "
            f"{self.operator}  "
            f"{self.num_b}"
        )

        card_surf = self.font_card.render(
            card_str,
            True,
            (25, 30, 42)
        )

        screen.blit(
            card_surf,
            (
                card_rect.centerx -
                card_surf.get_width() // 2,

                card_rect.centery -
                card_surf.get_height() // 2
            )
        )

        # --------------------------------------------------
        # TIMER BAR
        # --------------------------------------------------

        timer_x = card_rect.x
        timer_y = card_rect.bottom + 8

        timer_width = card_rect.width
        timer_height = 10

        timer_ratio = max(
            0,
            self.time_remaining / self.time_limit
        )

        # Timer background
        pygame.draw.rect(
            screen,
            (70, 70, 80),
            (
                timer_x,
                timer_y,
                timer_width,
                timer_height
            ),
            border_radius=5
        )

        # Timer progress
        pygame.draw.rect(
            screen,
            (80, 210, 100),
            (
                timer_x,
                timer_y,
                int(timer_width * timer_ratio),
                timer_height
            ),
            border_radius=5
        )

        # Timer text
        timer_text = self.font_hud.render(
            f"Time: {self.time_remaining}s",
            True,
            (220, 220, 225)
        )

        screen.blit(
            timer_text,
            (
                self.width // 2 -
                timer_text.get_width() // 2,

                timer_y + 14
            )
        )

        # --------------------------------------------------
        # INPUT BOX
        # --------------------------------------------------

        self.input_box.render(screen)

        # --------------------------------------------------
        # SUBMIT BUTTON
        # --------------------------------------------------

        pygame.draw.rect(
            screen,
            (45, 140, 80),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (215, 225, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_txt = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            btn_txt,
            (
                self.submit_btn.centerx -
                btn_txt.get_width() // 2,

                self.submit_btn.centery -
                btn_txt.get_height() // 2
            )
        )

        # --------------------------------------------------
        # FEEDBACK MESSAGE
        # --------------------------------------------------

        msg_surf = self.font_hud.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            msg_surf,
            (
                self.width // 2 -
                msg_surf.get_width() // 2,

                315
            )
        )