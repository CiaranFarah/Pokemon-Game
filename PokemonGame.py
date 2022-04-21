import pygame

pygame.init()

win = pygame.display.set_mode((576, 576))  # Creates a 576 X 576 window for the game to be played on

pygame.display.set_caption("Pokemon Battle")  # Sets the name at top of the window

clock = pygame.time.Clock()
bg = pygame.image.load("bg.png")

# All the sprites used for animating the Pokemon
tyranitar_walk_up = [pygame.image.load(".//sprites/Tyranitar/6.png"), pygame.image.load(".//sprites/Tyranitar/7.png"), pygame.image.load(".//sprites/Tyranitar/8.png"), pygame.image.load(".//sprites/Tyranitar/11.png")]
tyranitar_walk_down = [pygame.image.load(".//sprites/Tyranitar/0.png"), pygame.image.load(".//sprites/Tyranitar/1.png"), pygame.image.load(".//sprites/Tyranitar/9.png"), pygame.image.load(".//sprites/Tyranitar/10.png")]
tyranitar_walk_left = [pygame.image.load(".//sprites/Tyranitar/4.png"), pygame.image.load(".//sprites/Tyranitar/3.png"), pygame.image.load(".//sprites/Tyranitar/4.png"), pygame.image.load(".//sprites/Tyranitar/5.png")]
tyranitar_walk_right = [pygame.image.load(".//sprites/Tyranitar/17.png"), pygame.image.load(".//sprites/Tyranitar/18.png"), pygame.image.load(".//sprites/Tyranitar/19.png"), pygame.image.load(".//sprites/Tyranitar/20.png")]
tyranitar_death = pygame.image.load(".//sprites/Tyranitar/13.png")
tyranitar_projectiles = [pygame.image.load(".//sprites/Tyranitar/Projectile0.png"), pygame.image.load(".//sprites/Tyranitar/Projectile1.png"), pygame.image.load(".//sprites/Tyranitar/Projectile2.png"), pygame.image.load(".//sprites/Tyranitar/Projectile3.png")]


blaziken_walk_left = [pygame.image.load(".//sprites/blaziken/0.png"), pygame.image.load(".//sprites/blaziken/1.png"), pygame.image.load(".//sprites/blaziken/15.png"), pygame.image.load(".//sprites/blaziken/16.png")]
blaziken_walk_right = [pygame.image.load(".//sprites/blaziken/17.png"), pygame.image.load(".//sprites/blaziken/18.png"), pygame.image.load(".//sprites/blaziken/19.png"), pygame.image.load(".//sprites/blaziken/20.png")]
blaziken_walk_up = [pygame.image.load(".//sprites/blaziken/4.png"), pygame.image.load(".//sprites/blaziken/5.png"), pygame.image.load(".//sprites/blaziken/9.png"), pygame.image.load(".//sprites/blaziken/8.png")]
blaziken_walk_down = [pygame.image.load(".//sprites/blaziken/13.png"), pygame.image.load(".//sprites/blaziken/12.png"), pygame.image.load(".//sprites/blaziken/11.png"), pygame.image.load(".//sprites/blaziken/10.png")]
blaziken_death = pygame.image.load(".//sprites/blaziken/14.png")
blaziken_projectiles = [pygame.image.load(".//sprites/blaziken/projectile3.png"),pygame.image.load(".//sprites/blaziken/projectile4.png"), pygame.image.load(".//sprites/blaziken/projectile5.png"), pygame.image.load(".//sprites/blaziken/projectile6.png")]


class projectile(object):  # Class for when the Pokemon attack
    def __init__(self, x, y, facing, graphics):
        self.x = x
        self.y = y

        self.facing = facing
        self.graphics = graphics

        if facing == "left" or facing == "up":  #If the projectile goes left or up we want to decrement the y value
            self.vel = -7  # The Y axis is inverted in pygame so to go up you decrement
        else:
            self.vel = 7

    def draw(self, win):
        if facing == "right":  # Select the projectile art based on direction of the Pokemon
            picture = self.graphics[0]
        elif facing == "left":
            picture = self.graphics[1]
        elif facing == "up":
            picture = self.graphics[2]
        else:
            picture = self.graphics[3]

        win.blit(picture, (self.x, self.y))


