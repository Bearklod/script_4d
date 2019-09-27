import c4d
from c4d import gui
from c4d import utils


def main():
    obj = doc.GetActiveObject()

    if obj == None:
        gui.MessageDialog('=(')
    else:        
        pc = c4d.PointObject.GetPointCount(obj)        
        sel = obj.GetPointS()
        sel.DeselectAll()
        
        itr2 = 0
        while itr2 <= pc:
            itr2 += 1            
            pc = c4d.PointObject.GetPointCount(obj)#point count
            pp = tuple(c4d.PointObject.GetAllPoints(obj))
            for i in range(pc):
                if i == range(pc)[-1]:
                    break
                elif pp[i] == pp[i+1]:
                    sel = obj.GetPointS()
                    sel.Select(i)
                    sel.Select(i+1)
                    c4d.CallCommand(12568)
                    sel.DeselectAll()
                    c4d.EventAdd() 
                    break
                else: continue
                
if __name__=='__main__':
    main()