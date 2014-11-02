#! /usr/bin/env python
""" Tutorial 5: Textured Cube
"""
from __future__ import print_function

from OpenGL.GL import *
from csgl import *

import glfw
import math as mathf

ViewMatrix = mat4.fill(0)
ProjectionMatrix = mat4.fill(0)

def getViewMatrix():
    return ViewMatrix

def getProjectionMatrix():
    return ProjectionMatrix


# Initial position : on +Z
position = vec3( 0, 0, 5 )
# Initial horizontal angle : toward -Z
horizontalAngle = 3.14
# Initial vertical angle : none
verticalAngle = 0.0
# Initial Field of View
initialFoV = 45.0

speed = 3.0 # 3 units / second
mouseSpeed = 0.005

lastTime = None

def computeMatricesFromInputs(window):
    global lastTime
    global position
    global horizontalAngle
    global verticalAngle
    global initialFoV
    global ViewMatrix
    global ProjectionMatrix

    # glfwGetTime is called only once, the first time this function is called
    if lastTime == None:
        lastTime = glfw.get_time()

    # Compute time difference between current and last frame
    currentTime = glfw.get_time()
    deltaTime = currentTime - lastTime

    # Get mouse position
    xpos,ypos = glfw.get_cursor_pos(window)

    # Reset mouse position for next frame
    glfw.set_cursor_pos(window, 1024/2, 768/2);

    # Compute new orientation
    horizontalAngle += mouseSpeed * float(1024.0/2.0 - xpos );
    verticalAngle   += mouseSpeed * float( 768.0/2.0 - ypos );

    # Direction : Spherical coordinates to Cartesian coordinates conversion
    direction = vec3(
        mathf.cos(verticalAngle) * mathf.sin(horizontalAngle), 
        mathf.sin(verticalAngle),
        mathf.cos(verticalAngle) * mathf.cos(horizontalAngle)
    )
    
    # Right vector
    right = vec3(
        mathf.sin(horizontalAngle - 3.14/2.0), 
        0.0,
        mathf.cos(horizontalAngle - 3.14/2.0)
    )
    
    # Up vector
    up = vec3.cross( right, direction )

    # Move forward
    if glfw.get_key( window, glfw.KEY_UP ) == glfw.PRESS or glfw.get_key( window, glfw.KEY_W ) == glfw.PRESS:
        position += direction * deltaTime * speed;
    
    # Move backward
    if glfw.get_key( window, glfw.KEY_DOWN ) == glfw.PRESS or glfw.get_key( window, glfw.KEY_S ) == glfw.PRESS:
        position -= direction * deltaTime * speed
    
    # Strafe right
    if glfw.get_key( window, glfw.KEY_RIGHT ) == glfw.PRESS or glfw.get_key( window, glfw.KEY_D ) == glfw.PRESS:
        position += right * deltaTime * speed
    
    # Strafe left
    if glfw.get_key( window, glfw.KEY_LEFT ) == glfw.PRESS or glfw.get_key( window, glfw.KEY_A ) == glfw.PRESS:
        position -= right * deltaTime * speed
    

    FoV = initialFoV# - 5 * glfwGetMouseWheel(); # Now GLFW 3 requires setting up a callback for this. It's a bit too complicated for this beginner's tutorial, so it's disabled instead.

    # Projection matrix : 45 Field of View, 4:3 ratio, display range : 0.1 unit <-> 100 units
    ProjectionMatrix = mat4.perspective(FoV, 4.0 / 3.0, 0.1, 100.0)
    # Camera matrix
    ViewMatrix       = mat4.lookat(
                                position,           # Camera is here
                                position+direction, # and looks here : at the same position, plus "direction"
                                up                  # Head is up (set to 0,-1,0 to look upside-down)
                           )

    # For the next frame, the "last time" will be "now"
    lastTime = currentTime
