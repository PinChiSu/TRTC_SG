#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df_kind_layer_TRTC_R = pd.read_csv('TRTC_exits - Facility&waypoints_all.csv')
kind_layer_TRTC_R = df_kind_layer_TRTC_R.values.tolist()
df_big_stations = pd.read_csv('TW - Station Graph Gsheet to Groovy Input - all.csv')
big_stations_details = df_big_stations.values.tolist()
df_TRTC_exits_details = pd.read_csv('HSR Metro SG_exit (Pin Chi) - TRTC_exit.csv')
exit_inf_TRTC = df_TRTC_exits_details.values.tolist()


# In[3]:


class exitprint:
    def __init__(self, exit_inf, stationName):
        self.exit_inf = exit_inf
        self.stationid = exit_inf[7]
        self.long_name = exit_inf[2]
        self.lon = exit_inf[4]
        self.lat = exit_inf[5]
        self.exitid = exit_inf[8]
        self.stationName = stationName
    def printGroovyCode(self):
        print("// add exits")
        for i in range(len(self.exit_inf)):
            if self.exit_inf[i][7] == self.stationName:
                if (self.exit_inf[i][2] == '0'):
                    self.exit_inf[i][8] = self.exit_inf[i][7] + '_1'
                    self.exit_inf[i][3] = self.exit_inf[i][3] + '1'
                groovyCode = "\nexit \"" + self.exit_inf[i][8] + "\" with {\n" +                              "  long_name \"" + self.exit_inf[i][3] + "\"\n" +                              "  coords { lat " + str(self.exit_inf[i][5]) + "; lon " + str(self.exit_inf[i][4]) + " }\n" +                              "  layer 0\n}\n"
                print(groovyCode)


# In[4]:


class printKind:
    def __init__(self, kind_layer, stationName):
        self.kind_layer = kind_layer
        self.stationName = stationName
        # self.path_details = path_details
    def printWaypoint(self):
        is_waypoint = False
        for i in range(len(self.kind_layer)):
            if self.kind_layer[i][0] == self.stationName:
                if self.kind_layer[i][1] == 'waypoint':
                    if is_waypoint == False:
                        print("\n// waypoints\n")
                    is_waypoint = True
                    title = "waypoint \"" + self.kind_layer[i][2] + "\" with {\n"
                    layer = "  layer " + str(self.kind_layer[i][3])
                    end = "\n}\n"
                    groovyCode = title + layer + end
                    print(groovyCode)
    def printFacility(self):
        is_facility = False
        for i in range(len(self.kind_layer)):
            if self.kind_layer[i][0] == self.stationName:
                if self.kind_layer[i][1] == 'facility':
                    if is_facility == False:
                        print("// facilities\n")
                    is_facility = True
                    title = "facility \"" + self.kind_layer[i][2] + "\" with {\n"
                    kind = "  kind FacilityKind.TICKET_GATE\n"
                    layer = "  layer " + str(self.kind_layer[i][3])
                    end = "\n}\n"
                    groovyCode = title + kind + layer + end
                    print(groovyCode)


# In[5]:


