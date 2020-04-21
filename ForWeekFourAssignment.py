"""
ForWeekFourAssignment.py
Author: Alonzo James C. Artuz
Last edited: 4/21/2020

A Utility Script for GUIOverlordScript.py

"""

import maya.cmds as mc
import random

import os

"""
colorSelect is a global variable that stores lists for colors
"""
colorSelect = []
colorSelect.append([1,0,0]) #red
colorSelect.append([0,1,0]) #green
colorSelect.append([0,0,1]) #blue
colorSelect.append([1,0,1])  #magenta
colorSelect.append([1,1,0]) #yellow

def randomCubes(**kwargs):
    """
    randomCubes(**kwargs)
        INPUT:
            **kwargs                a dicitonary of keyword arguements, to be used to generate cubes. Should not be inputted manually, but given by GUIOverlordScript.py

    randomCubes(**kwargs) will take arguements from GUIOverlordScript, unpack them and generate cubes based on them
    """
    #setting defaults, in event some kind of null is passed.
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
    if(not kwargs["numberOfCubes"] is None): #if exists, then use.
        numOfCubes = kwargs["numberOfCubes"]
        
    if(not kwargs["startFrame"] is None): #if exists, then use
        if((kwargs["startFrame"] < endFrame) and (kwargs["startFrame"] > 0)): #checking if the start frame is larger than the end frame.
            startFrame = kwargs["startFrame"]
        
    if(not kwargs["endFrame"] is None): #if exists, then use
        if(kwargs["endFrame"] > startFrame): #checking if the end frame is larger than the start frame
            endFrame = kwargs["endFrame"]
    
    if(not kwargs["sizeRandom"] is None): #if exists, then use
        sizeRandom[0] = kwargs["sizeRandom"][0]
           
    if(kwargs["sizeRandom"][1] >= sizeRandom[0]): #checking if max is greater than or equal to min
        sizeRandom[1] = kwargs["sizeRandom"][1]
           
    if(not kwargs["allowColor"] is None): #if exists, then use
        allowColor = kwargs["allowColor"]
        
    if(not kwargs["minJitter"] is None): #if exists, then use
        minJitter = kwargs["minJitter"]
        
    if(not kwargs["maxJitter"] is None): #if exists, then use
        maxJitter = kwargs["maxJitter"]
        
    halfFrame = endFrame/2 #Creating the "halfFrame" for animation purposes
    grp = mc.group(em=True,name="CubeGroup") #Creating the base group

    for i in range(numOfCubes):
        
        #cube has random height/depth/width properties
        cube = mc.polyCube(height=random.randint(sizeRandom[0],sizeRandom[1]),depth=random.randint(sizeRandom[0],sizeRandom[1]),width=random.randint(sizeRandom[0],sizeRandom[1]),name="ModCube1")
        
        #add shader if allowed
        if(allowColor):
            ranColor = colorSelect[random.randint(0,4)]
            setShader(cube,ranColor)
            
        #Set a keyframe at start , 1/4 , 1/2 , 3/4 , end
        setKeyFrames(cube,minJitter,maxJitter,startFrame,endFrame)
        setKeyFrames(cube,minJitter,maxJitter,halfFrame)
        setKeyFrames(cube,minJitter,maxJitter,(halfFrame*1.5))
        setKeyFrames(cube,minJitter,maxJitter,(halfFrame/1.5))

        #parent the cube to the group
        mc.parent(cube,grp)

def setKeyFrames(obj,minJitter,maxJitter,*frames):
    """
    setKeyFrames(Obj obj,Array[3] minJitter, Array[3] maxJitter, Int *frame)
        INPUTS:
            Object obj              the polygon to be affected
            List[3] minJitter       the XYZ minimum position of obj
            List[3] maxJitter       the XYZ maximum position of obj
            Int *frames             the specific frames to have these transformations.
    """

    #random position
    rx = random.randint(minJitter[0],maxJitter[0])
    ry = random.randint(minJitter[1],maxJitter[1])
    rz = random.randint(minJitter[2],maxJitter[2])
    
    #move cube
    mc.move(rx,ry,rz,obj,a=True)
    
    #set keyframes based on frame input
    for i in frames:
        mc.currentTime(i)
        mc.setKeyframe(obj,at = "translateX", v= rx)
        mc.setKeyframe(obj,at = "translateY", v= ry)
        mc.setKeyframe(obj,at = "translateZ", v= rz)
        
def setShader(poly,color):
    """
    setShader(poly,color)
        INPUT:
            Object poly                   the polygon that you want shaded
            List[int,int,int] color       the color that you want the polygon

        this function will create a blinn shader with the given color then it will assign it to poly
    """
    #create shader
    myShader = mc.shadingNode("blinn",asShader=True)

    #sets shader colors
    specShaderR = mc.setAttr(myShader + ".colorR",color[0])
    specShaderG = mc.setAttr(myShader + ".colorG",color[1])
    specShaderB = mc.setAttr(myShader + ".colorB",color[2])

    #assign
    mc.select(poly[0])
    mc.hyperShade(assign=myShader)
