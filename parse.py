from bs4 import BeautifulSoup
import urllib
import urllib.request
import re
import json

url_bu_class_search = "https://www.bu.edu/phpbin/course-search/search.php?page=w0&pagesize=50&adv=1&nolog=&search_adv_all=&yearsem_adv=2023-SPRG&credits=*&pathway=&hub_match=all&pagesize=-1"
req = urllib.request.Request(url_bu_class_search, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()
    
soup = BeautifulSoup(html, "lxml")
content = soup.get_text()
content_list = content.split("\n\n\n\n\n")

prefix = []
HUB_dict = {}
for content in content_list:
    if "\n\t\t\t\t\t\t\t\t\t" in content:
        content = content.replace("\n\t\t\t\t\t\t\t\t", "")
        content = content[2:]
        if len(content)==3:
            prefix.append(content)
#         prefix.append(content)

        if "("in content:
            index_f = content.index("(")
            index_l = content.index(")")
            HUB_dict[content[index_f+1: index_l]] = content[:index_f-1]
            
            
prefix.append("XRG")
prefix.append("XCC")
HUB_dict.pop('XCC')

HUB_fullname = list(HUB_dict.values())

link_lst = []
for link in soup.find_all("a"):
    if "/phpbin" in link.get('href'):
        link_lst.append("https://www.bu.edu"+link.get('href'))
        
cls_info = {}
for content in content_list:
    cls = content[:11]
    if cls[:3] in prefix:
        cls_info[cls[:-1]] = {}
        
cls_info_keys = list(cls_info.keys())
                
for content in content_list:
    cls = content[:11]
    if cls[:3] in prefix:
        cls_info[cls[:-1]]["major"]=cls[4:6]
        
        cls_info[cls[:-1]]["HUB"] = []
        for hub in HUB_fullname:
            if hub in content:
                cls_info[cls[:-1]]["HUB"].append(hub)
        
        if "Prereq" in content:
            cls_info[cls[:-1]]["Prereq"] = []
            i = content.index("\n\n\n")
            prereq_line = content[i:]
            for class_name in cls_info_keys:
                name1 = class_name
                name2 = class_name[:3]+class_name[4:6]+class_name[7:]
                name3 = name1.lower()
                name4 = name2.lower()
                name5 = class_name[-6:]
                name6 = class_name[-6:-4]+class_name[-3:]
                name7 = name5.lower()
                name8 = name6.lower()
                if name1 in prereq_line or name2 in prereq_line or name3 in prereq_line or name4 in prereq_line or name5 in prereq_line or name6 in prereq_line or name7 in prereq_line or name8 in prereq_line:
                    cls_info[cls[:-1]]["Prereq"].append(class_name)
         
        

for inner_url in link_lst[1:-3]:
    req = urllib.request.Request(inner_url, headers={'User-Agent': 'Mozilla/5.0'})
    html2 = urllib.request.urlopen(req).read()
    soup2 = BeautifulSoup(html2, "lxml")
    content = soup2.get_text()
    class_name = content[69:79]
    print("class_name", class_name)
        
    if class_name[-3:].isnumeric():
        cls_info[class_name]["section"] = {}
        
        num_of_LEC = content.count("LEC") + content.count("IND")
        
        for num in range(num_of_LEC):
            sect = chr(65+num)+str(1)
            if sect in content:
                index = content.index(sect)
                time_list = content[index:].split()
                time_schdeule = time_list[3]+time_list[4]+time_list[5][:2]
                if len(time_schdeule)<=15 and "-" in time_schdeule:
                    cls_info[class_name]["section"][sect] = time_schdeule
                    print(time_schdeule)
                

with open("class_info.json", "w") as fp:
    json.dump(cls_info,fp)
 