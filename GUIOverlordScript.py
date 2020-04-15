"""
GUIOverlordScript.py
Author: Alonzo James C. Artuz
Created: 4/6/2020

This script is a GUI interface for "ForWeekFourAssignment.py" based on the "OptionsWindowBaseClass.py"
"""
import maya.cmds as mc
import ForWeekFourAssignment as fwf
import OptionsWindowBaseClass as OWBC

reload(fwf)
reload(OWBC)

class UltamiteCubeNoiseGenerator(OWBC.OptionsWindow):
    """
    Custom windows base class
    """
      
    def __init__(self):
        OWBC.OptionsWindow.__init__(self)
        self.title = "Ultamite Cube Noise Generator v0.1"
        self.actionName = "Generate Cubes and Close"
        self.applyName = "Generate Cubes"
        
    def displayOptions(self):
        self.layout = mc.columnLayout(adjustableColumn = True)
        
        self.frame1 = mc.frameLayout(collapsable=True,label="Cube Number",width=512)
        self.subFrame = mc.rowColumnLayout(nr = 3,adjustableColumn = True)
        self.cubeIntField = mc.intFieldGrp(numberOfFields=1,label="number of Cubes",value1=5)
        mc.setParent("..")
        
        self.frame2 = mc.frameLayout(collapsable=True,label="Cube attributes",width=512)
        self.FrameIntField = mc.intFieldGrp(numberOfFields=2,label="Frame Period",value1=0,value2=0) #leave blank for default
        self.sizeIntField = mc.intFieldGrp(numberOfFields=2,label="Size min/max",value1=0,value2=5)
        self.minJitIntField = mc.intFieldGrp(numberOfFields=3,label="Minimum position Jitter",value1=-5,value2=-5,value3=-5)
        self.maxJitIntField = mc.intFieldGrp(numberOfFields=3,label="Maximum position Jitter",value1=5,value2=5,value3=5)
        mc.setParent("..")
        
        self.frame3 = mc.frameLayout(collapsable=True,label="Color attributes")
        self.allowColorCheckBox = mc.checkBox(label="Use Color")
        
    def applyBtnCmd(self,*args):
        """ 
        applyBtnCmd() will be called when the user presses Generate Cubes button 
        This function will read values set by the user and pass it to ForWeekFourAssignment for cube generation
        """
        self.commandDict = {}
        
        _cubeNum = mc.intFieldGrp(self.cubeIntField,q=True,v1=True)
        self.commandDict["numberOfCubes"] = _cubeNum
        
        _startFrame = mc.intFieldGrp(self.FrameIntField,q=True,v1=True)
        self.commandDict["startFrame"] = _startFrame
        
        _endFrame = mc.intFieldGrp(self.FrameIntField,q=True,v2=True)
        self.commandDict["endFrame"] = _endFrame
        
        _sizeRandom = [mc.intFieldGrp(self.sizeIntField,q=True,v1=True),mc.intFieldGrp(self.sizeIntField,q=True,v2=True)]
        self.commandDict["sizeRandom"] = _sizeRandom
        
        _allowColor = mc.checkBox(self.allowColorCheckBox,q=True,v=True)
        self.commandDict["allowColor"] = _allowColor
        
        _minJit = [mc.intFieldGrp(self.minJitIntField,q=True,v1=True),mc.intFieldGrp(self.minJitIntField,q=True,v2=True),mc.intFieldGrp(self.minJitIntField,q=True,v3=True)]
        self.commandDict["minJitter"] = _minJit
        
        _maxJit = [mc.intFieldGrp(self.maxJitIntField,q=True,v1=True),mc.intFieldGrp(self.maxJitIntField,q=True,v2=True),mc.intFieldGrp(self.maxJitIntField,q=True,v3=True)]
        self.commandDict["maxJitter"] = _maxJit
        
        fwf.randomCubes(**self.commandDict)
    
    def actionCmd(self,*args):
        """ 
        actionCmd() will call applyBtnCmd() and close the window
        """
        self.applyBtnCmd()
        mc.deleteUI(self.window,window=True)
        
    def helpMenuCmd(self,*args):
        """
        helpMenuCmd() will create a new window with help information about the tool
        """
        mc.window( width=273 , height=175, title = "Ultamite Cube Noise Generator Help")
        mc.columnLayout( adjustableColumn=True )
        mc.text( label='UltamiteCubeNoiseGenerator' )
        mc.text( label='A simpler tool that will generate an amount of cubes with many customization options' )
        mc.text( label='All of the default number will run the script correctly' )

        mc.showWindow()
        
win = UltamiteCubeNoiseGenerator()
win.create()