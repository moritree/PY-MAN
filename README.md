# PY-MAN
A simple Python implementation of PAC-MAN.

## Ghost behaviour
### Target tiles
The whole time that the game is running, except when the ghosts are turned blue and trying to escape from Pac-Man, each ghost's movement is governed by a "target tile" that it is trying to reach. There are no hard restrictions on where this tile must be- it can be (and often is) located on an inaccessible tile, and much of the ghosts' behaviour is a result of this. Each ghost uses the same algorithm to move towards its target tile, but each ghost has a different method of selecting the target that gives it its unique personality.

#### A.I algorithm
Ghosts are very short sighted and only plan one step ahead as they move about the maze. 
When there is a decision about which way to turn, the choice is made on which tile adjoining the intersection will bring the ghost closest to its target tile. Since this is the only consideration, it can result in the ghost selecting the "wrong" direction and taking an inefficient path to its target. The main restriction is that ghosts cannot reverse their direction unless in a dead end, and a secondary caveat is that they cannot turn upwards through the two exits at the top of the ghost house's area.

### Movement modes
The ghosts are always in one of four modes: chase, scatter, frightened, or dead. 

The mode that the ghosts spend the most time in is "chase". In this mode, all the ghosts use Pac-Man's position as a factor in selecting their target tile, although only Blinky uses Pac-Man's position verbatim.
In Scatter mode, each of the four ghosts has an inaccessible target tile, causing the four ghosts to disperse to the corners and run laps around an island.
Frightened mode is unique, as frightened ghosts have no target tile, but instead make pseudorandom decisions at junctions.
Dead ghosts set their target inside the ghost house, where their eyes speed back to in order to respawn.

### Individual personalities
#### Red Ghost: Blinky
EN:|JA: 
---|---
Shadow |追いかけ (chaser)

Appropriately, Blinky's target tile in chase mode is always Pac-Man's current tile. This makes sure that Blinky is usually following close behind the player. He starts outside of the ghost house and is usually the most immediate threat.

#### Pink Ghost: Pinky
EN:|JA: 
---|---
Speedy |待ち伏せ (ambusher)

Pinky does not, in fact, move any faster than the other ghosts, but can seem faster, as he targets the tile a couple of blocks ahead of the direction which Pac-Man is facing.

#### Blue Ghost: Inky
EN:|JA: 
---|---
Bashful |気紛れ (whimsical)

Inky remains inside the ghost house until Pac-Man has consumed at least 30 dots. Inky uses both Pac-Man and Blinky's position to select its target tile. To locate Inky's target, we first select the tile two squares ahead of Pac-Man (like Pinky's target). Then, imagine drawing a vector from Blinky to this location, and doubling the vector's length- this is Inky's actual target.

#### Orange Ghost: Clyde
EN:|JA: 
---|---
Pokey |お惚け (feigning ignorance)

Clyde is the last to leave the ghost house, only leaving once more than a third of the dots have been collected. Clyde's targeting method can give the impression that he is ignoring Pac-Man altogether- its targeting is identical to Blinky's, except when it is close to Pac-Man, when its target tile is set to its scatter mode tile. The effect is that Clyde alternates between coming towards Pac-Man, and then changing his mind to go back to the corner whenever Pac-Man gets too close.
