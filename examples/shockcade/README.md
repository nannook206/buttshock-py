Ever wanted to really feel an arcade game?

Own a ET312 box, a serial cable, linux, and mame?

This little project interfaces a ET312 to mame games. It currently
supports Street Fighter 2 (ShockFighterII?) but you can plug in
anything else by modifying the lua code.

If you get hit, you get a decreasing shock. If you get KO'd then you
get a ~10 second shock on high.

Requirements:

* Any ET312 box. You'll need a link cable to connect it to your
computer. We assume it's at /dev/ttyUSB0, if not you can edit the
default in etgame.py or add an option into the lua file.

* The etgame.py script and shockcade.lua file and the buttshock-py
library (which this came with)

* Some linux box (Ubuntu, Fedora, Raspberry PI) with Python3 called python3. If your
python3 isn't called python3 then alter that in the py file.

* Mame and various mame roms like sf2.zip. Mame 0.171 won't work as it
has a bug, but earlier and later ones will. Make sure you can run
"mame sf2" and play the game as normal.

* Player 1 hooked to channel A of your ET box, optionally player 2
hooked to channel B. Set the levels of the A and B knobs
appropriately. Our shocks only go as high as you set those levels.

Run:

run this in the directory where the py and lua files are

% mame -rp /path/to/your/rom -autoboot_script shockcade.lua sf2

a couple of seconds later, if everything is working, you'll see "Game"
appear instead of the current mode name on the ET box.

You're ready. fight!

If you're finding yourself losing on purpose you don't have your level
high enough!

Other games:

You can make this work for other games too, like getting a shock when
you get eaten by a ghost in pacman, or even as a a "new email"
notifier, we look forward to seeing your patches!  Look at mamecheats
for memory locations for lives and power levels for various games.

Raspberry PI 3:

Getting this all working on a Raspberry PI 3 is possible, but a bit
of a hassle.  It is a hassle because all the mame emulators shipped
with PI things like picade are not the mamedev version and therefore
don't support LUA scripting.  However this works:

* Install Rasbian.

* You need a newer version of SDL2 which has PI3 optimizations.  So
follow these instructions
http://choccyhobnob.com/tutorials/compiling-mame-on-raspberry-pi/ for
installing SDL2 and SDL2-ttf

* You need Mame 0.171 or later. I used 0.174 already compiled to
save time from the site above.

* Run "mame -cc" to make a config file, then edit it. I selected
"autoframeskip", decreased the sound mix to 11050, disabled
video aliasing.

* Run mame as above, in X.  Framebuffer video isn't fast enough.

* If you're using a large display you still won't be able to run
properly. I used the PI "hdmi_mode" setting in config.txt to select
a 800x600 mode.

