# Regal Run: What is it?
Regal Run is a small platforming game i made to improve my skills in game development and Python.
The whole development process was around 3 months long. I worked on the game on and off in my free time.\
 \
Regal Run is 100% made in Python. It contains a level system, physics, animations, parallax and a lot more.

## What Did I Learn?
Before this i only had some game-making experience in Unity and so i knew nothing about how much work would have to be put into this.
I learned a lot of new stuff and gained a new viewpoint to game-making.
### Camera Creation and Usage
Cameras in Unity were easy. I just had to place it in the game environment and make it track the player. With pygame it was different.
Since the screen's location was constant i had to render objects with the camera's location as an offset so that they could be moved onto the screen. It was quite an experience but i learned a lot.
### Collisions
Collisions are a staple for platforming games. The hero needs somewhere to stand on right?
I thought this was going to be easy since i just had to check if the player's collision box was inside the ground collision box and then prevent the player from moving further, but that produced a buggy mess.
I had to seperate the collision checks into axises and move in that axis first then check the collision. This taught me a lot about problem-solving.
### Framerates and How They Affect the Game
I had already understood from Unity that i had to seperate the physics from the rest of the code.
But only when i started this project i learned that i had to seperate physics and rendering specifically.
Towards the end of the project i had to seperate the fps of rendering and physics. Then i had to make the game occasionally execute multiple frames of physics and even fractions of frames to catch up to the framerate.
From all this i grasped the basics of managing framerate and why it's incredibly important in projects.
### Levels, Editing, Saving and Loading
Regal Run has a very basic system for levels. You start the game and the game loads levels from the .level files. As you get to the end you move onto the next level. The levels are made from tiles.
Which are saved as chunks[^1] in the files to save space. There are spikes, death pits, checkpoints and endpoints. Theres also a scrolling parallax background which was irrefutably a pain to implement.\
 \
Theres also a level editing system for the game. By pressing the keybind **C** you can toggle on and off the editor mode. While you are in editor mode you can fly around freely and can go through tiles. You can also select tiles from a list to modify the level.
Once you are done editing the level you can press the keybind **V** to save the level.
### Python and Pygame
I'm no expert in Python, but after making Regal Run with it my Python and Pygame skills improved drastically. I didn't specifically learn anything, but i can more comfortably program in Python now.
## What I Could've Done Better and What Went Well
I think i still have a lot of room to improve on in programming and game design in general, but i picked out the most important topics to discuss here.
### The Structure of the Code
In my opinion i rushed a lot of things. The code isn't very reusable and there was a lot of hardcoding involved. I should've used more functions and classes to generalise everything.
Also the lack of experience in Pygame made me create lots of problems. Especially the coordinate system in Regal Run is not very well thought out.
### Planning
I had already planned out most of the game in the beginning. Changes were of course made into the plans during development, but i think i should've planned out the programming part out aswell. Since my plans were fairly surface level and in my opinion quite lacking i should've spent more time fleshing out the idea of the game.
### Research
I mostly made everything myself without putting much thought into it. For example level saving and loading, optimizations and physics were all made by me with maybe a little bit of looking up information. Since i didn't know the best algorithms and methods to do these things i think i could've optimized the game better if i had researched a little more.
### So, What Went Well?
I think i successfully performed good optimization to my game. I performed frustum culling[^2] which upped the performance of the game. I optimized level saving into seperate chunks[^1] so that the level files were considerably smaller. I also restrained collision checks to tiles only close to the player.
Also the art that i made in my opinion fit with Buch's tileset well.
## Appendix
In short i made a Python game using the Pygame library. I learned a lot of important aspects of game development and improved my programming skills.
I will also add a few smaller sections down here for less important information.
<details>
  <summary>FAQ</summary>
  <ul>
    <li>How many levels are there?
      <ul>
        <li>There are 6 levels including the last lobby level in the base game.</li>
      </ul>
    </li>
    <li>Will you be expanding upon the game?
      <ul>
        <li>I don't plan to expand upon the game except maybe a few bug fixes here and there. You are free to make your own levels though.</li>
      </ul>
    </li>
  </ul>
  
</details>

<details>
  <summary>How to create levels</summary>
  <ol>
    <li>Navigate to the levels folder.</li>
    <li>Add a new file called <b>level_number.level</b></li> 
    <li>Then play through all levels until you end up at your newly created level.</li>
    <li>Editor mode can be activated by pressing <b>C</b></li>
    <li>After you are done with the editing of the level press <b>V</b> to save it.</li>
  </ol>
  <ul>
   <li>Tile IDs:
   <ol type="1">
    <li>Collision</li>
    <li>Death</li>
    <li>Checkpoint</li>
    <li>Endpoint</li>
    <li>Opacity increase (ex. bushes)</li>
   </ol>
   </li>
  </ul>
  
</details>

<details>
  <summary>Showcase</summary>
  <ul>
   <li>
    <a href="https://youtu.be/TUaTfN_zZiw">Playthrough and Showcase</a>
   </li>
  </ul>
</details>



<details>
  <summary>Credits</summary>
  <ul>
    <li>Art is from <a href="https://opengameart.org/content/a-platformer-in-the-forest">A platformer in the forest</a> by Buch with a few small additions of my own.</li>
    <li>Sounds were made with <a href="https://sfxr.me/">jsfxr</a>.</li>
    <li>All the source code is made by me.</li>
    
  </ul>
</details>

[^1]: Chunks in this regard are areas of the same type of tile which i saved within the .level file into seperate lines. Chunks were saved with the smallest and biggest x and y values and the tiles' metadata.
[^2]: Frustum culling is a basic technique where you cull all objects that aren't inside the camera's bounding box.
