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


def ptToEdg(obj, frm, to):
    bc = c4d.BaseContainer()
    bc.SetInt32(c4d.MDATA_CONVERTSELECTION_LEFT, frm)
    bc.SetInt32(c4d.MDATA_CONVERTSELECTION_RIGHT, to)
    bc.SetBool(c4d.MDATA_CONVERTSELECTION_TOLERANT, False)

    res = utils.SendModelingCommand(command = c4d.MCOMMAND_CONVERTSELECTION,
                                    list = [obj],
                                    mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                    bc = bc,
                                    doc = None)


def selPol(poly, Gone, selgon, points, nbr, bs):
    nLen = polyEdgSyze(poly, Gone, points, nbr)
    for n in selgon:
        ref = nLen[Gone.index(n)]
        for q in nLen.keys():
            if nLen[q] == ref:
                if type(Gone[q]) == list:
                    for s in Gone[q]:
                        bs.Select(s)
                else:
                    bs.Select(Gone[q])


def ngoneIndexPoly(obj):
    nGone = []
    pGone = []
    fromPolyToN = obj.GetPolygonTranslationMap()
    poly = tuple(obj.GetNGonTranslationMap(len(fromPolyToN[1]), fromPolyToN[1]))

    for i in poly:
        if len(i)>1:
            nGone.append(i)
        elif len(i)==1:
            pGone.append(i[0])
    return tuple(nGone), tuple(pGone)


def polyEdgSyze(allPoly, polygons, points, nbr):
    if press_button() == 0: 
        n = 2
    else:
        n = 0

    allPolygons = {}
    for p in polygons:
        one = []

        if type(p) is list:


            for j in p:
                getNbr = nbr.GetNeighbor(allPoly[j].a, allPoly[j].b, j)

                if getNbr not in p:
                    one.append(round((points[allPoly[j].a] - points[allPoly[j].b]).GetLength(), n))
                getNbr = nbr.GetNeighbor(allPoly[j].b, allPoly[j].c, j)

                if getNbr not in p:
                    one.append(round((points[allPoly[j].b] - points[allPoly[j].c]).GetLength(), n))

                if allPoly[j].IsTriangle():
                    getNbr = nbr.GetNeighbor(allPoly[j].c, allPoly[j].a, j)

                    if getNbr not in p:
                        one.append(round((points[allPoly[j].c] - points[allPoly[j].a]).GetLength(),n))

                else:
                    getNbr = nbr.GetNeighbor(allPoly[j].c, allPoly[j].d, j)

                    if getNbr not in p:
                        one.append(round((points[allPoly[j].c] - points[allPoly[j].d]).GetLength(), n))
                    getNbr = nbr.GetNeighbor(allPoly[j].d, allPoly[j].a, j)

                    if getNbr not in p:
                        one.append(round((points[allPoly[j].d] - points[allPoly[j].a]).GetLength(), n))

        else:
            one.append(round((points[allPoly[p].a] - points[allPoly[p].b]).GetLength(), n))
            one.append(round((points[allPoly[p].b] - points[allPoly[p].c]).GetLength(), n))

            if allPoly[p].IsTriangle():
                one.append(round((points[allPoly[p].c] - points[allPoly[p].a]).GetLength(), n))

            else:
                one.append(round((points[allPoly[p].c] - points[allPoly[p].d]).GetLength(), n))
                one.append(round((points[allPoly[p].d] - points[allPoly[p].a]).GetLength(), n))
        one.sort()
        allPolygons[polygons.index(p)] = one
    return allPolygons


