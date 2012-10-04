"""
Created on Jul 9, 2012
@author: raul

"""


import rhinoscriptsyntax as rs
from System.Drawing import Color
import GeometryOperations
import Rhino

print("Draw module")
print("version: 2012/07/09")
print("")


def drawCuverDirection(curveGUID):
    
    if not rs.IsLayer("fab-Direction"):
        
        rs.AddLayer("fab-Direction")
        rs.LayerColor("fab-Direction", Color.FromArgb(100,180 ,180))
        
    
    pts =  rs.CurveEditPoints(curveGUID)
    
    if pts != None:
        
        arrow = rs.AddLine(pts[0], pts[1])
        arrow = rs.ScaleObject(arrow, pts[0], (0.3, 0.3, 0.3))
        print(rs.CurveArrows(arrow, 2))
        
        rs.ObjectLayer(arrow, "fab-Direction")

def drawCurveArrow(_curve, _size, _direction=0):
    
    '''
    parameters: _curveGUID
                _size
                _direction
                            0 = start
                            1 = end
    
    return:    
    
    
                            
    '''
    
    
    
    
    
    print("WIP")




def drawVector(vector, origin):
    
    """
    this function draws vector in rhino
    
    """
    
    layerName = "Annotation-Vector"
    if not rs.IsLayer(layerName):
        
        rs.AddLayer(layerName)
        rs.LayerColor(layerName, Color.FromArgb(150,50,50))
    
    print(rs.VectorLength(vector))
    
    lineID = rs.AddLine(origin, GeometryOperations.movePoint(origin, vector))
    
    rs.CurveArrows(lineID, 2)
    rs.ObjectLayer(lineID, layerName)
    rs.ObjectColor(lineID, (150,150,150))
    
    return lineID

def drawFrame(_plane, _scale):
    
    # Annotation Layer
    
    layerName = "Annotation-Frame"
    rs.EnableRedraw(False)
    
    if not rs.IsLayer(layerName):
        
        rs.AddLayer(layerName)
        rs.LayerColor(layerName, Color.FromArgb(100,100,100))
    
    ptPointOnXAxe           = GeometryOperations.movePoint(_plane[0], _plane[1])
    ptPointOnYAxe           = GeometryOperations.movePoint(_plane[0], _plane[2])
    ptPointOnZAxe           = GeometryOperations.movePoint(_plane[0], _plane[3])
    
    x = rs.AddLine(_plane[0], ptPointOnXAxe)
    rs.ScaleObject(x, _plane[0], (_scale,_scale,_scale))
    rs.CurveArrows(x,2)
    
    y = rs.AddLine(_plane[0], ptPointOnYAxe)
    rs.ScaleObject(y, _plane[0], (_scale,_scale,_scale))
    rs.CurveArrows(y,2)
    
    z = rs.AddLine(_plane[0], ptPointOnZAxe)
    rs.ScaleObject(z, _plane[0], (_scale,_scale,_scale))
    rs.CurveArrows(z, 2)
    
    rs.ObjectColor(x, (200,100,100))
    rs.ObjectColor(y, (100,200,100))
    rs.ObjectColor(z, (100,100,200))
    
    rs.ObjectLayer(x,layerName)
    rs.ObjectLayer(y,layerName)
    rs.ObjectLayer(z,layerName)
    
    rs.AddGroup("Annotation-Frame")
    rs.AddObjectsToGroup((x,y,z),"Annotation-Frame")
    rs.EnableRedraw(True)

def drawPalneAxeAndArrows(_plane, _scale):
    
    # Annotation Layer
    
    layerName = "Annotation-Axe"
    
    if not rs.IsLayer(layerName):
        
        rs.AddLayer(layerName)
        rs.LayerColor(layerName, Color.FromArgb(100,100,100))
    
    ptPointOnXAxe           = GeometryOperations.movePoint(_plane[0], _plane[1])
    ptPointOnYAxe           = GeometryOperations.movePoint(_plane[0], _plane[2])
    ptPointOnZAxe           = GeometryOperations.movePoint(_plane[0], _plane[3])
    
    x = rs.AddLine(_plane[0], ptPointOnXAxe)
    rs.ScaleObject(x, _plane[0], (_scale,_scale,_scale))
    rs.CurveArrows(x,2)
    
    y = rs.AddLine(_plane[0], ptPointOnYAxe)
    rs.ScaleObject(y, _plane[0], (_scale,_scale,_scale))
    rs.CurveArrows(y,2)
    
    z = rs.AddLine(_plane[0], ptPointOnZAxe)
    rs.ScaleObject(z, _plane[0], (_scale,_scale,_scale))
    rs.CurveArrows(z, 2)
    
    
    rs.ObjectColor(x, (200,100,100))
    rs.ObjectColor(y, (100,200,100))
    rs.ObjectColor(z, (100,100,200))
    
    
    rs.ObjectLayer(x,layerName)
    rs.ObjectLayer(y,layerName)
    rs.ObjectLayer(z,layerName)
    
    
    rs.AddGroup("Annotation-Plane")
    rs.AddObjectsToGroup((x,y,z),"Annotation-Plane")
    
