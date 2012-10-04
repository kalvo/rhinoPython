'''
Created on Aug 31, 2012

@author: raul
'''


def Point3dListTo3DList(Point3dLis):
    
    listPoint3d = Point3dLis.ToArray()
    
    list3D = []
    
    for RhinoPoint3d in listPoint3d:
        
        p = (RhinoPoint3d.X, RhinoPoint3d.Y, RhinoPoint3d.Z)
        
        list3D.append(p)
    
    return list3D


def Point3dToP3D(RhinoPoint3d):
    
    P = (RhinoPoint3d.X, RhinoPoint3d.Y, RhinoPoint3d.Z)
    
    return P
 