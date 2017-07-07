1. Install the following from the repositories:
	- python-webpy
	- python-pygame
	- mediainfo
	- uzbl

2. Edit the BASE, ASSETS, VIDEOS, STATIC, CRASHES, BUMPERS variables to point to the proper directories.
	You will find them in the main loop of h.py

3. Run h.py
	It will start a uzbl screen. That screen is the audience and team screen.

4. Open another browser and navigate to http://localhost:8080/manage
	I think the options are mostly self explanatory.

5. Podium hints are at http://localhost:8080/hints
	Autorefresh currently at 3 seconds. 

6. Editing at http://localhost:8080/editor
	you can add/edit/delete teams an categories from there.
