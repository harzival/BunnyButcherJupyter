#!/usr/bin/env python
# coding: utf-8

# In[34]:


from PyGEL3D import js
from PyGEL3D import gel
import numpy as np
import pymesh
js.set_export_mode()


# In[35]:


box_min = np.array ( [ -0.11, +0.10, -0.01 ] )
box_max = np.array ( [ -0.04, +0.17, +0.06 ] )
box = pymesh.generate_box_mesh ( box_min, box_max )


# In[36]:


bunny = pymesh.load_mesh ( "bunny.obj" )


# In[37]:


intersection = pymesh.boolean ( box, bunny, "intersection", "carve")


# In[38]:


pymesh.save_mesh("output.obj", intersection, ascii=True)


# In[39]:


mesh = gel.obj_load("output.obj")
js.display(mesh, smooth=False)