class pokemon(object):
    def __init__(self, x, y, width, height, walk_left, walk_right, walk_up, walk_down, death_sprite):
        self.x = x  # X coordinate of character
        self.y = y  # Y coordinate of character
        self.width = width  # Width and height of spreight
        self.height = height
        self.vel = 5  # How much our characters x, y coordinate changes by

        self.left = False  # If the character is currently walking left or right
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0

        self.standing = True  # If the character isn't moving
        self.hitbox = (self.x, self.y + 11, 19, 52)  # Ignore this for now
        self.walk_left = walk_left  # These are the lists of sprites
        self.walk_right = walk_right
        self.walk_up = walk_up
        self.walk_down = walk_down
        self.death_sprite = death_sprite
        self.health = 10

    def draw(self, win):  # Displays the sprites

        if self.health > 0:
            if self.walkCount + 1 >= 12:  # We have 4 sprites per animation and we want 3 frames per second so 4*3=12
                self.walkCount = 0

            if not self.standing:  # If the character is moving we need to update the sprite to reflect that

                if self.left:
                    win.blit(self.walk_left[self.walkCount // 3], (self.x, self.y))  # This cycles through the animation sprites
                    self.walkCount += 1
                elif self.right:
                    win.blit(self.walk_right[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1

                elif self.up:
                    win.blit(self.walk_up[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1

                elif self.down:
                    win.blit(self.walk_down[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1

            else:
                if self.right:  # If the character is facing right when we stop display that image
                    win.blit(self.walk_right[0], (self.x, self.y))

                elif self.up:
                    win.blit(self.walk_up[0], (self.x, self.y))

                elif self.down:
                    win.blit(self.walk_down[0], (self.x, self.y))

                else:
                    win.blit(self.walk_left[0], (self.x, self.y))

        else:  # If the Pokemon is out of health we switch their art to their death sprite
            win.blit(self.death_sprite, (self.x, self.y))

        self.hitbox = (self.x, self.y, 26, 29)  # This is the hitbox to check if the Pokemon gets hit by attacks
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, 25, 8))  # This is the healthbar red
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 10, 25 - (2.5 * (10 - self.health)), 8))  # This is the green part and every time the Pokemon gets hit we make it horizontally smaller so red can show

    def hit(self):
        if self.health > 0:
            self.health -= 1

def redrawGameWindow():  # We need to redraw the window every second so the sprites refresh
    win.blit(bg, (0, 0))
    tyranitar.draw(win)  # Draw our Pokemon
    blaziken.draw(win)
    for shot in blaziken_fire:  # Draw every projectile since multiple can be on the screen at once
        shot.draw(win)

    for shot in tyranitar_fire:
        shot.draw(win)

    pygame.display.update()


tyranitar = pokemon(250, 210, 26, 30, tyranitar_walk_left, tyranitar_walk_right, tyranitar_walk_up, tyranitar_walk_down, tyranitar_death)
blaziken = pokemon(250, 210, 26, 30, blaziken_walk_left, blaziken_walk_right, blaziken_walk_up, blaziken_walk_down, blaziken_death)
blaziken_fire = []  # Lists to hold their attacks
tyranitar_fire = []

blaziken_shoot_loop = 0  # Variable used to cause a delay so they can't spam attacks
tyranitar_shoot_loop = 0


run = True
while run:
    clock.tick(12)  # Slight delay so everything can execute

    if blaziken_shoot_loop > 0:  # Explained above
        blaziken_shoot_loop += 1

    if blaziken_shoot_loop > 10:
        blaziken_shoot_loop = 0

    if tyranitar_shoot_loop > 0:
        tyranitar_shoot_loop += 1

    if tyranitar_shoot_loop > 10:
        tyranitar_shoot_loop = 0

    for event in pygame.event.get():  # Make sure we quit if they hit the x button on the window
        if event.type == pygame.QUIT:
            run = False

    for shot in blaziken_fire:  # Check if the attack hit the opponent

        if shot.facing == "up":  #hitbox at 0 and 1 are the x, and y, hitbox at 2 and 3 are width and height
            #  The hitbox for up checks that the attack is between the x coordinate and the x coordinate - width and between the y coordinate and y coordinate - height
            if shot.x  > tyranitar.hitbox[0] - tyranitar.hitbox[2] and shot.x < tyranitar.x + tyranitar.hitbox[2] and shot.y > tyranitar.hitbox[1] - tyranitar.hitbox[3] and shot.y < tyranitar.hitbox[1]:  # Checks if projectile is between top and bottom of hitbox
                tyranitar.hit()
                blaziken_fire.pop(blaziken_fire.index(shot))
        elif shot.facing == "down":
            #  The rest of the hitboxes follow similar logic with slight adjustments
            if shot.x  > tyranitar.hitbox[0] - tyranitar.hitbox[2] and shot.x < tyranitar.x + tyranitar.hitbox[2] and shot.y > tyranitar.hitbox[1] - tyranitar.hitbox[3] and shot.y < tyranitar.hitbox[1]:  # Checks if projectile is between top and bottom of hitbox
                tyranitar.hit()
                blaziken_fire.pop(blaziken_fire.index(shot))

        elif shot.facing == "right":

            if shot.x  > tyranitar.hitbox[0] - tyranitar.hitbox[2] and shot.x < tyranitar.x + tyranitar.hitbox[2] and shot.y < tyranitar.hitbox[1] + tyranitar.hitbox[3] and shot.y > tyranitar.hitbox[1]:
                tyranitar.hit()
                blaziken_fire.pop(blaziken_fire.index(shot))

        else:
            if shot.x  < tyranitar.hitbox[0] + tyranitar.hitbox[2] and shot.x > tyranitar.x  and shot.y < tyranitar.hitbox[1] + tyranitar.hitbox[3] and shot.y > tyranitar.hitbox[1]:
                tyranitar.hit()
                blaziken_fire.pop(blaziken_fire.index(shot))

        if (shot.facing == "right" or shot.facing == "left") and shot.x < 576 and shot.x > 0:  # If the Pokemon is facing right or left we want to have the attack move on the x axis
            shot.x += shot.vel

        elif (shot.facing == "up" or shot.facing == "down") and shot.y <576 and shot.y > 0:  # If the Pokemon is facing up or down we want to have the attack on the y axis
            shot.y += shot.vel
        else:  # We are done with the attack so we want it popped from the list so it disappears
            blaziken_fire.pop(blaziken_fire.index(shot))

    for shot in tyranitar_fire:  # This is the same code as above but for the other Pokemon
        if shot.facing == "up":
            if shot.x  > blaziken.hitbox[0] - blaziken.hitbox[2] and shot.x < blaziken.x + blaziken.hitbox[2] and shot.y > blaziken.hitbox[1] - blaziken.hitbox[3] and shot.y < blaziken.hitbox[1]:  # Checks if projectile is between top and bottom of hitbox
                blaziken.hit()
                tyranitar_fire.pop(tyranitar_fire.index(shot))

        elif shot.facing == "down":
            if shot.x  > blaziken.hitbox[0] - blaziken.hitbox[2] and shot.x < blaziken.x + blaziken.hitbox[2] and shot.y > blaziken.hitbox[1] - blaziken.hitbox[3] and shot.y < blaziken.hitbox[1]:  # Checks if projectile is between top and bottom of hitbox
                blaziken.hit()
                tyranitar_fire.pop(tyranitar_fire.index(shot))

        elif shot.facing == "right":

            if shot.x  > blaziken.hitbox[0] - blaziken.hitbox[2] and shot.x < blaziken.x + blaziken.hitbox[2] and shot.y < blaziken.hitbox[1] + blaziken.hitbox[3] and shot.y > blaziken.hitbox[1]:
                blaziken.hit()
                tyranitar_fire.pop(tyranitar_fire.index(shot))

        else:
            if shot.x  < blaziken.hitbox[0] + blaziken.hitbox[2] and shot.x > blaziken.x  and shot.y < blaziken.hitbox[1] + blaziken.hitbox[3] and shot.y > blaziken.hitbox[1]:
                blaziken.hit()
                tyranitar_fire.pop(tyranitar_fire.index(shot))



        if (shot.facing == "right" or shot.facing == "left") and shot.x < 576 and shot.x > 0:
            shot.x += shot.vel

        elif (shot.facing == "up" or shot.facing == "down") and shot.y <576 and shot.y > 0:
            shot.y += shot.vel
        else:
            tyranitar_fire.pop(tyranitar_fire.index(shot))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and blaziken.x > blaziken.vel:  #Update the variables depending on which key is pressed
        # Also moves Pokemon to left, the rest of the keys are self explanatory
        blaziken.x -= blaziken.vel
        blaziken.standing = False
        blaziken.left = True
        blaziken.right = False
        blaziken.up = False
        blaziken.down = False

    elif keys[pygame.K_RIGHT] and blaziken.x < 576 - blaziken.width - blaziken.vel:  # Have a checker to make sure Pokemon won't go off screen
        blaziken.x += blaziken.vel
        blaziken.standing = False
        blaziken.right = True
        blaziken.left = False
        blaziken.up = False
        blaziken.down = False

    elif keys[pygame.K_UP] and blaziken.y > blaziken.vel:
        blaziken.y -= blaziken.vel
        blaziken.standing = False
        blaziken.right = False
        blaziken.left = False
        blaziken.up = True
        blaziken.down = False

    elif keys[pygame.K_DOWN] and blaziken.y < 545:  # Make sure Pokemon doesn't go off screen
        blaziken.y += blaziken.vel
        blaziken.standing = False
        blaziken.right = False
        blaziken.left = False
        blaziken.up = False
        blaziken.down = True

    if keys[pygame.K_RSHIFT] and blaziken_shoot_loop == 0:
        if blaziken.left:
            facing = "left"
        elif blaziken.right:
            facing = "right"
        elif blaziken.down:
            facing = "down"
        else:
            facing = "up"

        if len(blaziken_fire) < 6:  # Create the attack and allow up to 6 attacks on screen at once
            blaziken_fire.append(projectile((blaziken.x), round(blaziken.y + blaziken.height//2), facing, blaziken_projectiles))

        blaziken_shoot_loop = 1  # Update this to avoid spam attacks

    if (keys[pygame.K_e] or keys[pygame.K_q]) and tyranitar_shoot_loop == 0:
        if tyranitar.left:  # This Pokemon needed a bit more adjustment to get the attack to come out at the proper place
            calculation_x = (tyranitar.x - tyranitar.width - 15)  # That is why there are calculation variables
            calculation_y = round(tyranitar.y - tyranitar.height / 4 + 20)
            facing = "left"
        elif tyranitar.right:
            calculation_x = (tyranitar.x + tyranitar.width / 1)
            calculation_y = round(tyranitar.y - tyranitar.height/4 + 20)
            facing = "right"
        elif tyranitar.down:
            calculation_x = (tyranitar.x + tyranitar.width/2.25)
            calculation_y = round(tyranitar.y + tyranitar.height)
            facing = "down"
        else:
            calculation_x = (tyranitar.x + tyranitar.width/2.25)
            calculation_y = round(tyranitar.y - tyranitar.height)
            facing = "up"

        if len(tyranitar_fire) < 3:

            tyranitar_fire.append(projectile(calculation_x, calculation_y, facing, tyranitar_projectiles))

        tyranitar_shoot_loop = 1

    if keys[pygame.K_a] and tyranitar.x > tyranitar.vel:  # All the same as the other Pokemon
        tyranitar.x -= tyranitar.vel
        tyranitar.standing = False
        tyranitar.left = True
        tyranitar.right = False
        tyranitar.up = False
        tyranitar.down = False

    elif keys[pygame.K_d] and tyranitar.x < 576 - tyranitar.width - tyranitar.vel:
        tyranitar.x += tyranitar.vel
        tyranitar.standing = False
        tyranitar.right = True
        tyranitar.left = False
        tyranitar.up = False
        tyranitar.down = False

    elif keys[pygame.K_w] and tyranitar.y > tyranitar.vel:
        tyranitar.y -= tyranitar.vel
        tyranitar.standing = False
        tyranitar.right = False
        tyranitar.left = False
        tyranitar.up = True
        tyranitar.down = False

    elif keys[pygame.K_s] and tyranitar.y < 545:
        tyranitar.y += tyranitar.vel
        tyranitar.standing = False
        tyranitar.right = False
        tyranitar.left = False
        tyranitar.up = False
        tyranitar.down = True

    if not keys[pygame.K_d] and not keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]:  # If no keys are being pressed make the character be still
        tyranitar.standing = True
        tyranitar.walkCount = 0

    if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        blaziken.standing = True

        blaziken.walkCount = 0


    redrawGameWindow()

    if blaziken.health == 0 or tyranitar.health == 0:
        pygame.time.wait(10000)  # Freezes the game and waits 10 seconds for window to close once game is finished
        run = False


pygame.quit()

