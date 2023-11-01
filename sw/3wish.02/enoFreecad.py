# Scene support routines, initially for FreeCAD
# Brygg Ullmer, Clemson University
# Begun 2023-11-01

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import yaml, traceback

##################### Enodia FreeCAD support objects ##################### 

class enoFreecad:
  yamlFn    = None
  yamlD     = None
  yamlScene = None
  fcDoc     = None

  partTypeMap  = {'box': 'Part::Box', 'plane': 'Part::Plane'}
  fcObjHandles = {}

  ############# constructor #############

  def __init__(self, yamlFn=None, fcDoc=None, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.yamlFn = yamlFn
    self.fcDoc  = fcDoc

    if yamlFn is not None: self.loadYaml(yamlFn)

  ############# getObj #############

  def getObj(self, objName):
    if self.fcObjHandles is None:
      print("enoFreecad getObj error: fcObjHandles is None"); return None

    if objName not in self.fcObjHandles:
      print("enoFreecad getObj error: object %s not in fcObjHandles" % objName); return None

    result = self.fcObjHandles(objName)
    return result

  ################# Add Object ################# 

  def loadYaml(self, yamlFn):
    try:
      self.yamlFn = yamlFn
      f           = open(yamlFn, 'rt')
      self.yamlD  = yaml.safe_load(f)

      if 'scene' in self.yamlD:
        self.yamlScene = self.yamlD['scene']
        if not isinstance(self.yamlScene, list):
           print("enoFreecad parseYaml error: scene found, but does not contain a list"); return None
        
        for el in self.yamlScene: self.addObjectY(el)
    except:
      print("enoFreecad parseYaml exception:"); traceback.print_exc(); return None

  ################# Add Object by parsed YAML description ################# 

  # parse entries like:
  #- {name: bldg1a,  type: box,   dimensions: [28, 28, 3], placement: [[ 0,  0,   0], [0,  0, 0]]}
  #- {name: floor,   type: plane, dimensions: [32, 32],    placement: [[-1, -1,   0], [0,  0, 0]]}

  def addObjectY(self, objY):
    try:
      for field in ['name', 'type', 'dimensions']:
        if field not in objY :
          print("enoFreecad addObjectY: no %s found in %s" % (field, objY)); return None

      pname, ptype, dimensions = objY['name'], objY['type'], objY['dimensions']

      if ptype in self.partTypeMap: fcPtype = self.partTypeMap[pttype]
      else: print("enoFreecad addObjectY: part type %s is presently unknown" % ptype); return None

      obj = self.doc.addObject(fcPtype, pname)

      obj.Length = dimensions[0]
      obj.Width  = dimensions[1]

      if len(dimensions) == 3:
        obj.Height = dimensions[2]

      if 'placement' in objY:
        objTrans, objRot = objY['placement']
        tx, ty, tz = objTrans
        rx, ry, rz = objRot

        obj.Placement = Appl.Placement(App.Vector(tx, ty, tz), App.Rotation(rx, ry, rz))
      
      self.fcObjHandles[pname] = obj

    except:
      print("enoFreecad addObjectY exception:"); traceback.print_exc(); return None

### end ###

