"""
GUIOverlordDeployment.py
Author: Alonzo James C. Artuz
Created: 4/20/2020

This script is a deployment script for "GUIOverlordScript.py"
"""

import GUIOverlordScript as GUI

def GUIOverlordDeployment():
    """
    Function to be called when deployed.
    """
    win = GUI.UltamiteCubeNoiseGenerator()
    win.create()