def drawTextCenter(_multiline, _rowheight, _FRAME_Dest, _LayerName, _GroupName):
    

    """ 
    
    _multiline # []
    
    """

    rs.EnableRedraw(False)

    _multiline =  _multiline[::-1]

    tolatHeight =  len(_multiline) * _rowheight * 1.3 # there is 20 extra space per line
    
    Text = []
    
    for rowIndex in range(len(_multiline)):
        
        letterY = rowIndex * _rowheight * 1.3 - (tolatHeight/2)
        
        row =  _multiline[rowIndex]
    
        rowWidth =  len(row) * _rowheight
        
        for letterIndex in range(len(row)):

            letterX =  letterIndex*_rowheight - ( rowWidth/2 )
            
            newLetters = drawLetter(row[letterIndex], _rowheight, letterX, letterY) # <- this is list 
            
            Text.append(newLetters)
    
    # Transform Letter components to right place
    
    FRAME_base = rs.PlaneFromFrame((0,0,0), (1,0,0), (0,1,0))
    
    for Letter in Text:
        
        for GUID_segment in Letter:

            TRANSFORM = Rhino.Geometry.Transform.ChangeBasis(_FRAME_Dest, FRAME_base)
            rs.TransformObject(GUID_segment, TRANSFORM, False)
            rs.ObjectLayer(GUID_segment, _LayerName)
            rs.AddObjectToGroup(GUID_segment, _GroupName)


    rs.EnableRedraw(True)

def drawLetter(_letter, scale, x, y):
    
    SQ  = 0.12  *scale
    W   = 0.6   *scale
    H   = 1.0   *scale
    L   = 0.6   *scale 
     
    # Matrix
     
    D = {}  # [ 5 x 7 ]
     
    j = 0
    jValue = y
    
    D[(0,j)] = (x        ,jValue, 0)
    D[(1,j)] = (x+SQ     ,jValue, 0)
    D[(2,j)] = (x+W/2    ,jValue, 0)
    D[(3,j)] = (x+W-SQ   ,jValue, 0)
    D[(4,j)] = (x+W      ,jValue, 0)
    
    j = 1
    jValue = SQ + y
    
    D[(0,j)] = (x        ,jValue, 0)
    D[(1,j)] = (x+SQ     ,jValue, 0)
    D[(2,j)] = (x+W/2    ,jValue, 0)
    D[(3,j)] = (x+W-SQ   ,jValue, 0)
    D[(4,j)] = (x+W      ,jValue, 0)
    
    j = 2
    jValue = L-SQ + y
    
    D[(0,j)] = (x        ,jValue, 0)
    D[(1,j)] = (x+SQ     ,jValue, 0)
    D[(2,j)] = (x+W/2    ,jValue, 0)
    D[(3,j)] = (x+W-SQ   ,jValue, 0)
    D[(4,j)] = (x+W      ,jValue, 0)
    
    j = 3
    jValue = L + y
    
    D[(0,j)] = (x      ,jValue, 0)
    D[(1,j)] = (x+SQ     ,jValue, 0)
    D[(2,j)] = (x+W/2    ,jValue, 0)
    D[(3,j)] = (x+W-SQ   ,jValue, 0)
    D[(4,j)] = (x+W      ,jValue, 0)
    
    j = 4
    jValue = L+SQ +  y
    
    D[(0,j)] = (x        ,jValue, 0)
    D[(1,j)] = (x+SQ     ,jValue, 0)
    D[(2,j)] = (x+W/2    ,jValue, 0)
    D[(3,j)] = (x+W-SQ   ,jValue, 0)
    D[(4,j)] = (x+W      ,jValue, 0)
    
    j = 5
    jValue = H-SQ + y
    
    D[(0,j)] = (x        ,jValue, 0)
    D[(1,j)] = (x+SQ     ,jValue, 0)
    D[(2,j)] = (x+W/2    ,jValue, 0)
    D[(3,j)] = (x+W-SQ   ,jValue, 0)
    D[(4,j)] = (x+W      ,jValue, 0)
    
    j = 6
    jValue = H + y
    
    D[(0,j)] = (x        ,jValue, 0)
    D[(1,j)] = (x+SQ     ,jValue, 0)
    D[(2,j)] = (x+W/2    ,jValue, 0)
    D[(3,j)] = (x+W-SQ   ,jValue, 0)
    D[(4,j)] = (x+W      ,jValue, 0)
     
    # Letter index
     
