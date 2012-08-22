import rhinoscriptsyntax as rs

def clicker():

    start = rs.GetInteger("Start Number")
    textHeight =  rs.GetReal("Text Height")
    
    pt = rs.GetPoint("Get Point")
    
    i = start
    
    while pt != None:
        
        rs.AddText(str(i),pt,textHeight,"Arial",0,2)
        
        i += 1
        
        pt = rs.GetPoint("Get Point")

        
        
if __name__ == "__main__":
    
    clicker()