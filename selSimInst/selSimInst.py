import c4d
from c4d import gui


def selector(obj, mainObj):
    if not obj:
        return
    selector(obj.GetDown(), mainObj)
    selector(obj.GetNext(), mainObj)
    if not obj.GetDown():
        if obj.GetType() == 5126:
            if obj[c4d.INSTANCEOBJECT_LINK] == mainObj:
                obj.SetName(str(mainObj.GetName()))
                obj.SetBit(c4d.BIT_ACTIVE)


def main():
    mainObj = doc.GetActiveObject()
    if not mainObj:
        return

    obj = doc.GetFirstObject()
    selector(obj, mainObj)

    c4d.EventAdd()




if __name__=='__main__':
    main()
