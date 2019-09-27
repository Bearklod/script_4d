"""
getLenSetLen
Get or set Length from selected edges or splines
 
"""

import c4d
from c4d import gui
from c4d import utils


def press_button():
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):

        if bc[c4d.BFM_INPUT_QUALIFIER]==1:
            press_shift = 1
        else:
            press_shift = 0
        return press_shift


def sendModCom(obj):
    utils.SendModelingCommand(command = c4d.MCOMMAND_EDGE_TO_SPLINE,
                                        list = [obj],
                                        mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                        doc = None)  
    

def setLen(obj, leng): 

    if obj.GetType() == 5101:
        leng.Init(obj)
        l = round(leng.GetLength(),2)
        
    elif obj.GetType() == 5100:
        es = obj.GetEdgeS()
        
        if not es.GetCount():
            return
        
        sendModCom(obj)
    
        spl = obj.GetDown()
        leng.Init(spl)
        l = round(leng.GetLength(),2)
        spl.Remove()
    else: return
    
    try:
        need = float(c4d.gui.InputDialog('no David Blaine, no', 100))
    except ValueError:       
        return
    


    obj.SetRelScale(c4d.Vector(need/l))


def getLen(obj, leng):
    scale = obj.GetRelScale().x
    if obj.GetType() == 5101:
        leng.Init(obj)
        output = round(leng.GetLength(),2)*scale
        gui.MessageDialog('{} {}'.format(output, 'cm'))

    elif obj.GetType() == 5100:
        es = obj.GetEdgeS()
        if not es.GetCount():
            return
        
        sendModCom(obj)

        spl = obj.GetDown()
        leng.Init(spl)
        output = round(leng.GetLength(),2)*scale
        gui.MessageDialog('{} {}'.format(output, 'cm'))
        spl.Remove()


def main():

    c4d.CallCommand(13957)
    obj = doc.GetActiveObject()
    if not obj:
        return
    leng = c4d.utils.SplineLengthData()

    if press_button():
        setLen(obj, leng)
    else:
        getLen(obj, leng)

    c4d.EventAdd()


if __name__=='__main__':
    main()
