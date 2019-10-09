import c4d
from c4d import gui

obj_list = (c4d.Onull,
            c4d.Oextrude,
            c4d.Osymmetry,
            c4d.Oconnector,
            c4d.Osweep,
            1018544,
            1010865,
            1039861,
            1001002,
            1039859,
            1019396,
            5150,
            5125,
            1007455,
            5117,
            5107
        )

def removeempty(obj):
    if not obj:
        return
    removeempty(obj.GetDown())
    removeempty(obj.GetNext())
    if not obj.GetDown():

        if obj.GetType() in obj_list:
            obj.Remove()
        elif obj.GetType()== c4d.Oinstance and not obj[c4d.INSTANCEOBJECT_LINK]:
            obj.Remove()
        elif obj.GetType()== 1018957 and not obj[c4d.MGINSTANCER_LINK]:
            obj.Remove()

def main():
    obj = doc.GetFirstObject()
    removeempty(obj)

    c4d.EventAdd()
if __name__=='__main__':
    main()
