

from pylab import *
import pygame
import math
import numpy as np
#==============================================================================
# pygame.mixer.pre_init(44100, -16, 1, 512)
# pygame.mixer.init()
#==============================================================================
print("Initial head")
bird_change_x=3.0
bird_change_y=3.0
rock_change_x=0.0
rock_change_y=0.0


def angryBird(m, g, v0, y0, alpha, diam, rho, k, time, dt):
    """ finds the trajectory of the redstripe with given initial values.
    
    Args:
        m     : mass of the redstripe in kg
        g     : gravity in m/s^2
        v0    : initial release velocity of the redstripe in m/s
        y0    : initial release height of the redstripe in meters
        alpha : initial release angle of the redstripe in degrees
        diam  : diameter of the redstripe in meters
        rho   : air density in kg/m^3
        k     : stiffnes of the spring N/m
        time  : simulation time
        dt    : time step.
    Returns:
        t     : time in seconds
        r     : position in meters
        v     : velocity in m/s
    Raises:
        TypeError: if n is not a number
        ValueError: if n is negative
    """
    alpha = radians(alpha)      # Initial angle in radian
    D = 3.0*rho*diam**2         # drag coefficient
    R = (diam/2)                # ball contact starts - equilibrium length of Spring
    # Numerical initialization
    n = int(ceil(time/dt))
    a = zeros((n, 2), float)
    v = zeros((n, 2), float)
    r = zeros((n, 2), float)
    t = zeros((n, 2), float)
    # Set initial values
    r[0,1] = y0                             # initial position of the ball
    v[0,:] = v0*cos(alpha), v0*sin(alpha)   # initial velocity in i, j

    # Integration loop
    for i in range(n-1):
        if (r[i,1] < R):
            N = k*(R-r[i,1])*array([0,1])
        else:
            N = array([0,0])
        FD = - D*norm(v[i,:])*v[i,:]
        G = -m*g*array([0,1])
        Fnet = N + FD + G
        a = Fnet/m
        v[i+1,:] = v[i] + a*dt
        r[i+1,:] = r[i] + v[i+1]*dt
        t[i+1] = t[i] + dt
    return t, r, v


# Call this function so the Pygame library can initialize itself
pygame.init()
# This sets the name of the window
pygame.display.set_caption('BCO611 is cool')
clock = pygame.time.Clock()
# Before the loop, load the sounds:
click_sound = pygame.mixer.Sound("voyyy.ogg")
fire_sound = pygame.mixer.Sound("boink.ogg")
# Set positions of graphics
background_position = [0, 0]
# Load and set up graphics.
background_image = pygame.image.load("background.png")
# Create an 1280x800 sized screen
screen = pygame.display.set_mode(background_image.get_rect().size)
background_image = background_image.convert()
#screen = pygame.display.set_mode([1280, 800])
background_image_ground = 600
player_image = pygame.image.load("red_sprite_small.png")
player_image_width, player_image_height = player_image.get_rect().size
player_image = player_image.convert()

rock_image = pygame.image.load("rock_small.png")
rock_image_width, rock_image_height = rock_image.get_rect().size
rock_image = rock_image.convert()

textInfo = "angle: 0 magnitude: 0"
yellow = (255, 255, 0)
black = (0,0,0)
font = pygame.font.Font('freesansbold.ttf', 24)
text = font.render(textInfo, True, yellow)
textRect = text.get_rect()
textRect.center = (170,770)



mass = 4             # mass of the ball in kg
gravity = 9.81          # gravitational acceleration in m/sˆ2
v0 = 150                # Initial velocity in m/s
#y0 = 0                 # Initial position in meters
alpha = 30              # Initial angle in degrees
diameter = 0.05         # diameter of the ball in meters
airdensity = 1.225      # air density in kg/m^3
stiffnes = 1000.0       # stiffnes of the spring N/m
time = 60.0             # simulation time
dt = 0.01               # time step

ball_size = 43
bird_mass =8
rock_mass =5


def detect_collision(bird_x,bird_y,rock_x,rock_y):
    """
    This function detects if there is any collision
    """
    
    global bird_change_x
    global bird_change_y
    global rock_change_x
    global rock_change_y
  
    if((((rock_x - bird_x)**2) + ((bird_y - rock_y)**2))<=((ball_size+ball_size)**2)): 
        print("Rock x: ", rock_x, "Rock y: ", rock_y, "Bird x: ", bird_x, "Bird y: ", bird_y)
        if((abs(rock_x-bird_x))!=0): # I just added this control because sometimes balls gets directly into each other and this values gets 0 so division by 0 cause crash
            angle = math.atan((abs(rock_y-bird_y))/(abs(rock_x-bird_x)))
            point_of_collision = [(rock_x + ball_size*math.cos(angle)), (rock_y + ball_size*math.sin(angle))]
            print("Collision angle: ", angle, "  Point of Collision: ", point_of_collision)
            v1, v2 = post_collision_velocity_calc(angle, point_of_collision, bird_mass, rock_mass, 1)
            print("V1: ", v1[0], "V2: ", v2[0])
            # ball.change_x = 3
            
            bird_change_x = float(v1[0])
            bird_change_y = float(v1[1])
            rock_change_x = float(v2[0])
            rock_change_y = float(v2[1])
            hit = True
            return hit, bird_change_x, bird_change_y, rock_change_x, rock_change_y
        

