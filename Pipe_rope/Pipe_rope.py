import c4d
from c4d import gui
from c4d import utils



def len_spline(spline):
    
    if spline.GetType() == 5181:
        lenght = 2*3.14*spline[c4d.PRIM_CIRCLE_RADIUS]
        return lenght
            
    elif spline.GetType() == 5186:
        lenght = (2*spline[c4d.PRIM_RECTANGLE_WIDTH])+(2*spline[c4d.PRIM_RECTANGLE_HEIGHT])
        return lenght
        
    elif spline.GetType() == 5101:    
        leng = c4d.utils.SplineLengthData()    
        leng.Init(spline)
        return leng.GetLength()


def press_button():
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        
        if bc[c4d.BFM_INPUT_QUALIFIER]==1:            
            press_shift = 1
        else:
            press_shift = 0
        return press_shift

def obj_list():
    objs = doc.GetActiveObjects(1)
    for obj in objs:
        if obj.GetUp():
            if obj.GetUp().GetType() != 5116 and obj.GetUp().GetType() != 5118 and obj.GetUp().GetType()!= 1033577:
                yield obj
            else: pass
        else: yield obj

def main():
    
    mat = c4d.Material(c4d.Mbase)
    mat.SetName('rope')
    
    for i in obj_list():       
    
        if i.GetType() == 5181 or i.GetType() == 5186 or i.GetType() == 5101:            
            doc.StartUndo()
                
            sweep = c4d.BaseObject(c4d.Osweep)
            doc.AddUndo(c4d.UNDOTYPE_NEW, sweep)
            
            sweep.InsertUnderLast(i)
            sweep.InsertAfter(i)

            sweep.SetPhong(True,True, 45)
            sweep.SetName('Rope')
            nGone = c4d.BaseObject(5179)
            doc.AddUndo(c4d.UNDOTYPE_NEW, nGone)
            nGone[c4d.PRIM_NSIDE_RADIUS]=0.65
            nGone[c4d.PRIM_NSIDE_SIDES]=12

            nGone.InsertUnder(sweep)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, i)
            i.InsertAfter(nGone)
            
            tag = sweep.MakeTag(c4d.Ttexture)
            tag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
            tag[c4d.TEXTURETAG_TILESY] = len_spline(i)/10*3
            
            doc.InsertMaterial(mat)
            doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
            tag.SetMaterial(mat)
            
            if press_button() == 1:
                tag = sweep.MakeTag(1036222)
                tag[c4d.REDSHIFT_OBJECT_GEOMETRY_OVERRIDE]=True
                tag[c4d.REDSHIFT_OBJECT_GEOMETRY_SUBDIVISIONENABLED]=True
                tag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTENABLED]=True
                
                doc.EndUndo()
        
        else: print 'This is not a spline'
        
    c4d.EventAdd()
        
            
            
            




if __name__=='__main__':
    main()    