#    for i in range(5):
#        for j in range(7):
#     
#            rs.AddTextDot(str(j) + "," + str(i), D[(i,j)])
     
    # 8
     
    Letter = {}


    Letter['0'] =  (
            
            ((0,1),(1,0)),
            ((1,0),(3,0)),
            ((3,0),(4,1)),
            ((4,1),(4,5)),
            ((4,5),(3,6)),
            ((3,6),(1,6)),
            ((1,6),(0,5)),
            ((0,5),(0,1))
     
          )
    
     
    Letter['1'] =  (
            
            ((1,5),(2,6)),
            ((2,6),(2,0)),
            ((1,0),(3,0))
            
            )
    
     
    Letter['2'] =  (
            
            ((0,5),(1,6)),
            ((1,6),(3,6)),
            ((3,6),(4,5)),
            ((4,5),(4,4)),
            ((4,4),(0,0)),
            ((0,0),(4,0)),
            ((4,0),(4,1))

            )


    Letter['3'] =  (
            
            ((0,5),(1,6)),
            ((1,6),(3,6)),
            ((3,6),(4,5)),
            ((4,5),(4,4)),
            ((4,4),(3,3)),
            ((3,3),(4,2)),
            ((4,2),(4,1)),                        
            ((4,1),(3,0)),
            ((3,0),(1,0)),
            ((1,0),(0,1))
                                                            
            
          )

    Letter['4'] =  (
            
            ((3,6),(1,6)),    
            ((1,6),(0,5)),       
            ((0,5),(0,3)),       
            ((0,3),(3,3)),              
            ((3,3),(3,0))               
            
                       
           )
    
    Letter['5'] =  (
            
            ((4,6),(0,6)),
            ((0,6),(0,3)),
            ((0,3),(3,3)),
            ((3,3),(4,2)),
            ((4,2),(4,1)),
            ((4,1),(3,0)),
            ((3,0),(1,0)),
            ((1,0),(0,1))
   
            )
            

    Letter['6'] =  (
            
            ((4,5),(3,6)),
            ((3,6),(1,6)),
            ((1,6),(0,5)),
            ((0,5),(0,1)),            
            ((0,1),(1,0)),
            ((1,0),(3,0)),            
            ((3,0),(4,1)),
            ((4,1),(4,2)),                                       
            ((4,2),(3,3)),
            ((3,3),(1,3)),            
            ((1,3),(0,2))
            
                        
          )
   
   
    Letter['7'] =  (
            
            ((0,5),(1,6)),
            ((1,6),(3,6)),
            ((3,6),(4,5)),
            ((4,5),(0,0))
   
           )
    
    
    Letter['8'] = (
          
           ((3,3),(1,3)),
           ((1,3),(0,2)),
           ((0,2),(0,1)),
           ((0,1),(1,0)),
           ((1,0),(3,0)),
           ((3,0),(4,1)),
           ((4,1),(4,2)),
           ((4,2),(3,3)),
           ((3,3),(4,4)),
           ((4,4),(4,5)),
           ((4,5),(3,6)),
           ((3,6),(1,6)),
           ((1,6),(0,5)),
           ((0,5),(0,4)),
           ((0,4),(1,3))
          
           
          )
    
    Letter['9'] =  (
            
            ((0,1),(1,0)),
            ((1,0),(3,0)),
            ((3,0),(4,1)),
            ((4,1),(4,5)),
            ((4,5),(3,6)),
            ((3,6),(1,6)),
            ((1,6),(0,5)),
            ((0,5),(0,4)),
            ((0,4),(1,3)),
            ((1,3),(3,3)),
            ((3,3),(4,4)),

           )
    

    #rs.AddLine(D[ L8[0][0] ], D[ L8[0][1] ]) 
    
    GUID_Letter = []
    
    for i in Letter[_letter]:
        
        GUID_Letter.append( rs.AddLine(D[i[0]], D[i[1]]) )
    
    
    #print(GUID_Letter)
    
    return GUID_Letter
    
    
    


