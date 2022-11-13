import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
  
cred_obj = firebase_admin.credentials.Certificate('/Users/williamlee/Desktop/BostonHack/bostonhack-axinio-firebase-adminsdk-jucdk-a6596530ad.json')

default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': "https://bostonhack-axinio-default-rtdb.firebaseio.com/"
	})

ref = db.reference('class_info')
class_info = ref.get()


#read json file for the filters
f = open('filter_data.json')
filter_info = json.load(f)


#turn time into minutes
def chage_time_format(cls):
    
    temp_lst = []
    if " " not in cls:
        sec = cls[-2:]
        cls_rename = cls[:3]+" "+cls[3:5]+" "+cls[5:8]
    else:
        sec = cls[-2:]
        cls_rename = cls[:-3]
        
    look_up_time = class_info[cls_rename]["section"][sec]
    index_of_dash = look_up_time.index("-")
    
    start_time = look_up_time[:index_of_dash]
    index_of_col_start = start_time.index(":")
    if start_time[-2:]=="pm":
        start_hour = int(start_time[:index_of_col_start])+12
    else:
        start_hour = int(start_time[:index_of_col_start])
    start_minute = int(start_time[index_of_col_start+1:-2])
    
    first_input = 60*start_hour+start_minute
    temp_lst.append(first_input)
        
    end_time = look_up_time[index_of_dash+1:]
    index_of_col_end = end_time.index(":")
    if end_time[-2:]=="pm":
        end_hour = int(end_time[:index_of_col_end])+12
    else:
        end_hour = int(end_time[:index_of_col_end])
    end_minute = int(end_time[index_of_col_end+1:-2])
    
    second_input = 60*end_hour+end_minute
    temp_lst.append(second_input)
    return temp_lst
    

#the schedule that's already occupied
slot_occupied_lst = []
for cls in filter_info["classes"]:
    temp_lst = chage_time_format(cls)
    slot_occupied_lst.append(temp_lst)
    
classes_registered = filter_info["classes"]
    
#the classes that are already taken before (list)
classes_taken = filter_info["taken_classes"]

#look for the classes for major
num_of_major_class_desired = int(filter_info["majordesired"])
a = num_of_major_class_desired
major = filter_info["major"].upper()
classes = class_info.keys()
possible_classes_major = []


for cls in classes:
    if num_of_major_class_desired==0:
        break
    if class_info[cls]["major"]==major:
        if cls not in classes_taken:
            if "Prereq" in list(class_info[cls].keys()):
                if len(class_info[cls]["Prereq"])==0:
                    for section in list(class_info[cls]["section"].keys()):
                        section_required = class_info[cls]["section"][section]
                        time_required = chage_time_format(cls+" "+section_required)
                        
                        val = True
                        for occupied in slot_occupied_lst:
                            if not(time_required[1]<occupied[0] or time_required[0]>occupied[1]):
                                val = False
                        if val==True:
                            possible_classes_major.append(cls+" "+section_required)
                            num_of_major_class_desired -= 1
                else:
                    val1 = True
                    for prereq in class_info[cls]["Prereq"]:
                        prereq = prereq.replace(" ", "")
                        if prereq not in classes_taken and prereq not in classes_registered:
                            val1 = False
                        
                    if val1 == True:
                        for section in list(class_info[cls]["section"].keys()):
                            section_required = class_info[cls]["section"][section]
                            x = cls+section
                            x = x.replace(" ", "")
                            time_required = chage_time_format(x)
                            
                            val = True
                            for occupied in slot_occupied_lst:
                                if not(time_required[1]<occupied[0] or time_required[0]>occupied[1]):
                                    val = False
                            if val==True:
                                possible_classes_major.append(cls+" "+section)
                                num_of_major_class_desired -= 1
possible_classes_major = possible_classes_major[2:]
possible_classes_major = possible_classes_major[:a]
                            
#find hub classes desired
num_of_hub_class_desired = filter_info["hubdesired"]
hub_required = filter_info["hub"]
hub_converter = {"Philosophical Inquiry and Life's Meanings":"PLM",
 'Aesthetic Exploration':"AEX",
 'Historical Consciousness':"HCO",
 'Scientific Inquiry I':"SI1",
 'Scientific Inquiry II':"SI2",
 'Social Inquiry I':"SO1",
 'Social Inquiry II':"SO2",
 'Quantitative Reasoning I':"QR1",
 'Quantitative Reasoning II':"QR2",
 'The Individual in Community':"ITC",
 'Global Citizenship and Intercultural Literacy':"GCI",
 'Ethical Reasoning':"ETR",
 'First-Year Writing Seminar':"FYW",
 'Writing, Research, and Inquiry':"WRI",
 'Writing-Intensive Course':"WIN",
 'Oral and/or Signed Communication':"OSC",
 'Digital/Multimedia Expression':"DME",
 'Critical Thinking':"CRT",
 'Research and Information Literacy':"RIL",
 'Teamwork/Collaboration':"TWC",
 'Creativity/Innovation':"CRI"}



hub_dict = {}
for x in reversed(range(int(num_of_hub_class_desired)+1)):
    hub_dict[x]=[]

for cls in classes:
    if "section" in list(class_info[cls].keys()):
        if len(list(class_info[cls]["section"].values()))==0:
            hub_dict[0].append(cls)
        else:
            for section in list(class_info[cls]["section"].keys()):
                section_required = class_info[cls]["section"][section]
                x = cls+" "+section
                x = x.replace(" ", "")
                time_required = chage_time_format(x)
                
                val = True
                for occupied in slot_occupied_lst:
                    if not(time_required[1]<occupied[0] or time_required[0]>occupied[1]):
                        val = False
                if val==True and "HUB" in list(class_info[cls].keys()):
                    hub_this_class_has = class_info[cls]["HUB"]
                    count_hub = 0
                    for hub in hub_this_class_has:
                        hub_shorten = hub_converter[hub]
                        if hub_shorten in hub_required:
                            count_hub += 1
                    hub_dict[count_hub].append(cls)

hub_recommendation = []
hub_key = list(hub_dict.keys())[0]
hub_recommendation += hub_dict[hub_key][:int(num_of_hub_class_desired)]

print([possible_classes_major, hub_recommendation])
    
                        
                            

    


