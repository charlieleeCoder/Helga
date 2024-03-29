# Helga and The Server of Death
#### Video Demo:  <URL https://youtu.be/qFMmevdh3gM>
#### Description:
For my final project, I decided to deep dive into Python. It was the only programming language I was semi-familiar with before the course and therefore an area of interest.

I have previously made some basic games in Scratch and also using the pygame module and began a more ambitious 2d fighter game before starting this course that I didn't complete.

I decided to recreate a top-down RPG, similar in spirit to Zelda, called Helga. I just started a role where I use SQL all the time, so the image of an evil server was low-hanging fruit. I decided to create the game as a 3 by 3 grid of tiles that get updated as the x and y positions change, moving the player back to the coordinates on the opposite side of the tile they just left.

I think more than anything I learnt about feature creep. I implemented a load feature and a new game feature. However, I never actually implemented a save feature, other than the one that happens as you start a new game in a save slot. However, you can run a seperate sqlite3 query to change the starting tile.

I also did far less animations than I thought I would as the art aspect of the game is immensely time consuming and I didn't have suffcient time to spend creating many frame animations.

I probably dedicated too much time to the user interface section. I never got around to implementing the options either, only new game and continue. Also, I couldn't get this to work in a seperate module as intended, but later realised I was trying to return a changed copy of a list and that there would have been a fairly simple workaround but that would require a bit more time, which is unfortunately running out.

I also wish I could have implemented a proper text engine, for story and dialogue, as the draw_text function is pretty basic and doesn't really suit an RPG game so much as a Game Over or Victory screen.

I am pleased that I have started to use aspects of object orientated programming more, even using inheritance and parent and child classes within a seperate module. I would say my programming knowledge has probably grown more from this assignment than any other, but that is has also taken considerably longer.