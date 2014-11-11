import c2x
import pickle
import time
import math

#===============================================================================

class TUMUPCNJamAssist (c2x.ApplicationBase):
    # # # # # --- GLOBAL PARAMETERS --- # # # # #
    v0 = 25 / 3.6 #Jam threshold, m/s
    jam_time = 1 #Number of simulation steps (normal 100ms each) to require speed < v0 in order to judge that a jam is present
    #v_target = 16.7 #Workzone speed, m/s
    relevance_distance = 1000.0 #distance within which to react
    jam_break = 100.0
    thw = 2.1 #Note, please also change file name below!
    reach = 100000 #deliberately very high
    simulation_length = 3600.0
    
    #Communication/System
    cars_to_notsend = dict()
    cars_to_forward = dict()
    cars_to_forward_lane = dict()
    has_been_alerted = dict()
    destination_lane = dict()
    
    #Simulation Data
    vehicles_speed = dict()
    vehicles_speed_history = dict()
    vehicles_length = dict()
    vehicles_position = dict()

    # # # # # --- INIT METHOD: called in the very beginning once - DO NOT DELETE! --- # # # # #
    def __init__ (self):

        # IMPORTANT:
        # call the base-class ctor explicitly, otherwise c2x.run will complain
        # about not matching signature.

        c2x.ApplicationBase.__init__ (self)
    #---------------------------------------------------------------------------


    # # # # # --- called each time when VISSIM passes control to the application --- # # # # #
    def processTimestep (self):
        currentSystemTime = c2x.getCurrentTime()
        
        ##### LOG #####
        if ((currentSystemTime % 60) == 0):
            #Log for ascertaining extent of communication later
            #As no results of the communication will have an effect
            #(we are at the end of the timestep)
            #do this now
            myfile = open('reach-2.1-xxxxV-xxxE.log', 'a')
            #self.myfile.write(str(round(c2x.getCurrentTime(),1)) + "," + str(veh.ID) + "," + str(veh.Position.Y) + "\n")
            myfile.write(str(currentSystemTime)+",")
            if (self.reach != 100000): myfile.write(str(self.reach)+"\n")
            else: myfile.write("no receptions\n")
            myfile.flush()
            myfile.close()
            self.reach = 100000 #reset

        if (c2x.getNet().getVehicles().__len__ == 0):
            return
        
        #This is what we have to work with - all vehicles with 'c2x' equipment.
        #Type #40 is AmI, Type #100 is non-AmI        
        c2xVehicles = c2x.getNet().getVehicles()
        
        ##### SENDS #####
        for vehicle in c2xVehicles:
            if (vehicle.TypeID == 40):
                #Any equipped vehicle travelling slowly that is not aware of a further blockage behind will send fresh alerts
                if (vehicle.ID in self.vehicles_speed_history):
                    #if (vehicle.ID != 1): print self.vehicles_speed_history[vehicle.ID] #debugging
                    if ((self.vehicles_speed_history[vehicle.ID] > (self.jam_time - 1)) and (vehicle.ID not in self.cars_to_notsend)):
                        #If the vehicle believes it is at the end of the jam, send a message
                        message = (vehicle.ID, vehicle.getPosition().getY(), vehicle.LaneIndex, "jam")
                        vehicle.sendWireless(0,pickle.dumps(message))
                #otherwise (lower priority)forward someone else's message if requested
                elif (vehicle.ID in self.cars_to_forward):
                    message = (vehicle.ID, self.cars_to_forward[vehicle.ID], self.cars_to_forward_lane[vehicle.ID], "forward")
                    vehicle.sendWireless(0,pickle.dumps(message))
        
        ##### RECEPTIONS #####
        #Wipe dictionaries before processing new receptions
        self.cars_to_notsend.clear()
        self.cars_to_forward.clear()
        self.cars_to_forward_lane.clear()

        #Process all messages in flight this timestep
        while self.moreReceptionsForThisTimestep():
            #Do the radio stuff
            reception = self.receiveWireless()

            #Did anyone receive this message?
            if (reception.noReceivers ()):
                continue

            #If so, decrypt the message
            senderId, msgY, msgLane, command = pickle.loads(reception.getMessage())
            sender = reception.getSenderVehicle() #Use this to get info on the sender, like actual Y rather than the message data

            #Get all vehicles that received the message
            receivingVehicles = reception.getReceivingVehicles()
            #For each receiving vehicle
            for veh in receivingVehicles:
                #if sender, ignore message
                #print str(veh.ID) + "," + str(senderId) + "," + str(sender.ID) + "," + str(veh.TypeID) + "," + str(sender.TypeID)
                if (veh.ID == senderId): 
                    continue #go to next vehicle  

                #only equipped vehicles can process messages
                if (veh.TypeID == 40):
                    #if at any point a jam alert comes from close behind and in the same lane, that means we are no longer a/the jam-end, stop sending fresh messages
                    if (command == "jam" and veh.getPosition().getY() > msgY and (veh.LaneIndex == msgLane) and veh.getPosition().getY() < (msgY + self.jam_break) ):
                       self.cars_to_notsend[veh.ID] = True
                    
                    #if we are within the relevance distance and the message came from in front, forward message
                    if ((msgY - veh.getPosition().getY()) < self.relevance_distance and (msgY - veh.getPosition().getY()) > 0):
                       #if this alert is closer than previous ones, store it for use later as msgY
                       if (veh.ID in self.cars_to_forward):
                          if (msgY < self.cars_to_forward[veh.ID]):
                             self.cars_to_forward[veh.ID] = msgY
                             self.cars_to_forward_lane[veh.ID] = msgLane
                             #use destination lane opposite to closest message (will be flipped later)
                             self.destination_lane[veh.ID] = msgLane
                       #first time this vehicle received an alert to be forwarded
                       else:
                          self.cars_to_forward[veh.ID] = msgY
                          self.cars_to_forward_lane[veh.ID] = msgLane
                          self.destination_lane[veh.ID] = msgLane
                       #and be alerted
                       self.has_been_alerted[veh.ID] = msgY
                       #and log the reception of a relevant, acted-upon message (for determining affected area in analysis)
                       if (veh.Position.Y<self.reach):
                           self.reach = veh.Position.Y
        
        ##### CHANGE BEHAVIOUR #####
        
        #Now that we processed all receptions, deal with the consequences      
        self.vehicles_speed.clear()
        self.vehicles_position.clear()
        self.vehicles_length.clear()
        #but don't clear the speed history, i.e. this is not 100% efficient memory management

        #Need to gather all data (all vehicles) for this timestep FIRST before changing vehicle behavior (don't know order of vehicles)
        for vehicle in c2xVehicles:
            self.vehicles_speed[vehicle.ID] = vehicle.Speed
            #if less than threshold...
            if (vehicle.Speed < self.v0):
                #and was already less than threshold (consecutively)
                if (vehicle.ID in self.vehicles_speed_history): self.vehicles_speed_history[vehicle.ID] += 1
                else: self.vehicles_speed_history[vehicle.ID] = 1
            #otherwise, delete record if it exists
            elif (vehicle.ID in self.vehicles_speed_history): del self.vehicles_speed_history[vehicle.ID]
            self.vehicles_position[vehicle.ID] = vehicle.Position.Y
            self.vehicles_length[vehicle.ID] = vehicle.Length
            preceding_vehicle_id = vehicle.getLeadingVehicleID()

        #Now change behaviour
        for vehicle in c2xVehicles:
            #if "equipped"
            if (vehicle.TypeID == 40):
                #If in the broken down area:
                if (vehicle.CurrentLinkID == 4):
                    #Stop the vehicle
                    vehicle.DesiredSpeed = 0 #m/s!!!!!
                    vehicle.setColor(0,255,255)
                    continue #nothing more to do here
                #If alerted and behind the alert location:
                if ((vehicle.ID in self.has_been_alerted) and (vehicle.getPosition().getY() < self.has_been_alerted[vehicle.ID])):
                    #vehicle is equipped, alerted, default color for not doing anything special apart from lane-holding
                    vehicle.setColor(255,0,0)
                    #if within accident/priority/single-lane area,
                    if (vehicle.CurrentLinkID == 6 and vehicle.PositionOnLink >= 6.000): #Same location as speed decision in VISSIM
                        #If for some bizarre reason this is our first contact with the vehicle, back up its desired speed
                        #if (vehicle.ID not in self.vehicles_desired_speed_backup):
                            #self.vehicles_desired_speed_backup[vehicle.ID] = vehicle.DesiredSpeed
                            #print "Warning: first contact with c2x vehicle first at accident location"
                        #harmonize speed (i.e. don't take value from distribution)
                        vehicle.DesiredSpeed = 42.5 / 3.6 # m/s, VISSIM dist is linear from 40-45 km/h, assume an ACC has a fixed speed
                    #if not changing lane
                    if (vehicle.PositionInLane == 0.5):
                        #get vehicle/object in front
                        preceding_vehicle_id = vehicle.getLeadingVehicleID()
                        v_target = vehicle.DesiredSpeed # m/s
                        #If there is no leading vehicle
                        if (preceding_vehicle_id == 0):
                            #Apply a very simple ACC
                            if (vehicle.Speed > vehicle.DesiredSpeed):
                                needed_acc = vehicle.Speed - vehicle.DesiredSpeed# + 0.4 #fudge to get round vissim quantization
                                if (needed_acc > (2.0 * 0.7)): needed_acc = (2.0 * 0.7) #limit
                                needed_acc = needed_acc * -1 #decelerate
                            elif (vehicle.Speed < vehicle.DesiredSpeed):
                                needed_acc = vehicle.DesiredSpeed - vehicle.Speed# + 0.4 #fudge to get round vissim quantization
                                if (needed_acc > 1.4): needed_acc = 1.4 #limit
                            else: needed_acc = 0.0
                            vehicle.Acceleration = needed_acc
                            vehicle.setColor(0,0,255)
                        #If vehicle is actually a vehicle
                        elif (preceding_vehicle_id > 0): 
                            #Apply Kesting ACC
                            #Treiber/Helbing IDM acceleration with a=1.4, T=1.8, v0=60 (German roadworks speed), s0=2, b=2*0.7 (upstream of bottleneck Kesting ACC factor applied)

                            #Compute required data
                            f_distance = self.vehicles_position[preceding_vehicle_id] - vehicle.Position.Y 
                            length     = self.vehicles_length[preceding_vehicle_id]
                            headway = f_distance - length;
                            preceding_vehicle_speed = self.vehicles_speed[preceding_vehicle_id]
                            target_speed = vehicle.DesiredSpeed #start value

                            #Apply acceleration
                            #if (vehicle.Speed > vehicle.DesiredSpeed): target_speed -= 0.4 #fudge to get round vissim quantization
                            #elif (vehicle.Speed < vehicle.DesiredSpeed): target_speed += 0.4 #fudge to get round vissim quantization
                            vehicle.Acceleration = 1.4 * (1.0 - (math.pow((vehicle.Speed/target_speed),4)) - math.pow(((2+(vehicle.Speed*self.thw)+((vehicle.Speed*(vehicle.Speed-preceding_vehicle_speed))/(2*math.sqrt(1.4 * 2.0 * 0.7))))/headway),2) )
                            vehicle.setColor(0,0,0)
                        #If no lane-holding route has yet been assigned, (only assign if not changing lanes already, see above)
                        if (vehicle.CurrentRouteID == 3):
                            #backup
                            #self.vehicles_desired_speed_backup[vehicle.ID] = vehicle.DesiredSpeed
                            #Reduce and harmonize speed
                            #vehicle.DesiredSpeed = 100 / 3.6 # m/s
                        #Tell vehicle to switch or hold lane (done using routes)
                            if (vehicle.LaneIndex == 1):
                                vehicle.CurrentRouteID = 1
                            else:
                                vehicle.CurrentRouteID = 2
                #otherwise, vehicle is equipped but not doing anything special
                else:
                    vehicle.setColor(0,255,0)
                    #If we overwrote the desired speed, restore it
                    #if (vehicle.ID in self.vehicles_desired_speed_backup): vehicle.DesiredSpeed = self.vehicles_desired_speed_backup[vehicle.ID]

#===============================================================================
if (__name__ == '__main__'):
    try:
        application = TUMUPCNJamAssist()
        application.run ()

    except BaseException, e:
        print str (e)
        exit()
#===============================================================================