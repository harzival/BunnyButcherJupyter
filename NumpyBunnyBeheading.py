#!/usr/bin/env python
# coding: utf-8

# In[129]:


import numpy as np
from collections import namedtuple
vec3 = namedtuple('vec3', ['x', 'y', 'z'])


# In[130]:


# Input mesh filename
obj_input = "bunny.obj"
# Output mesh filename
obj_output = "output.obj"
# Min and max points to define the axis aligned box that will intersect the mesh.
box_min = vec3( -0.11, +0.10, 0.00 )
box_max = vec3( -0.04, +0.17, +0.06 )
#box_min = vec3 ( -1, -1, -1)
#box_max = vec3 ( 1, 1, 1)


# In[131]:


# Count the vertices in the input file
v_count = sum ( line [ :2 ] == "v " for line in open ( obj_input, 'r' ) )


# In[132]:


# Initialise an array of 64bit ints, pre-sized to the input file's vertex count
v_array = np.zeros(v_count, dtype=np.uint64)
# Define binary flags to assosiate with each vertex, to record and later determine if vertices are inside
# the box and/or if they are to be present in the output file.
INSIDE = np.uint64 ( 1 << 62 )
USED = np.uint64 ( 1 << 63 )


# In[133]:


# Function that takes x, y and z values of a vertex and returns if the vertex is located inside the box.
def vInsideBox(v):
    if (( box_min.x <= v.x <= box_max.x ) and
        ( box_min.y <= v.y <= box_max.y ) and
        ( box_min.z <= v.z <= box_max.z ) ):
        return True
    else:
        return False


# In[134]:


v_index = 0
for line in open ( obj_input, 'r' ):
    if ( line [:2] == "v " ):
        v_index += 1
        v_pos = line [ 2: ].rstrip ( "\n" ).split ( " " )
        v_pos = vec3 ( float ( v_pos [0] ), float( v_pos [1] ), float ( v_pos [ 2 ] ) )
        if ( vInsideBox ( v_pos ) ):
            v_array [ v_index - 1 ] = INSIDE
    if ( line [ :2 ] == "f " ):
        vInsideCount = 0
        f_vIndex = [ 0, 0, 0 ]
        f_data = line [ 2: ].rstrip ( "\n" ).split ( " " )
        for i in range ( 3 ):
            f_vIndex  [ i ] = int ( f_data [ i ].split ( '/' ) [ 0 ] )
            #f_vtIndex [ i ] = int ( f_data [ i ].split ( '/' ) [ 1 ] )
            #f_vnIndex [ i ] = int ( f_data [ i ].split ( '/', 1 ) [ 0 ] )
            if ( v_array [ f_vIndex [ i ] - 1 ] & INSIDE ):
                vInsideCount += 1
        if ( vInsideCount >= 2 ):
            for i in range ( 3 ):
                v_array [ f_vIndex [ i ] - 1 ] = v_array [ f_vIndex [ i ] - 1 ] | USED


# In[135]:


v_oldIndex = 0
v_newIndex = 0
output = open ( obj_output, 'w' )
output.flush
for line in open ( obj_input, 'r' ):
    if ( line [ :2 ] == "v " ):
        v_oldIndex += 1
        if ( v_array [ v_oldIndex - 1 ] & USED ):
            v_newIndex += 1
            v_array [ v_oldIndex - 1 ] = np.uint64 ( v_newIndex ) | USED
            output.write ( line )

for line in open ( obj_input, 'r' ):
    if ( line [ :2 ] == "f " ):
        f_vIndex = [ 0, 0, 0 ]
        f_data = line [ 2: ].rstrip ( "\n" ).split ( " " )
        for i in range ( 3 ):
            f_vIndex  [ i ] = int ( f_data [ i ].split ( '/' ) [ 0 ] )
        if ( v_array [ int ( f_vIndex [ 0 ] ) - 1 ] & USED ):
            if ( v_array [ int ( f_vIndex [ 1 ] ) - 1 ] & USED ):
                if ( v_array [ int ( f_vIndex [ 2 ] ) - 1 ] & USED ):
                    output.write ( "f {} {} {}\n".format ( 
                        str ( v_array [ f_vIndex [ 0 ] - 1 ] & ~( 1 << 63 ) ), 
                        str ( v_array [ f_vIndex [ 1 ] - 1 ] & ~( 1 << 63 ) ),
                        str ( v_array [ f_vIndex [ 2 ] - 1 ] & ~( 1 << 63 ) ) ) )


# In[1]:


from PyGEL3D import js
from PyGEL3D import gel
js.set_export_mode ( )
mesh = gel.obj_load ( "output.obj" )
js.display( mesh, smooth=False )


# In[ ]:




