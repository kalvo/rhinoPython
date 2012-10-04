"""
Created on Jul 9, 2012
@author: raul

"""

import rhinoscriptsyntax as rs
import scriptcontext
import Draw
import math


print("Geometry Operations module")
print("version: 2012/08/13")
print("")


def lineEndPoints( _lineGUID ):

    return ( rs.CurveStartPoint(_lineGUID), rs.CurveEndPoint(_lineGUID) ) # return tuple of end points

def offsetPlane(_plane, _distance):   
 
    ptOrigin            = _plane[0]
    ptOriginID          = rs.AddPoint(ptOrigin)
    vecTransform        = rs.VectorScale(_plane[3], _distance)
    ptOriginMoved       = rs.MoveObject(ptOriginID, vecTransform)
    planeMoved          = rs.MovePlane(_plane, ptOriginMoved)

    rs.DeleteObject(ptOriginID)
    return              planeMoved

def offsetPolyline(_polylineGUID, _offsetDistance):
    
    # works for CONVEX
    # offset direction is inwards
    
    # parameters:
    #               _polylineGUID
    #               _offsetDistance 
    #
    
    # version: 2012/07/05A
    
    
    name = "offsetPolyline"
    debug = False
    
    # EVALUATION
    
    doc = scriptcontext.doc    
    obj = doc.Objects.Find(_polylineGUID)
    
    if obj == None:
        
        print(name + ": No Object")
    
    crv = obj.CurveGeometry
    if not crv.IsPolyline():
        
        print(name + ": Curve is not polyline")
        return None
    
    if not crv.IsClosed:
        
        print(name + ": Curve is not closed")
        d = crv.PointAtEnd.DistanceTo(crv.PointAtStart)
        
        return None
    
    L = []
    
    pts= rs.CurvePoints(_polylineGUID)
    
    for i in range((len(pts)-1)):

        #print("")
        
        iP =  (i-1) % (len(pts)-1)
        iC =  (i+1) % (len(pts)-1)
        iN =  (i+2) % (len(pts)-1)
        
        #print(str(iP) + " " + str(i) + " " + str(iC)+ " " + str(iN))
        
        v1 = rs.VectorCreate(pts[iP], pts[i])
        v2 = rs.VectorCreate(pts[iN], pts[iC])

        
        a1 = rs.VectorAngle(v1,v2)
        a2 = rs.VectorAngle(rs.VectorReverse(v1),v2)
        
        if a1 < a2:
            if debug:
                print(str(a1) + " < " +  str(a2))
            # use first
            
        else:
            
            v1 = rs.VectorReverse(v1)
            if debug:
                print(str(a2) + " < " +  str(a1))
            # use second
        
        v = ((v1[0] + v2[0])/2, (v1[1] + v2[1])/2,(v1[2] + v2[2])/2)
        
        vY =  rs.VectorUnitize(v)
        vX = rs.VectorCreate(pts[i], pts[iC])
        vZ=  rs.VectorCrossProduct(vX, vY)
        
        ptMid =  ((pts[i][0] + pts[iC][0])/2, (pts[i][1] + pts[iC][1])/2, (pts[i][2] + pts[iC][2])/2)  
        
        p = rs.PlaneFromNormal(ptMid, vZ, vX)
        
        
        #DEBUG
        if debug:
            Draw.drawPalneAxeAndArrows(p, _offsetDistance)
            # make sure green arrawsa are pointing inwards
        
    
        ptA = movePoint(pts[i], rs.VectorScale( rs.VectorUnitize( p[2] ), _offsetDistance))
        ptB = movePoint(pts[iC], rs.VectorScale( rs.VectorUnitize( p[2] ), _offsetDistance))
        
        ln =  rs.AddLine(ptA, ptB)
        
        L.append(ln)
            
    
    P = []
    
    for i in range(len(L)):
        
        lineAPts =  lineEndPoints(L[i])
        lineBPts =  lineEndPoints(L[(i+1) % len(L)])
        
        intersection = rs.LineLineIntersection((lineAPts[0], lineAPts[1]), (lineBPts[0],lineBPts[1]))
        
        ptI = intersection[0]
        
        P.append(ptI)
        
    rs.DeleteObjects(L)
    
    P.append(P[0])
    
    return rs.AddPolyline(P)
    
