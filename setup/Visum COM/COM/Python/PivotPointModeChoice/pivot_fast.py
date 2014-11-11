import numpy
import wx

def errormsg(msg):
    wx.MessageBox(msg, "Pivot point mode choice", style=wx.ICON_ERROR|wx.OK)

def Pivot(Visum, T_old_no, T_new_no, U_old_no, U_new_no):
    """Calculate pivot point mode choice model.
       T_old_no = list of prior OD matrix numbers
       T_new_no = list of posterior OD matrix numbers (0 = don't save)
       U_old_no = list of prior utility (skim) matrix numbers
       U_new_no = list of posterior utility (skim) matrix numbers """


    # fetch all matrices into numarrays
    T = []
    U_old = []
    U_new = []
    ODs = Visum.Net.ODMatrices
    skims = Visum.Net.SkimMatrices
    for no in T_old_no:
        try:
            T.append(ODs.ItemByKey(no).GetValues())
        except:
            errormsg("%d is not a valid OD matrix number." % no)
            return
    for no in U_old_no:
        try:
            U_old.append(skims.ItemByKey(no).GetValues())
        except:
            errormsg("%d is not a valid skim matrix number or does not contain data." % no)
            return
    for no in U_new_no:
        try:
            U_new.append(skims.ItemByKey(no).GetValues())
        except:
            errormsg("%d is not a valid skim matrix number or does not contain data." % no)
            return

    # convert lists into arrays
    T     = numpy.array(T)
    U_old = numpy.array(U_old)
    U_new = numpy.array(U_new)

    # compute pivot point model
    Ts = sum(T)               # total trips
    p  = T / Ts               # prior mode shares
    p[numpy.isnan(p)] = 0      # set results of division by zero to 0
    p  *= numpy.exp(U_new-U_old)    # posterior mode shares
    Ts /= sum(p)              # total matrix / sum of posterior shares
    Ts[numpy.isnan(Ts)] = 0    # set results of division by zero to 0

    # save matrices
    for i, no in enumerate(T_new_no):
        if no > 0:
            try:
                ODs.ItemByKey(no).SetValues(p[i] * Ts)
            except:
                errormsg("%d is not a valid OD matrix number or saving failed." % no)
                return


""" In the example I am going to change only the PuT supply. The prior
    utility matrices are no. 2 for PrT and no. 8 for PuT. The posterior PuT
    utilities are in no.6 and I reuse no.2 for PrT, because I do not change PrT.
    Prior OD matrices are no.1 for PrT and no.5 for PuT. I am only interested
    in posterior PuT demand, so I set the posterior PrT OD matrix number to
    zero (= don'T_old save) and store the posterior PuT demand in matrix no. 11. """
Pivot(Visum, [1,5], [0,11], [2,8], [2,6])
