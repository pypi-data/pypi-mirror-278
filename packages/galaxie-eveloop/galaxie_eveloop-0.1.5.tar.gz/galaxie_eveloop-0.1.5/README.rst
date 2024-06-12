.. image:: https://img.shields.io/badge/License-WTFPL-brightgreen.svg
   :target: http://www.wtfpl.net/about/
   :alt: License: WTFPL
.. image:: https://readthedocs.org/projects/galaxie-eveloop/badge/?version=latest
  :target: https://galaxie-eveloop.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

=============================
Galaxie EveLoop documentation
=============================
.. figure::  https://galaxie-curses.readthedocs.io/_images/logo_galaxie.png
   :align:   center

Description
-----------
Galaxie Event Loop is a low tech main loop couple with a event bus.

After many years as kernel of Galaxie Curses project, it have been as decision to extract the main loop and the event bus.
Especially that because it work and be very small.


Links
-----
 * Git: https://codeberg.org/Tuuux/galaxie-eveloop/
 * Read the Doc: https://galaxie-eveloop.readthedocs.io/
 * PyPI: https://pypi.org/project/galaxie-eveloop/
 * PuPI Test: https://test.pypi.org/project/galaxie-eveloop/

Installation via pip
--------------------
Pypi

.. code:: bash

  pip install galaxie-eveloop

Pypi Test

.. code:: bash

  pip install -i https://test.pypi.org/simple/ galaxie-eveloop

Example
-------

.. code:: python

  from glxeveloop import MainLoop
  from time import time

  count = 1
  mainloop = MainLoop().loop
  mainloop.timer.fps.min = 30
  mainloop.timer.fps.value = 60
  mainloop.timer.fps.max = 30
  start = time()


  def pre():
      global count
      global mainloop
      global start
      if count >= 30:
          mainloop.stop()


  def cmd():
      global count
      global mainloop

      print("COUNT: {0}, FPS: {1}".format(count, mainloop.timer.fps.value))


  def post():
      global count
      count += 1
      if count > 30:
          print("TIME: {0}".format((time() - start)))
          print("PRECISION: {0}".format(1 - (time() - start)))


  def main():
      mainloop.hooks.cmd = cmd
      mainloop.hooks.pre = pre
      mainloop.hooks.post = post

      mainloop.start()


  if __name__ == '__main__':
      main()

While return

.. code:: shell

  COUNT: 1, FPS: 60.0
  COUNT: 2, FPS: 60.0
  COUNT: 3, FPS: 30.0
  COUNT: 4, FPS: 30.0
  COUNT: 5, FPS: 30.0
  COUNT: 6, FPS: 30.0
  COUNT: 7, FPS: 30.0
  COUNT: 8, FPS: 30.0
  COUNT: 9, FPS: 30.0
  COUNT: 10, FPS: 30.0
  COUNT: 11, FPS: 30.0
  COUNT: 12, FPS: 30.0
  COUNT: 13, FPS: 30.0
  COUNT: 14, FPS: 30.0
  COUNT: 15, FPS: 30.0
  COUNT: 16, FPS: 30.0
  COUNT: 17, FPS: 30.0
  COUNT: 18, FPS: 30.0
  COUNT: 19, FPS: 30.0
  COUNT: 20, FPS: 30.0
  COUNT: 21, FPS: 30.0
  COUNT: 22, FPS: 30.0
  COUNT: 23, FPS: 30.0
  COUNT: 24, FPS: 30.0
  COUNT: 25, FPS: 30.0
  COUNT: 26, FPS: 30.0
  COUNT: 27, FPS: 30.0
  COUNT: 28, FPS: 30.0
  COUNT: 29, FPS: 30.0
  COUNT: 30, FPS: 30.0
  TIME: 0.9341855049133301
  PRECISION: 0.0657961368560791

It Take 2 iterations for the loop to slow FPS for match the 30 FPS ask by the setting.
The mainloop can impose a Frame Rate :)