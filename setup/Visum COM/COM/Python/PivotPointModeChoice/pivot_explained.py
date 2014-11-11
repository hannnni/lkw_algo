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


    # fetch all matrices into numpy ndarrays
    T_old = []
    U_old = []
    U_new = []
    ODs = Visum.Net.ODMatrices
    skims = Visum.Net.SkimMatrices
    for no in T_old_no:
        try:
            T_old.append(ODs.ItemByKey(no).GetValues())
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
    T_old = numpy.array(T_old)
    U_old = numpy.array(U_old)
    U_new = numpy.array(U_new)

    # compute pivot point model
    T_old_sum = sum(T_old)            # total trips
    p_old = T_old / T_old_sum         # prior mode shares
    p_old[numpy.isnan(p_old)] = 0      # set results of division by zero to 0 by using numpy advanced indexing
    p_new  = p_old * numpy.exp(U_new-U_old)     # posterior mode shares
    p_new_sum = sum(p_new)
    T_new = T_old_sum * p_new / p_new_sum
    T_new[numpy.isnan(T_new)] = 0          # set results of division by zero to 0 by using numpy advanced indexing

    # save matrices
    for i, no in enumerate(T_new_no):
        if no > 0:
            try:
                ODs.ItemByKey(no).SetValues(T_new[i])
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
