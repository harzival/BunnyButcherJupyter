#!/usr/bin/env python
# coding: utf-8

# In[23]:


from PyGEL3D import js
from PyGEL3D import gel
import numpy as np
import pymesh
js.set_export_mode()


# In[24]:


bunny = pymesh.load_mesh("HDbunny/bunny.obj")


# In[25]:


bunny.get_attribute_names()


# In[26]:


box_min = np.array([ -0.11, +0.10, -0.01 ])
box_max = np.array([ -0.04, +0.17, +0.06 ])
box = pymesh.generate_box_mesh(box_min, box_max)


# In[27]:


intersection = pymesh.boolean(box, bunny, "intersection", "carve")


# In[28]:


intersection.get_attribute_names()


# In[29]:


pymesh.save_mesh("output2.obj", intersection, *intersection.get_attribute_names())


# In[ ]:


mesh = gel.obj_load("output2.obj")
js.display(mesh, smooth=False)

