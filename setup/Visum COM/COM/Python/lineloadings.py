"""This script produces a 2D plot of line volumes for a selected line route. It opens
   a dialog with all line routes. Select one, and the script will create a contour diagram
   in Excel. The x axis contains the analysis time intervals and the y axis contains the
   active line route items. Set a line route item filter on route points only to exclude
   items without stop points.

   Precondition: The current model must contain a PuT assignment result and analysis
   time intervals, for which volumes have been saved. Excel must be installed. Requires
   the VisumPy library."""

import sys
import numpy
import VisumPy.excelplot as plotter
import wx


def fromGetMulti(indandvalues):
    arr = numpy.array(indandvalues)
    if len(arr) == 0: return []
    return (arr[:,1])

def MakeDiagram(LR):
    externalkey = "%s/%s/%s" % (LR.AttValue("LINENAME"), LR.AttValue("NAME"), LR.AttValue("DIRECTIONCODE"))
    times = Visum.Procedures.Functions.AnalysisTimes
    ticodes = [ times.TimeInterval(i).AttValue("CODE") for i in numpy.arange(times.NumTimeIntervals)+1 ]

    if len(ticodes) == 0:
        wx.MessageBox("There are no time intervals in the VISUM version.")
        return

    LRIs = LR.LineRouteItems
    names = LRIs.GetMultiAttValues("STOPPOINT\\NAME")
    names = [name[1] for name in names]
    vol = numpy.array([fromGetMulti(LRIs.GetMultiAttValues("VOL(%s)" % code)) for code in ticodes])

    chart = plotter.Chart("Line route volumes over time and course for %s" % externalkey, "Time")
    for i, name in enumerate(names):
        chart.addSeries(ticodes, vol[:,i], name)
    chart.chart.ChartType = 85 # Surface top-view
    chart.show()

class LineLoadingsDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.CAPTION|wx.RESIZE_BORDER|wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)

        self.LB = wx.ListBox(self, -1, choices=[], style=wx.LB_ALWAYS_SB)

        self.LRs = Visum.Net.LineRoutes.GetAll
        for LR in self.LRs:
            externalkey = "%s/%s/%s" % (LR.AttValue("LINENAME"), LR.AttValue("NAME"), LR.AttValue("DIRECTIONCODE"))
            self.LB.Append(externalkey)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LISTBOX, self.OnLBClick, self.LB)

    def __set_properties(self):
        self.SetTitle("Line volumes:")
        self.SetMinSize((170, 200))

    def __do_layout(self):
        sizer_1 = wx.GridSizer(1, 1, 0, 0)
        sizer_1.Add(self.LB, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def OnLBClick(self, event):
        sel = int(self.LB.GetSelection())
        MakeDiagram(self.LRs[sel])

    def OnClose(self, event):
        Terminated.set()
        self.Destroy()

wx.InitAllImageHandlers()
dlg = LineLoadingsDlg(None, -1, "")
app.SetTopWindow(dlg)
dlg.Show()