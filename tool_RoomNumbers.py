
import Rhino
import System.Drawing
import Rhino.Geometry as RG
import rhinoscriptsyntax as rs

def main():
    
    prefix =  rs.GetString("Prefix: ")
    counter =  rs.GetInteger("Counter: ")
    
    text = prefix + str(counter)
            
    while drawNames(text) == True:
        
        counter += 1
        text = prefix + str(counter)
        

def drawNames(text):
    
    global ptStart 
    global vecToStart
    global txtNumber
    txtNumber = text
    
    # first point
    
    gp = Rhino.Input.Custom.GetPoint()
    gp.DynamicDraw += GetStartPointDynamicDraw
    
    if gp.Get() == Rhino.Input.GetResult.Cancel:
        
        print("Stop")
        return False
    
    ptStart = gp.Point() # : Point3d
    
    vecToStart = Rhino.Geometry.Vector3d(ptStart)
    
    # second Point
    
    gp = Rhino.Input.Custom.GetPoint()
    gp.DynamicDraw += GetEndPointForText
    if gp.Get() == Rhino.Input.GetResult.Cancel:
        
        print("Stop")
        return False
        
    
    ptEnd = gp.Point() # : Point3d
    
    
    vecNormal =  Rhino.Geometry.Vector3d(0,0,1)
    vecA = Rhino.Geometry.Vector3d(ptEnd)

    vecApproach = vecA - vecToStart
    vecApproach.Unitize()
    
    vecOritation =  Rhino.Geometry.Vector3d.CrossProduct(vecNormal, vecApproach)
    vecOritation.Unitize()
    
    ptOnXAxe = RG.Point3d.Add(ptEnd, vecApproach)
    ptOnYAxe = RG.Point3d.Add(ptEnd, vecOritation)
    
    vecTextLeft = RG.Vector3d.Multiply(len(txtNumber)*0.7, vecApproach)
    vecTextLeft.Reverse()
    
    vecTextUp =  RG.Vector3d.Multiply(0.5, vecOritation)
    
    ptTextLeft =  RG.Point3d.Add(ptEnd, vecTextLeft)
    ptTextUp = RG.Point3d.Add(ptTextLeft, vecTextUp)
    
    R3P = Rhino.Geometry.Plane(ptTextUp,vecApproach,vecOritation)
    
    rs.AddText(txtNumber, R3P, 0.8)
    
    return True
    


def GetEndPointForText(sender, args):
    #pt1  = Rhino.Geometry.Point3d(0,0,0)

    vecNormal =  Rhino.Geometry.Vector3d(0,0,1)
    vecA = Rhino.Geometry.Vector3d(args.CurrentPoint)

    vecApproach = vecA - vecToStart
    vecApproach.Unitize()
    
    vecOritation =  Rhino.Geometry.Vector3d.CrossProduct(vecNormal, vecApproach)
    vecOritation.Unitize()
    
    ptOnXAxe = RG.Point3d.Add(args.CurrentPoint, vecApproach)
    ptOnYAxe = RG.Point3d.Add(args.CurrentPoint, vecOritation)
    
    args.Display.DrawLine(ptStart, args.CurrentPoint,  System.Drawing.Color.Gray, 1)
    
    args.Display.DrawLine(args.CurrentPoint, ptOnXAxe,  System.Drawing.Color.Red, 2)
    args.Display.DrawLine(args.CurrentPoint, ptOnYAxe,  System.Drawing.Color.Green, 2)
    
    
    vecTextLeft = RG.Vector3d.Multiply(len(txtNumber)*0.7, vecApproach)
    vecTextLeft.Reverse()
    
    vecTextUp =  RG.Vector3d.Multiply(0.5, vecOritation)
    
    ptTextLeft =  RG.Point3d.Add(args.CurrentPoint, vecTextLeft)
    ptTextUp = RG.Point3d.Add(ptTextLeft, vecTextUp)
    
    R3P = Rhino.Geometry.Plane(ptTextUp,vecApproach,vecOritation)
    
    args.Display.Draw3dText(txtNumber, System.Drawing.Color.White, R3P, 0.8, "Arial")
    

def GetStartPointDynamicDraw(sender, args ):
    
    rCircle =  Rhino.Geometry.Circle(args.CurrentPoint, 0.8) 
    args.Display.DrawCircle(rCircle, System.Drawing.Color.Blue, 2)


if __name__ == "__main__":
    main()