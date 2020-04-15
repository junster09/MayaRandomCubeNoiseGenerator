"""
ForWeekFourAssignment.py

A script that makes a new scene, runs "randomCubes", then saves the file

"""

import maya.cmds as mc
import random

import os
print os.environ["HOME"]

#reload(rca)


"""
randomCubes(**kwargs)

Random cubes will use numOfCubes and generate that amount of cubes in a random space.
"""

def randomCubes(**kwargs):
    startFrame = mc.playbackOptions(query = True, minTime = True)
    endFrame = mc.playbackOptions(query = True, maxTime = True)
    
    numOfCubes = 0
    #sizeRandom[0] is min
    #sizeRandom[1] is max
    sizeRandom = [0,5]
    
    allowColor = False
    
    minJitter = [-5,-5,-5]
    
    maxJitter = [5,5,5]
    
    #looking through kwargs
    if(not kwargs["numberOfCubes"] is None):
        numOfCubes = kwargs["numberOfCubes"]
        
    if(not kwargs["startFrame"] is None):
        if((kwargs["startFrame"] < endFrame) and (kwargs["startFrame"] > 0)):
            startFrame = kwargs["startFrame"]
        
    if(not kwargs["endFrame"] is None):
        if(kwargs["endFrame"] > startFrame):
            endFrame = kwargs["endFrame"]
    
    if(not kwargs["sizeRandom"] is None):
        sizeRandom[0] = kwargs["sizeRandom"][0]
           
    if(kwargs["sizeRandom"][1] >= sizeRandom[0]):
        sizeRandom[1] = kwargs["sizeRandom"][1]
           
    if(not kwargs["allowColor"] is None):
        allowColor = kwargs["allowColor"]
        
    if(not kwargs["minJitter"] is None):
        minJitter = kwargs["minJitter"]
        
    if(not kwargs["maxJitter"] is None):
        maxJitter = kwargs["maxJitter"]
        
    halfFrame = endFrame/2
    grp = mc.group(em=True,name="CubeGroup")
    #makes x random cube between -10,10
    for i in range(numOfCubes):
        
        #cube has random height/depth/width properties
        cube = mc.polyCube(height=random.randint(sizeRandom[0],sizeRandom[1]),depth=random.randint(sizeRandom[0],sizeRandom[1]),width=random.randint(sizeRandom[0],sizeRandom[1]),name="ModCube1")
        
        if(allowColor):
            AddColorToObject(cube)
            
        #do frame anim
        setKeyFrames(cube,minJitter,maxJitter,startFrame,endFrame)
        setKeyFrames(cube,minJitter,maxJitter,halfFrame)
        setKeyFrames(cube,minJitter,maxJitter,(halfFrame*1.5))
        setKeyFrames(cube,minJitter,maxJitter,(halfFrame/1.5))
        
        mc.parent(cube,grp)
"""
setKeyFrames(Obj obj,Array[3] minJitter, Array[3] maxJitter, Int *frame)

wil set a new random position of obj and keyframe it at frame
"""

def setKeyFrames(obj,minJitter,maxJitter,*frames):
    
    #random position
    rx = random.randint(minJitter[0],maxJitter[0])
    ry = random.randint(minJitter[1],maxJitter[1])
    rz = random.randint(minJitter[2],maxJitter[2])
    
    #move cube
    mc.move(rx,ry,rz,obj,a=True)
    
    #rotate cube
    #mc.rotate(rx,ry,rz,obj,a=True)
    
    for i in frames:
        mc.currentTime(i)
        mc.setKeyframe(obj,at = "translateX", v= rx)
        mc.setKeyframe(obj,at = "translateY", v= ry)
        mc.setKeyframe(obj,at = "translateZ", v= rz)
    
"""
AddColorToObject(obj)

will apply a color to a geometry in the editor.
"""
def AddColorToObject(objectToColor):
    mc.select(clear=True)
    numVertex = mc.polyEvaluate(objectToColor,vertex=True)
    
    for i in range(0,numVertex,random.randint(1,2)):
        
        vtxName = objectToColor[0] + ".vtx[%s]"%i
        
        mc.select(vtxName)
        mc.polyColorPerVertex(colorRGB=[random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)],colorDisplayOption=True)
        
"""
createShapeFast(s)

Will create and extrude a polySphere.
"""
def createShapeFast(s):
    obj = mc.polySphere(r=s,name="ModSphere1")
    
    polycount = mc.polyEvaluate(obj[0],face = True)
    
    face = []
    
    for i in range(0,polycount,random.randint(1,4)):
        #"%s.f[%s]%(Object Name, Index) gathers faces
        face.append("%s.f[%s]"%(obj[0],i))
        
    mc.polyExtrudeFacet(face,kft=False,ltz=1,ls=[0.1,0.1,0.1])
    return obj