def selectEdges(obj,points,poly,selEdge,se,nbr):
    tuple(selEdge)
    if press_button() == 0: 
        n = 2
    else:
        n = 0
    lenEdge = []

    bs = c4d.BaseSelect()
    p = []

    for z in selEdge:
        se.DeselectAll()
        obj.SetSelectedEdges(nbr, se, c4d.EDGESELECTIONTYPE_SELECTION)
        se.Select(z)
        obj.SetSelectedEdges(nbr, se, c4d.EDGESELECTIONTYPE_SELECTION)
        ptToEdg(obj, 1, 0)
        obj.GetPointS()
        selPt = []
        for pt in range(len(points)):                 # get selected points
            if obj.GetPointS().IsSelected(pt):
                selPt.append(pt)
        lenEdge.append(round((obj.GetPoint(selPt[1])-obj.GetPoint(selPt[0])).GetLength(), n))
        se.DeselectAll()
        obj.SetSelectedEdges(nbr, se, c4d.EDGESELECTIONTYPE_SELECTION)
    for p in poly:
        if round((points[p.a] - points[p.b]).GetLength(), n) in lenEdge:
            indx = nbr.GetPolyInfo(poly.index(p))['edge'][p.FindEdge(p.a, p.b)]
            bs.Select(indx)
            obj.SetSelectedEdges(nbr, bs, c4d.EDGESELECTIONTYPE_SELECTION)
        if round((points[p.b] - points[p.c]).GetLength(), n) in lenEdge:
            indx = nbr.GetPolyInfo(poly.index(p))['edge'][p.FindEdge(p.b, p.c)]
            bs.Select(indx)
            obj.SetSelectedEdges(nbr, bs, c4d.EDGESELECTIONTYPE_SELECTION)
        if p.IsTriangle():
            if round((points[p.c] - points[p.a]).GetLength(), n) in lenEdge:
                indx = nbr.GetPolyInfo(poly.index(p))['edge'][p.FindEdge(p.a, p.c)]
                bs.Select(indx)
                obj.SetSelectedEdges(nbr, bs, c4d.EDGESELECTIONTYPE_SELECTION)
        else:
            if round((points[p.c] - points[p.d]).GetLength(), n) in lenEdge:
                indx = nbr.GetPolyInfo(poly.index(p))['edge'][p.FindEdge(p.c, p.d)]
                bs.Select(indx)
                obj.SetSelectedEdges(nbr, bs, c4d.EDGESELECTIONTYPE_SELECTION)
            if round((points[p.d] - points[p.a]).GetLength(), n) in lenEdge:
                indx = nbr.GetPolyInfo(poly.index(p))['edge'][p.FindEdge(p.d, p.a)]
                bs.Select(indx)
                obj.SetSelectedEdges(nbr, bs, c4d.EDGESELECTIONTYPE_SELECTION)

def main():
    c4d.CallCommand(13957)            #clear consol
    obj = doc.GetActiveObject()
    if not obj or obj.GetType() != 5100:
        return

    selPolyObj = obj.GetPolygonS()

    poly = tuple(obj.GetAllPolygons())
    polyCount = obj.GetPolygonCount()
    points = tuple(obj.GetAllPoints())
    nbr = utils.Neighbor()
    nbr.Init(obj)
    nGone, pGone = ngoneIndexPoly(obj)
    
    selPoly = []
    selNgon = []
    selEdge = []

    for i in pGone:
        if selPolyObj.IsSelected(i):
            selPoly.append(i)

    for j in nGone:
        for k in j:
            if selPolyObj.IsSelected(k):
                if j not in selNgon:
                    selNgon.append(j)
                    
    tuple(selPoly)
    tuple(selNgon)
    

    if len(selNgon) != 0:
        selPol(poly, nGone, selNgon, points, nbr, selPolyObj)

    if len(selPoly) != 0:
        selPol(poly, pGone, selPoly, points, nbr, selPolyObj)

    ####################################################################

    se = obj.GetSelectedEdges(nbr, c4d.EDGESELECTIONTYPE_SELECTION)
    for edge in range(nbr.GetEdgeCount()):
        if se.IsSelected(edge):
            selEdge.append(edge)
    if len(selEdge) == 0:
        return
    else: 
        selectEdges(obj,points,poly,selEdge,se,nbr)


    c4d.EventAdd()


if __name__=='__main__':
    main()
