# Provided code for Subdivison and Geodesic Spheres

from __future__ import division
import traceback

# parameters used for object rotation by mouse
mouseX_old = 0
mouseY_old = 0
rot_mat = PMatrix3D()

vertices = []
faces = []
corners = []
opposites = []
isRandom = False
isShown = False
c = 0

# initalize things
def setup():
    size (800, 800, OPENGL)
    frameRate(30)
    noStroke()

# draw the current mesh (you will modify parts of this routine)
def draw():
    
    global vertices
    global faces
    global corners
    global opposites
    global isRandom
    global isShown
    global c
    
    background (100, 100, 180)    # clear the screen to black

    perspective (PI*0.2, 1.0, 0.01, 1000.0)
    camera (0, 0, 6, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    
    # create an ambient light source
    ambientLight (102, 102, 102)

    # create two directional light sources
    lightSpecular (202, 202, 202)
    directionalLight (100, 100, 100, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    stroke (0)                    # draw polygons with black edges
    fill (200, 200, 200)          # set the polygon color to white
    ambient (200, 200, 200)
    specular (0, 0, 0)            # turn off specular highlights
    shininess (1.0)
    
    applyMatrix (rot_mat)   # rotate the object using the global rotation matrix

    # THIS IS WHERE YOU SHOULD DRAW YOUR MESH
    
    for face in faces:
        
        if (isRandom):
            fill(face[3])
        
            beginShape()
            vertex(vertices[face[0]][0], vertices[face[0]][1], vertices[face[0]][2])
            vertex(vertices[face[1]][0], vertices[face[1]][1], vertices[face[1]][2])
            vertex(vertices[face[2]][0], vertices[face[2]][1], vertices[face[2]][2])
            endShape(CLOSE)
        
        else:
            fill(200, 200, 200)
            
            beginShape()
            vertex(vertices[face[0]][0], vertices[face[0]][1], vertices[face[0]][2])
            vertex(vertices[face[1]][0], vertices[face[1]][1], vertices[face[1]][2])
            vertex(vertices[face[2]][0], vertices[face[2]][1], vertices[face[2]][2])
            endShape(CLOSE)
            
    if (len(vertices) != 0 and len(corners) != 0 and isShown):
        translate(vertices[corners[c]][0] * 0.8 + vertices[corners[next(c)]][0] * 0.1 + vertices[corners[next(next(c))]][0] * 0.1, 
                  vertices[corners[c]][1] * 0.8 + vertices[corners[next(c)]][1] * 0.1 + vertices[corners[next(next(c))]][1] * 0.1, 
                  vertices[corners[c]][2] * 0.8 + vertices[corners[next(c)]][2] * 0.1 + vertices[corners[next(next(c))]][2] * 0.1)
        sphere(0.04)
    
    popMatrix()

# read in a mesh file (this needs to be modified)
def read_mesh(filename):
    
    global vertices
    global faces
    global corners
    global opposites
    global isRandom
    global c
    
    vertices = []
    faces = []
    corners = []
    opposites = []
    c = 0

    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        
        vertices.append([x, y, z])

    # read in the faces
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if (nverts != 3):
            print "error: this face is not a triangle"
            exit()

        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        
        faces.append([index1, index2, index3, color(random(255), random(255), random(255))])
        corners.append(index1)
        corners.append(index2)
        corners.append(index3)
        
    opposites = [0] * len(corners)
    for a in range(len(corners)):
        for b in range(len(corners)):
            opposite(a, b)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# process key presses (call your own routines!)
def handleKeyPressed():
    
    global vertices
    global faces
    global corners
    global opposites
    global isRandom
    global isShown
    global c
    
    if key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == 'n': # next
        c = next(c)
    elif key == 'p': # previous
        c = next(next(c))
    elif key == 'o': # opposite 
        c = opposites[c]
    elif key == 's': # swing
        c = swing(c)
    elif key == 'd': # subdivide mesh
        newFaces = []
        m1 = []
        m2 = []
        m3 = []
        for face in faces:
            m1 = [(vertices[face[0]][0] + vertices[face[1]][0]) / 2, (vertices[face[0]][1] + vertices[face[1]][1]) / 2, (vertices[face[0]][2] + vertices[face[1]][2]) / 2]
            m2 = [(vertices[face[2]][0] + vertices[face[1]][0]) / 2, (vertices[face[2]][1] + vertices[face[1]][1]) / 2, (vertices[face[2]][2] + vertices[face[1]][2]) / 2]
            m3 = [(vertices[face[0]][0] + vertices[face[2]][0]) / 2, (vertices[face[0]][1] + vertices[face[2]][1]) / 2, (vertices[face[0]][2] + vertices[face[2]][2]) / 2]
            
            if vertices.count(m1) == 0:
                vertices.append(m1)
            if vertices.count(m2) == 0:
                vertices.append(m2)
            if vertices.count(m3) == 0:
                vertices.append(m3)
                
            newFaces.append([face[0], vertices.index(m1), vertices.index(m3), color(random(255), random(255), random(255))])
            newFaces.append([vertices.index(m1), face[1], vertices.index(m2), color(random(255), random(255), random(255))])
            newFaces.append([vertices.index(m2), face[2], vertices.index(m3), color(random(255), random(255), random(255))])
            newFaces.append([vertices.index(m1), vertices.index(m2), vertices.index(m3), color(random(255), random(255), random(255))])
            
        faces = newFaces
        corners = []
        
        for face in faces:
            corners.append(face[0])
            corners.append(face[1])
            corners.append(face[2])
            
        opposites = [0] * len(corners)
        for a in range(len(corners)):
            for b in range(len(corners)):
                opposite(a, b)
            
    elif key == 'i': # inflate mesh
        newVertices = []
        
        for v in vertices:
            newVertices.append(PVector(v[0] , v[1], v[2]).normalize())
            
        vertices = newVertices
        
    elif key == 'r': # toggle random colors
        isRandom = not isRandom
    elif key == 'c': # toggle showing current corner
        isShown = not isShown
    elif key == 'q': # quit the program
        exit()

# remember where the user first clicked
def mousePressed():
    global mouseX_old, mouseY_old
    mouseX_old = mouseX
    mouseY_old = mouseY

# change the object rotation matrix while the mouse is being dragged
def mouseDragged():
    global rot_mat
    global mouseX_old, mouseY_old
    
    if (not mousePressed):
        return
    
    dx = mouseX - mouseX_old
    dy = mouseY - mouseY_old
    dy *= -1

    len = sqrt (dx*dx + dy*dy)
    if (len == 0):
        len = 1
    
    dx /= len
    dy /= len
    rmat = PMatrix3D()
    rmat.rotate (len * 0.005, dy, dx, 0)
    rot_mat.preApply (rmat)

    mouseX_old = mouseX
    mouseY_old = mouseY

def next(c):
    t = c // 3
    n = 3 * t + (c + 1) % 3
    return n

def opposite(a, b):
    global vertices
    global opposites
    global corners

    if (vertices[corners[next(a)]] == vertices[corners[next(next(b))]] and vertices[corners[next(b)]] == vertices[corners[next(next(a))]]):
        opposites[a] = b
        opposites[b] = a

def swing(c):
    n = next(c)
    r = opposites[n]
    s = next(r)
    return(s)     