def post_collision_velocity_calc(angle,point_of_collision,body_mass_first,body_mass_second,coefficient_of_restitution):           
     """
     This function returns the post-collision velocities of the bodies. Except for the assignment I added ball referances to get pre collision velocities
     """
     #Ball velocity initialize
     first_ball_vel = np.matrix([[bird_change_x],[bird_change_y]])
     second_ball_vel = np.matrix([[rock_change_x],[rock_change_y]])
     
     #Short name initalize for mass and coefficient values
     m1 = body_mass_first
     m2 = body_mass_second
     e = coefficient_of_restitution
     
     # Rotation matrix initialize
     R1 = np.matrix([[np.cos(angle), np.sin(angle)],
                  [-np.sin(angle), np.cos(angle)]])
     
     R2 = np.matrix([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle), np.cos(angle)]])


     v1p, v1n = R1*first_ball_vel
     v2p, v2n = R1*second_ball_vel
                        
     # Compute the post-collision velocities for the two spheres
     v1pt, v2pt = np.multiply((1.0/(m1+m2)), np.matrix([[(m1-e*m2), m2*(1+e)],[m1*(1+e), (m2-e*m1)]])*np.vstack((v1p, v2p)))
     
     # The final step in the process is to rotate the post-collision velocities
     # back to the standard Cartesian coordinate system
     v1post = R2*np.vstack((v1pt, v1n))
     v2post = R2*np.vstack((v2pt, v2n))
     
     return v1post, v2post

#Initial position of rock
rock_x=800
rock_y=580

#After collision gravity - it is not 9.8 to let it look more like game
fall_gravity = 1

#Parameters to avoid bird and rock into the ground
bird_grounded = False
rock_grounded = False

done = False
simulation = False
game=False
drag=False
start_pos = [0,0]
end_pos = [0,0]

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_pos=pygame.mouse.get_pos()
            drag=True
            print("Mouse down")
        elif event.type == pygame.MOUSEBUTTONUP:
            _, r,v = angryBird(mass, gravity, v0, background_image_ground - y, alpha, diameter, airdensity, stiffnes, time, dt)
            click_sound.play()
            simulation = True
            drag = False
            print("Mouse up")
            
    # Copy image to screen:
    screen.blit(background_image, background_position)
    
    screen.blit(text, textRect)
    
    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    if not simulation and not game:
        if drag:
            end_pos=pygame.mouse.get_pos()
            if end_pos[1]-start_pos[1]!=0 and end_pos[0]-start_pos[0]!=0 :
                dx = end_pos[0]-start_pos[0]
                dy = end_pos[1]-start_pos[1]
                angle = math.atan2(-dy,dx)
                dist = math.sqrt((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)
                degs = math.degrees(angle)
                
                x1 ,y1 = start_pos[0] , start_pos[1] 
                x2 = start_pos[0] + (start_pos[0] - end_pos[0]) 
                y2 = start_pos[1] + (start_pos[1] - end_pos[1]) 
                pygame.draw.line(screen, black, [x1,y1], [x2,y2], 5)
                
                
                if degs<=0 :
                    degs += 180
                else:
                    degs -= 180
                    
                draw_rad = math.radians(degs)
                
                
                
                print(degs,dist)
                
                text = font.render(textInfo, True, yellow)
                textInfo = "angle: {} magnitude: {}".format(int(degs), int(dist))
                alpha = degs
                v0 = dist
            print(start_pos, end_pos)
        else:
            player_position = pygame.mouse.get_pos()
            x = player_position[0] - player_image_width/2
            y = player_position[1] - player_image_height/2
            if y > background_image_ground:  y = background_image_ground
        
        
        #After sim calc
        
        # Copy image to screen:
        screen.blit(player_image, [x, y])
        screen.blit(rock_image, [rock_x,rock_y])
    else:
        screen.blit(text, textRect)
        pygame.mouse.set_visible(False)
        if not game:
            for i in range(len(r)):
                screen.blit(background_image, background_position)
                screen.blit(text, textRect)
                bird_change_x = v[i,0]/5
                bird_change_y = v[i,1]/5
                xsim = x + r[i, 0]
                ysim = background_image_ground - r[i, 1]
                game = detect_collision(xsim, ysim, rock_x, rock_y)
                
                if game:
                    print("----Hit----")
                    
                    x = xsim
                    y = ysim
                    break
                if ysim >= background_image_ground: fire_sound.play()
                    
                # Copy image to screen:
                screen.blit(player_image, [xsim, ysim])
                screen.blit(rock_image, [rock_x,rock_y])
                pygame.mouse.set_pos(xsim + 45 , ysim + 45)
                pygame.display.flip()
        else:
            print("Bird change x,y: " + str(bird_change_x) +" " + str(bird_change_y))
            print("Rock change x,y: " + str(rock_change_x) +" " + str(rock_change_y))
            x += bird_change_x
            if y <= background_image_ground and not bird_grounded:
                y += bird_change_y
                y += bird_mass * fall_gravity
            else:
                bird_grounded = True
                y=background_image_ground
            rock_x += rock_change_x
            
            
            if rock_y <= background_image_ground and not rock_grounded:
                rock_y += rock_change_y
                rock_y += rock_mass * fall_gravity
            else:
                rock_grounded=True
                rock_y=background_image_ground
            screen.blit(player_image, [x, y])
            screen.blit(rock_image, [rock_x,rock_y])
        pygame.mouse.set_visible(True)
        simulation = False
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit ()