class pathprint:
    def __init__(self, stationName, SG_path_details):
        self.stationName = stationName
        self.SG_path_details = SG_path_details
    # print path details
    def printGroovyCode_raw_lv2(self):
        start_exit_facility = False
        start_exit_waypoint = False
        start_waypoint_facility = False
        start_platform = False
        start_f2f = False
        start_p2p = False
        start_w2p = False
        start_w2w = False
        for i in range(len(self.SG_path_details)):
            if self.SG_path_details[i][1] == stationName:
                if (self.SG_path_details[i][2] == 'exit' and self.SG_path_details[i][4] == 'facility'):
                    #print("\n check e2f\n")
                    if start_exit_facility == False:
                        print("\n// between exits and ticket gate\n")
                        start_exit_facility = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] and " +                                 str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = ""
                if (self.SG_path_details[i][2] == 'facility' and self.SG_path_details[i][4] == 'exit'):
                    #print("\n check e2f\n")
                    if start_exit_facility == False:
                        print("\n// between exits and ticket gate\n")
                        start_exit_facility = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] to " +                                 str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = ""
                if (self.SG_path_details[i][2] == 'facility' and self.SG_path_details[i][4] == 'facility'):
                    #print("\n check e2f\n")
                    if start_f2f == False:
                        print("\n// between ticket gate\n")
                        start_f2f = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] and " +                                 str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = ""
                if (self.SG_path_details[i][2] == 'exit' and self.SG_path_details[i][4] == 'waypoint'):
                    #print("\n check e2w\n")
                    if start_exit_waypoint == False:
                        print("// between exits and waypoints\n")
                        start_exit_waypoint = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] and " +                             str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = ""
                if (self.SG_path_details[i][2] == 'facility' and self.SG_path_details[i][4] == 'waypoint'):
                    #print("\n check w2f\n")
                    if start_waypoint_facility == False:
                        print("// between waypoints and ticket gates\n")
                        start_waypoint_facility = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] and " +                             str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = ""
                if (self.SG_path_details[i][2] == 'waypoint' and self.SG_path_details[i][4] == 'waypoint'):
                    #print("\n check w2f\n")
                    if start_w2w == False:
                        print("// between waypoints\n")
                        start_w2w = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] and " +                             str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = ""
                if (self.SG_path_details[i][2] == 'facility' and self.SG_path_details[i][4] == 'platform'):
                    #print("\n check f2p\n")
                    if start_platform == False:
                        print("// between ticket gate and platform\n")
                        start_platform = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] to " +                             str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = ""
                if (self.SG_path_details[i][2] == 'platform' and self.SG_path_details[i][4] == 'facility'):
                    #print("\n check p2f")
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] to " +                             str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = "\n  start_node_location_hint { structured_hint LocationHintStructuredHint." + str(self.SG_path_details[i][8]) +                                                  " }"
                if (self.SG_path_details[i][2] == 'waypoint' and self.SG_path_details[i][4] == 'platform'):
                    #print("\n check f2p\n")
                    if start_w2p == False:
                        print("// between waypoint and platform\n")
                        start_w2p = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] to " +                             str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                if (self.SG_path_details[i][2] == 'platform' and self.SG_path_details[i][4] == 'waypoint'):
                    #print("\n check p2f")
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] to " +                             str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = "\n  start_node_location_hint { structured_hint LocationHintStructuredHint." + str(self.SG_path_details[i][8]) +                                                  " }"
                if (self.SG_path_details[i][2] == 'platform' and self.SG_path_details[i][4] == 'platform'):
                    #print("\n check p2p\n")
                    if start_p2p == False:
                        print("\n// between platforms\n")
                        start_p2p = True
                    title = str(self.SG_path_details[i][6]) + " " + str(self.SG_path_details[i][2]) + "[\"" + str(self.SG_path_details[i][3]) + "\"] to " +                                 str(self.SG_path_details[i][4]) + "[\"" + str(self.SG_path_details[i][5]) + "\"] add {"
                    kind = "\n  kind WayKind." + str(self.SG_path_details[i][7])
                    average_duration_seconds = "\n  average_duration_seconds " + str(self.SG_path_details[i][9])
                    LocationHintStructuredHint = ""
                end = "\n}\n"
                groovycode = title + kind + average_duration_seconds + LocationHintStructuredHint + end
                print(groovycode)


# In[6]:


# input the station name and output the results
stationName = input('Enter the stationid👍 :')


# In[7]:


test = exitprint(exit_inf_TRTC, stationName)
test.printGroovyCode()
test = printKind(kind_layer_TRTC_R, stationName)
test.printFacility()
test.printWaypoint()
test1 = pathprint(stationName, big_stations_details)
test1.printGroovyCode_raw_lv2()


# In[ ]:





# In[ ]:





# In[ ]:




