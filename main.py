import pgzrun
import random
import itertools

WIDTH=400
HEIGHT=400

BLOCK_POSITIONS=[
    (350,50),
    (350,350),
    (50,350),
    (50,50),
]
#the cycle function will let us cycle through the positions indefinitely
block_positions=itertools.cycle(BLOCK_POSITIONS)
block=Actor("block",center=(50,50))
ship=Actor("ship", center=(200,200))

def draw():
    screen.clear()
    screen.blit("background",(65,100))
    block.draw()
    ship.draw()

#blockMVT
def move_block():
    animate(block,"bounce_end", duration=1, pos=next(block_positions))

move_block()
clock.schedule_interval(move_block,3)

#shipMVT
def next_ship_target():
    x=random.randint(100,300)
    y=random.randint(100,300)
    ship.target=x,y

    target_angle=ship.angle_to(ship.target)
    #angles are tricky
    # Angles are tricky because 0 and 359 degrees are right next to each other.
   #
   # If we call animate(angle=target_angle) now, it wouldn't know about this,
   # and will simple adjust the value of angle from 359 down to 0, which means
   # that the ship spins nearly all the way round.
   #
   # We can always add multiples of 360 to target_angle to get the same angle.
   # 0 degrees = 360 degrees = 720 degrees = -360 degrees and so on. If the
   # ship is currently at 359 degrees, then having it animate to 360 degrees
   # is the animation we want.
   #
   # Here we calculate how many multiples we need to add so that any rotations
   # will be less than 180 degrees.
    target_angle+=360*((ship.angle-target_angle+180)//360)
   
    animate(
       ship,
       angle=target_angle,
       duration=2,
       on_finished=move_ship,

   )

def move_ship():
    anim=animate(
        ship,
        tween="accel_decel",
        pos=ship.target,
        duration=ship.distance_to(ship.target)/200,
        on_finished=next_ship_target,

    )

next_ship_target()
pgzrun.go()
