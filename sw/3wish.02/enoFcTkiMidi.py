# Initial weaving of weaving of FreeCAD and kin, Tkinter, and midi controls
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import sys

from w3core  import *
from w3shift import *

################### Enodia FreeCAD Tkinter Midi controls ###################

class enoFcTkiMidi:
  numSliders     = 8
  tkiSliderWidth = 300
  tkiSliderNames = None

  useTki  = True 
  useMidi = True

  tkiActive      = None
  midiActive     = None

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.useTki:  self.activateTki();  self.buildTki()
    if self.useMidi: self.activateMidi(); self.buildMidi()

    if self.textureImgFn is not None:
      self.buildTexturePlaneIv()



view, doc, sg, root = genViewDocSgRoot()

#Heider & Simmel 1944 variant; https://www.youtube.com/watch?v=VTNmLt7QX8E
stage  = doc.addObject("Part::Plane", "floor")  #https://wiki.freecad.org/Part_Plane
bldg1a = doc.addObject("Part::Box",   "bldg1a")
bldg1b = doc.addObject("Part::Box",   "bldg1b")

screen1 = doc.addObject("Part::Plane", "screen1") 
screen2 = doc.addObject("Part::Plane", "screen2") 

stage.Length     = stage.Width  = 32.
bldg1a.Length    = bldg1a.Width = 28.; bldg1a.Height = 3.
bldg1b.Length    = bldg1b.Width = 26.; bldg1b.Height = 3.
screen1.Width    = 8
screen1.Length   = 8. / 1.77
screen2.Width    = screen1.Width
screen2.Length   = screen1.Length

stage.Placement   = App.Placement(App.Vector(-1,   -1, 0), App.Rotation( 0, 0, 0))
bldg1a.Placement  = App.Placement(App.Vector( 0,    0, 0), App.Rotation( 0, 0, 0))
bldg1b.Placement  = App.Placement(App.Vector( 1,    1, 1), App.Rotation( 0, 0, 0))
screen1.Placement = App.Placement(App.Vector( 3,    3, 5), App.Rotation( 0, 90, 0))
screen2.Placement = App.Placement(App.Vector( 11.5, 3, 5), App.Rotation( 0, 90, 0))

bldgCut1   = App.activeDocument().addObject("Part::Cut", "Bldg central void")
bldgCut1.Base = bldg1a
bldgCut1.Tool = bldg1b

doc.recompute()

Gui.runCommand('Std_ViewZoomOut',0)
Gui.SendMsgToActiveView("ViewFit")

### end ###
