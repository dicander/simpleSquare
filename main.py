# import the pygame module, so you can use it
from dataclasses import dataclass
import random

import pygame


@dataclass
class Bullet:
    x: int
    y: int

@dataclass
class Alien:
    x: int
    y: int
    direction: int

@dataclass
class Particle:
    x: int
    y: int
    speed_x: int
    speed_y: int

# define a main function
def main():
    # initialize the pygame module
    framecounter = 0
    pygame.init()
    X_MAX = 10
    X_MIN = -10
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BULLET_SPEED = 10
    BULLET_SIZE = 10
    ALIEN_SIZE = 40
    COOLDOWN_INIT = 20

    # load and set the logo
    pygame.display.set_caption("Space Invaders")
    killedaliens = 0
    clock = pygame.time.Clock()

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # define a variable to control the main loop
    running = True

    hero_y = 500
    hero_x = 300
    alien_speed = 1
    hero_dead = False
    x_speed = 0
    left_pressed = False
    right_pressed = False
    shooting = False
    bullets = []
    aliens = []
    alienbullets = []
    particles = []
    direction = -1
    for y in [20, 120, 220]:
        direction *= -1
        for x in range(0, 800, 50):
            aliens.append(Alien(x, y, direction))

    cooldown = 0
    """ Main loop """
    while running:
        """Add alien counter to the screen"""
        # fill the screen with black
        screen.fill((3, 3, 3))
        dead_bullets = []
        for bullet in bullets:
            pygame.draw.rect(screen, (0, 255, 0), (bullet.x, bullet.y, BULLET_SIZE, BULLET_SIZE))
            bullet.y -= BULLET_SPEED
            if bullet.y < -BULLET_SIZE:
                dead_bullets.append(bullet)
        for dead_bullet in dead_bullets:
            bullets.remove(dead_bullet)
        dead_bullets = []
        for bullet in alienbullets:
            pygame.draw.rect(screen, (255, 255, 0), (bullet.x, bullet.y, BULLET_SIZE, BULLET_SIZE))
            bullet.y += BULLET_SPEED
            if bullet.y > SCREEN_HEIGHT:
                dead_bullets.append(bullet)
        for dead_bullet in dead_bullets:
            alienbullets.remove(dead_bullet)
        """Check if the hero is hit by an alien bullet"""
        for bullet in alienbullets:
            if bullet.x + BULLET_SIZE//2 > hero_x and bullet.x + BULLET_SIZE // 2 < hero_x + 50 and \
                    hero_y < bullet.y + BULLET_SIZE//2 < hero_y + 50:
                hero_dead = True
                hero_x = SCREEN_WIDTH
                hero_y = SCREEN_HEIGHT
                for i in range(1000):
                    particles.append(Particle(hero_x + 25 + random.randint(0, 20),
                                              hero_y + 25 + random.randint(0, 20),
                                              random.randint(-20, 20),
                                              random.randint(-10, 10)))
                alienbullets.remove(bullet)
                break
        """Check if the hero is hit by an alien"""
        for alien in aliens:
            if hero_x < alien.x + ALIEN_SIZE // 2 < hero_x + 50 and \
                    hero_y < alien.y + ALIEN_SIZE // 2 < hero_y + 50:
                hero_dead = True
                hero_x = SCREEN_WIDTH
                hero_y = SCREEN_HEIGHT
                for i in range(1000):
                    particles.append(Particle(hero_x + 25 + random.randint(0, 20),
                                              hero_y + 25 + random.randint(0, 20),
                                              random.randint(-20, 20),
                                              random.randint(-10, 10)))
                break
        dead_aliens = []
        for alien in aliens:
            for bullet in bullets:
                if bullet.x > alien.x and bullet.x < alien.x + ALIEN_SIZE and \
                        bullet.y > alien.y and bullet.y < alien.y + ALIEN_SIZE:
                    for i in range(250):
                        particles.append(Particle(alien.x + ALIEN_SIZE // 2+random.randint(0, 20),
                                                  alien.y + ALIEN_SIZE // 2+random.randint(0, 20),
                                                  random.randint(-20, 20),
                                                  random.randint(-10, 10)))
                    dead_aliens.append(alien)
                    bullets.remove(bullet)
                    break
            pygame.draw.rect(screen, (0, 0, 255), (alien.x, alien.y, ALIEN_SIZE, ALIEN_SIZE))
            if alien.y % (ALIEN_SIZE + 10) != 0 or \
                    (alien.x == 0 and alien.direction < 0) or \
                    (alien.x == SCREEN_WIDTH - ALIEN_SIZE and alien.direction > 0):
                alien.y += 1
                if alien.x < 0:
                    alien.x = 0
                if alien.x == 0:
                    alien.direction = 1
                if alien.x > SCREEN_WIDTH - ALIEN_SIZE:
                    alien.x = SCREEN_WIDTH - ALIEN_SIZE
                if alien.x == SCREEN_WIDTH - ALIEN_SIZE:
                    alien.direction = -1
            else:
                alien.x += alien.direction * alien_speed
            if alien.x < 0:
                alien.x = 0
            if alien.x > SCREEN_WIDTH - ALIEN_SIZE:
                alien.x = SCREEN_WIDTH - ALIEN_SIZE
        killedaliens += len(dead_aliens)

        alien_speed = 3 - len(aliens)//20
        for dead_alien in dead_aliens:
            aliens.remove(dead_alien)
        dead_particles = []
        for particle in particles:
            pygame.draw.rect(screen, (255, 0, 0), (particle.x, particle.y, 2, 2))
            particle.x += particle.speed_x
            particle.y += particle.speed_y

            if particle.x < 0 or particle.x > SCREEN_WIDTH or particle.y > SCREEN_HEIGHT:
                dead_particles.append(particle)
            if framecounter % 3 == 0:
                particle.speed_y += 1
                if particle.speed_x > 0:
                    particle.speed_x -= 1
                if particle.speed_x < 0:
                    particle.speed_x += 1
        for dead_particle in dead_particles:
            particles.remove(dead_particle)
        """Go through all aliens and randomly make any one of them shoot an alien bullet."""
        if framecounter % 100 == 0:
            if aliens:
                attacker = random.choice(aliens)
                alienbullets.append(Bullet(attacker.x + ALIEN_SIZE // 2, attacker.y + ALIEN_SIZE))
        if not aliens and not hero_dead:
            """Print all aliens eliminated"""
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Win condition fulfilled. Enjoy free movement!', True, (255, 255, 255), (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, textRect)
        if not hero_dead:
            pygame.draw.rect(screen, (255, 255, 255), (hero_x, hero_y, 50, 50))
        else:
            """If the hero is dead, display a message"""
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('GAME OVER!', True, (255, 255, 255), (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, textRect)
        """Show the number of aliens still in the game in the top left corner"""
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Aliens left: ' + str(len(aliens)), True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 4, 25)
        screen.blit(text, textRect)
        """Show the number of aliens killed in the top right corner"""
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Aliens killed: ' + str(killedaliens), True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2 + 200, 25)
        screen.blit(text, textRect)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                running = False
            # If user presses the S key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                left_pressed = True
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                left_pressed = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                right_pressed = True
            if event.type == pygame.KEYUP and event.key == pygame.K_f:
                right_pressed = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j and not hero_dead:
                shooting = True
            if event.type == pygame.KEYUP and event.key == pygame.K_j or hero_dead:
                shooting = False
        if right_pressed:
            if x_speed < X_MAX:
                x_speed += 1
        elif x_speed > 0:
            x_speed -= 1
        if left_pressed:
            if x_speed > X_MIN:
                x_speed -= 1
        elif x_speed < 0:
            x_speed += 1
        hero_x += x_speed
        if hero_x < 0:
            hero_x = 0
            x_speed = 0
        if hero_x > SCREEN_WIDTH - 50:
            hero_x = SCREEN_WIDTH - 50
            x_speed = 0
        if shooting and cooldown == 0:
            bullets.append(Bullet(hero_x + 20, hero_y-10))
            cooldown = COOLDOWN_INIT
        clock.tick(60)
        if cooldown > 0:
            cooldown -= 1
        framecounter += 1
        pygame.display.flip()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()



