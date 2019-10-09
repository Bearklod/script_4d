import c4d
from c4d import gui

def press_button():
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):        
        if bc[c4d.BFM_INPUT_QUALIFIER]==1:            
            press_shift = 1
        else:
            press_shift = 0
        return press_shift

def lenEdg(obj):
    lst = []
    pt = tuple(obj.GetAllPoints())

    for i in range(len(pt)-1):
        lst.append(round((pt[i+1]-pt[i]).GetLength()))
    return tuple(lst)

def sameSelection(obj, pCount, lenLst, bBox, button):
    while obj:        
        if obj.GetType() == 5100:        
            #print obj.GetName()
            if not button:        
                if pCount == obj.GetPolygonCount() and lenLst == lenEdg(obj):
                    obj.SetBit(c4d.BIT_ACTIVE)
                    sameSelection(obj.GetDown(), pCount, lenLst, bBox, button)
                obj = obj.GetNext()
            else:
                if bBox == obj.GetRad():
                     obj.SetBit(c4d.BIT_ACTIVE)
        else:
            sameSelection(obj.GetDown(), pCount, lenLst, bBox, button)
            obj = obj.GetNext()        

def main():
    #c4d.CallCommand(13957)
    button = press_button()
    objs = doc.GetActiveObjects(1)
    for obj in objs:
        if obj == None or obj.GetType() != 5100:
            return
        pCount = obj.GetPolygonCount()
        lenLst = lenEdg(obj)
        bBox = obj.GetRad()
    
        sameSelection(doc.GetFirstObject(), pCount, lenLst, bBox, button)
    

    
    c4d.EventAdd() 
 




    

if __name__=='__main__':
    main()
