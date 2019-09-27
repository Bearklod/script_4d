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


def len_spline(spline):

    if spline.GetType() == 5181:
        lenght = 2 * 3.14 * spline[c4d.PRIM_CIRCLE_RADIUS]
        return lenght

    elif spline.GetType() == 5186:
        lenght = (2 * spline[c4d.PRIM_RECTANGLE_WIDTH]) + (2 * spline[c4d.PRIM_RECTANGLE_HEIGHT])
        return lenght

    elif spline.GetType() == 5101:
        leng = c4d.utils.SplineLengthData()
        leng.Init(spline)
        return leng.GetLength()


def obj_list():
    objs = doc.GetActiveObjects(1)
    for obj in objs:
        if obj.GetUp():
            if obj.GetUp().GetType() != 5116 and obj.GetUp().GetType() != 5118:
                yield obj
            else:
                pass
        else:
            yield obj


def main():

    mat = c4d.Material(c4d.Mbase)
    mat.SetName('ROPE')
    doc.InsertMaterial(mat)
    for i in obj_list():
        if i.GetType() == 5181 or i.GetType() == 5186 or i.GetType() == 5101:
            doc.StartUndo()
            rope = c4d.BaseObject(1033577)
            rope.SetName('ROPE')
            doc.AddUndo(c4d.UNDOTYPE_NEW, rope)
            tag = rope.GetTag(c4d.Ttexture)
            tag = rope.MakeTag(c4d.Ttexture)
            tag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
            tag[c4d.TEXTURETAG_TILESY] = len_spline(i) * 5 / 10
            tag.SetMaterial(mat)

            doc.AddUndo(c4d.UNDOTYPE_CHANGE, i)
            rope.InsertBefore(i)
            rope.SetRelPos(i.GetRelPos())
            rope[c4d.REEPER_RAD] = 0.25
            rope[c4d.REEPER_STRANDS] = 6
            rope[c4d.REEPER_DIS] = 0.6
            rope[c4d.REEPER_COILS] = int(len_spline(i) * 5 / 10)
            if press_button() == 1:
                tag = rope.MakeTag(1036222)
                tag[c4d.REDSHIFT_OBJECT_GEOMETRY_OVERRIDE] = True
                tag[c4d.REDSHIFT_OBJECT_GEOMETRY_SUBDIVISIONENABLED] = True
                tag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTENABLED] = True
                rope[c4d.REEPER_DIS] = 0.55
            i.InsertUnder(rope)
            i.SetRelPos(c4d.Vector())
            c4d.EventAdd()
            doc.EndUndo()

        else:
            print "This isn't a spline"


if __name__ == '__main__':
    main()
