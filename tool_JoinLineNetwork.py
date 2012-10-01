import rhinoscriptsyntax as rs
import Convert
import GeometryOperations
from System.Drawing import Color


DEBUG = False

def main():
    
    linesGUID = rs.GetObjects("Lines", 4)
    Distance =  rs.GetReal("Critical Distance between points")
    
    if linesGUID == None or Distance == None:
        return 
    
    else:
        
        join(linesGUID, Distance)
    


def join(linesGUID, Distance):
    
    if DEBUG:
        reload(Convert)
        reload(GeometryOperations)
    
    Dist = Distance # critical distance

    LAYER_network       = "Lines-Network"

    LAYER = LAYER_network
    if not rs.IsLayer(LAYER):
        rs.AddLayer(LAYER)
        rs.LayerColor(LAYER, Color.FromArgb(100,100,100))
        rs.LayerPrintColor(LAYER, Color.FromArgb(0,0,0))
    
    
    # Collect Points
    
    pts = []
    
    for lineGUID in linesGUID:
        
        if rs.CurveLength(lineGUID)< Dist/2:
            # if distance is shorter than half the criticl one then 
            # i ma removeing it from system 
            linesGUID.remove(lineGUID)
            
        else:
            
            ptStart = rs.CurveStartPoint(lineGUID)
            ptEnd =  rs.CurveEndPoint(lineGUID)
            
            pts.append(ptStart)
            pts.append(ptEnd)
            
            
    
    # I find clusters.
    
    clusters = []

    for pt in pts:
        
        boolNoInRange = True
        
        for cluster in clusters:
            
            if cluster.isPointInRange(pt):
                
                cluster.addPoint(pt)
                boolNoInRange = False
            
        if boolNoInRange:
            
            cluster = csCircleCluster(pt, Dist/2)
            clusters.append(cluster)
            
            
            
    
    """
    
    Now i have collected all clusters
    
    """
    
    """
    
    For debugin perpos i will draw circles around clusters 
    
    """
    if DEBUG:
        
        for cluster in clusters:
            
            rs.AddCircle(rs.PlaneFromFrame(cluster.ptCenter, (1,0,0), (0,1,0)), cluster.radius)
            
    """
    
    I evaluate all lines in network and change start and end points so that they all meet up
    
    """
    
    for lineGUID in linesGUID:
        
        ptsList = rs.CurveEditPoints(lineGUID)
        ptsList = Convert.Point3dListTo3DList(ptsList)
        
        ptStart = ptsList[0]
        ptEnd   = ptsList[-1]
        
        boolStartArrow  = False
        boolEndArrow    = False
        
        boolStartDone   = False
        boolEndDone     = False
        
        for cluster in clusters:
            
            if cluster.isPointInRange(ptStart):
                
                ptStart = cluster.ptCenter 
                
                if len(cluster.pts) == 1:
                    
                    boolStartArrow = True
                    
                boolStartDone = True
            
            if cluster.isPointInRange(ptEnd):
                
                ptEnd = cluster.ptCenter 
                
                if len(cluster.pts) == 1:
                    
                    boolEndArrow = True
                    
                boolEndDone = True
            
            
            if boolStartDone and boolEndDone:
                break
            
        # rebuild polyline, i ma not constructing curves
        
        ptsList[0]      = ptStart
        ptsList[-1]     = ptEnd
        
        GUID = rs.AddPolyline(ptsList)
        rs.ObjectLayer(GUID, LAYER_network)
        
        if boolStartArrow and not boolEndArrow:
            
            rs.CurveArrows(GUID, 1)
            
        if not boolStartArrow and boolEndArrow:
            
            rs.CurveArrows(GUID, 2)
            
        if boolStartArrow and boolEndArrow:
            
            rs.CurveArrows(GUID, 3)



class csCircleCluster:
    
    def __init__(self, pt, radius):
        
        
        # pt : Rhino.Geometry.Point3d
        # radius : float
        
        pt3D = Convert.Point3dToP3D(pt)
        
        self.ptCenter =  pt3D
        self.radius =  radius
        self.pts = [pt3D]
        
    def addPoint(self, pt):
        
        pt3D = Convert.Point3dToP3D(pt)
        
        self.pts.append(pt3D)
        # find new center
        
        self.ptCenter =  GeometryOperations.midPoint(self.pts)
        
    def isPointInRange(self, pt):
    
        boolIsCloseToEveryone = True
        
        for ptMemeber in self.pts:
            
            # I evaluate if there is some distance larger than critical distance, if yes it is not part fo cluster.
            
            if GeometryOperations.distance2Points(ptMemeber, pt) > self.radius*2:
            
                boolIsCloseToEveryone = False
                break
            
        
        if boolIsCloseToEveryone:
            
            return True
            
        else:
        
            return False
        


if __name__ == "__main__":
    main()