def intersectLineSurface( _line3f, _SurfaceID):
    
    #     parameter:
    #     _line3D [L3D]
    #    _Surface [ID/String]
    #    return:
    #    pt [P3D]
    
    
    rs.EnableRedraw         = False

    ptLineStartP3D          = _line3f[0] # it do not matte which point we pick sinde line is consider as ray
    
    print(_SurfaceID)
    ptSurfaceEditpoints     = rs.SurfaceEditPoints(_SurfaceID)
    
    
    maxDistance             = -1
    
    for pt in ptSurfaceEditpoints:
        
        d                   = rs.Distance(ptLineStartP3D, pt)
        
        if d > maxDistance:
            
            maxDistance     = d
    
    
    magnitud                = maxDistance / 10
    
    
    vecLineDirection        = rs.VectorCreate(ptLineStartP3D, _line3f[1])
    vecLineDirection        = rs.VectorUnitize (vecLineDirection)
    vecLineDirection        = rs.VectorScale( vecLineDirection, magnitud)
    
    lineIntersectionID      = rs.AddLine ( ptLineStartP3D, movePoint(ptLineStartP3D, vecLineDirection))
    
    ptIntersection          = rs.CurveSurfaceIntersection(lineIntersectionID,  _SurfaceID )
    
    if len(ptIntersection) ==  0:
        # no intersection
        # we try no other side
        
        rs.DeleteObject(lineIntersectionID)
        vecLineDirection    = rs.VectorReverse( vecLineDirection )
        lineIntersectionID  = rs.AddLine ( ptLineStartP3D, movePoint(ptLineStartP3D, vecLineDirection))
        
        ptIntersection          = rs.CurveSurfaceIntersection(lineIntersectionID,  _SurfaceID )
        
        
    rs.DeleteObject(lineIntersectionID)
    
    rs.EnableRedraw         = True
    
    if len(ptIntersection) ==  0:
        return None
    else:
        return ptIntersection[0][1]

def movePoint(_pt3f, _vector3f):
    
    # return point3f
    
    pt =  ( _pt3f[0] + _vector3f[0], _pt3f[1] + _vector3f[1], _pt3f[2] + _vector3f[2])
    return pt

def movePointAlongLine(_startPoint, _endPoint, _fraction):
    
    """
    
    move start point of line along line to end Point
    
    fraction = [0 -> 1]
    
    Return
    
        pt : (x:float, y:float,z:float)
    
    """
    
    if _fraction >1 : 
        _fraction = 1
        
    if _fraction < 0:
        _fraction = 0
        
        
    x = _startPoint[0] + (_endPoint[0] - _startPoint[0])*_fraction
    y = _startPoint[1] + (_endPoint[1] - _startPoint[1])*_fraction
    z = _startPoint[2] + (_endPoint[2] - _startPoint[2])*_fraction
    
    return (x,y,z)
    
def buildSmoothCurve(_pts):
    
    """
    
    buildSmoothCurve ( pts : []
    
    """
    
    
    # parameters: corner points
    
    # return curve
    
    lnList = []
    for i in range(len(_pts)-1):
        
        #print(i)
        #print(_pts[i])
        #print(_pts[(i+1)])
        
        ln = rs.AddLine(_pts[i], _pts[(i+1)% len(_pts)])
        lnList.append(ln)
        
        
    
    ptList = []
    
    for ln in lnList:
        
        
        d = rs.CurveDomain(ln)
        
        ptStart = rs.EvaluateCurve(ln,d[0] + 0.05*(d[0] + d[1]))
        ptMid = rs.EvaluateCurve(ln,d[0] + 0.5*(d[0] + d[1]))
        ptEnd = rs.EvaluateCurve(ln,d[0] + 0.95*(d[0] + d[1]))
        
        ptList.append(ptStart)
        ptList.append(ptMid)
        ptList.append(ptEnd)
        
        
        
    ptList.append(ptList[0])
    
    rs.DeleteObjects(lnList)
    c = rs.AddCurve(ptList, 2)
    
    return c

    # End

def midPoint(_pts):


    """
    
    parameters: _pts : [(x:float,y:float,z:float)]
    return: pt: (x:float,y:float,z:float)
    
    """
    
    x = 0
    y = 0
    z = 0
    
    
    if len(_pts) == 0:
        
        return None
    
    
    for pt in _pts:
        
        x = x + pt[0]
        y = y + pt[1]
        z = z + pt[2]
    
    
    pt = (x/len(_pts), y/len(_pts), z/len(_pts))

    return pt

def averageVctor(VECTORS):
    
    """
    
        This function takes in all vectors.
        All vectors will be become unite vectors
        All vectors will be summed
        Result vector will be unit vector
    
        parameters
        
            VECTORS : (  (x : float, y : float, z : float) )
    
        return:
        
            vec    # (x : float, y : float, z : float)
        
            return None if there is no list
    
    """
    
    if len(VECTORS) == 0:
        
        return None
    
    v1 = rs.VectorUnitize( VECTORS[0] )
    
    if len(VECTORS) > 1:
        
        for i in range(1,  len(VECTORS) ):
        
            v2      = rs.VectorUnitize(VECTORS[i])
        
            v1      = rs.VectorAdd(v1, v2)
      
    return rs.VectorUnitize(v1)
    
def distance2Points(ptA, ptB):
    
    # ptA : (x:float,y:float,z:float)
    # ptB : (x:float,y:float,z:float)
    
    # return:
    
    # float
    
    D = math.sqrt(((ptA[0] - ptB[0]) * (ptA[0] - ptB[0]))  + ((ptA[1] - ptB[1]) * (ptA[1] - ptB[1])) + ((ptA[2] - ptB[2]) * (ptA[2] - ptB[2])))   
    
    return D


 
    
    
    
    
    
    
    
    
    
    
    
    
    


