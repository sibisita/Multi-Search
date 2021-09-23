#import the required packages
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import os
from datetime import datetime
from tkinter import messagebox
import json
#from tkinter import messagebox

#initialize tkinter window
root = Tk()

#initialize the variables for search values, files and output count 
search_values=[]
files_all=[]

#initialize the tkinter variables that has effect on the graphics
a="/".join(os.getcwd().split("\\"))
search_location1 = StringVar()
search_location1.set(a)
save_location1 = StringVar()
save_location1.set(a)
chvar=IntVar()
chvar.set(0)



def search1():
    search_location1.set(filedialog.askdirectory())
    #l1.configure(text="Location to search \t: '"+search_location1+"'")

def save1():
    save_location1.set(filedialog.askdirectory())
    #l2.configure(text="Location to save result\t: '"+save_location1+"'")
    
    

def extract_values():
    #root.withdraw()
    search.configure(state="disabled")
    start_time=datetime.now()
    

    search_values=(text_area.get("1.0","end")).splitlines()
    output={}
    for x in search_values:
        if len(x)==0:
            search_values.remove(x) #removing empty rows
    for item in search_values:
        output[item]=0#initializing dictionary with 0. To be increased as search hits.
    #print(output)
    #checkbox logic
    if chvar.get()==1:
        print("selected")
        file_list_subdirectory(search_location1.get())
        
    else:
        print("not selected")
        file_list_avoid_subdirectory(search_location1.get())

    #make save location directory
    i=1
    save_final=save_location1.get()+'/Multi-Search'
    lenght_save_final=len(save_final)
    while(os.path.exists(save_final)):
        save_final=save_final[:lenght_save_final]+str(i)
        i+=1




    #open file one by one and search every values together
    for path in files_all: 
        #print(path)
        logs_entry("searching : " + path.split("/")[-1])
        output=search_in_file(path,save_final,search_values,output)
    print(files_all,("\ncompleted"))

    end_time=datetime.now()
    completed_in=end_time-start_time
    logs_entry("\n\nTime taken for completion "+str(completed_in.total_seconds())+" Seconds")
    with open(save_final+"/log.log","w",encoding="utf8") as f:
        f.write(metadata_area.get("1.0","end"))
        f.write("\n"+str(output).replace(", ","\n")[1:-1])
    MsgBox = messagebox.askquestion ('Exit Application','Search Completed. Press Yes to exit.\n Press no to verify logs. ',icon = 'info')
    if MsgBox == 'yes':
        root.destroy()
    else:
        output_window.grid(column=11,row=1,pady=5, padx=5, rowspan=100,sticky="nw")
        output_window.configure(state='normal')
        output_window.insert(END, str(output).replace(", ","\n")[1:-1])
        output_window.configure(state='disabled')
        output_window.yview(END)
        output_lable.grid(column=11, row=0,sticky="w",columnspan=2)


        
    
    
    
    #root.deiconify()

    



#finding all files in sub-directory
def file_list_subdirectory(search_location1):    
    for (root,_,files) in os.walk(search_location1, topdown=True):
        for i in files:
            files_all.append(root+"/"+i)
            #print(root+i)
    #print(files_all)

#finding all files in only currect directory
def file_list_avoid_subdirectory(loc):
    for (root,_,files) in os.walk(loc, topdown=True):
        if loc==root:
            for i in files:
                files_all.append(root+"/"+i)

    #print(files_all)

#opening one file and searching all the values
def search_in_file(path,a,search_values,output):
    x={}
    for i in search_values:
        x[i]=True
    if not (os.path.exists(a)):
        os.mkdir(a)
        logs_entry("\nSave location created at : " + a+"\n")
    try:    
        file1 = open(path, "r",encoding="utf8")
        index=0
        for line in file1:
            index+=1
            
            for value in search_values:
                
                if value in line:
                    file2 = open(a+"/"+value+".txt","a+",encoding="utf8")
                    if os.path.realpath(file2.name)!=os.path.realpath(file1.name):
                        print(os.path.realpath(file2.name),os.path.realpath(file1.name))
                        print(a+"/"+value+".txt")
                        logs_entry("\nWriting to : "+value+".txt")
                        if x[value]:
                            file2.write("\n\n"+path+"\n")
                            x[value]=False
                        file2.write(str(index)+" : "+line)
                        output[value]+=1
                        print("Out put of file2.name",os.path.realpath(file2.name))
                    file2.close()

        print("Out put of file.name",os.path.realpath(file1.name))
        
        file1.close()
    except:
        logs_entry("Error while reading : "+path)
    print(output)
    return output

def logs_entry(log):
    statusbar.configure(state='normal')
    statusbar.insert(END, log+"\n")
    statusbar.configure(state='disabled')
    statusbar.yview(END)

about_this_application='''

Hi,

This application is created for searching a list of IPs from hundrends of network device backup. This can be be used for other usecases as well.



'''

def new_window():
    window11 = Toplevel(root)
    window11.title("About This Application!")
    ttk.Label(window11, text=about_this_application,font=("Times New Roman", 15)).grid(column=0, row=0,sticky="w")

            



#front end
root.title("Multi-Search")
ttk.Label(root, text="Enter the values to be searched below: ",font=("Times New Roman", 15)).grid(column=0, row=0,sticky="w",columnspan=2)
text_area = scrolledtext.ScrolledText(root, wrap=WORD, width=30, height=15,font=("Times New Roman", 12))
search=ttk.Button(root,text="Search",command=extract_values)
about=ttk.Button(root,text="About this Application",width=5,command=new_window)
metadata_area = scrolledtext.ScrolledText(root, wrap=WORD, width=25, height=10,font=("Times New Roman", 12))
metadata_area.configure(state='normal')
metadata_area.insert(END, "Metadata : \n\n")
subdir=ttk.Checkbutton(root,text="Use subdirectory",variable=chvar)
l1=ttk.Label(root, textvariable=search_location1)
search_loc=ttk.Button(root,text="Browse search folder",command=search1)
l2=ttk.Label(root, textvariable=save_location1)
save_loc=ttk.Button(root,text="Browse Save folder",command=save1)
space=ttk.Label(root, text=" ")
statusbar=scrolledtext.ScrolledText(root, wrap=WORD, width=60, height=15,font=("Times New Roman", 12))
statusbar.insert(INSERT, "Here comes the logs\n\n")
statusbar.configure(state='disabled')
output_window=scrolledtext.ScrolledText(root, wrap=WORD, width=30, height=30,state='disabled',font=("Times New Roman", 12))
output_lable=ttk.Label(root, text="Searched values and their number of occurances: ",font=("Times New Roman", 10))




#grid position
text_area.grid(column=0, row=2, pady=1, padx=1,sticky="w",rowspan=15,columnspan=2)
search.grid(column=3, row=6)
about.grid(column=3, row=3)
metadata_area.grid(column=3, row=8, padx=1,sticky="w")
subdir.grid(column=3, row=5)
l1.grid(column=0, row=18, pady=1, padx=1,sticky="w")
search_loc.grid(column=3, row=18, padx=1,sticky="w")
space.grid(column=0, row=20, pady=1, padx=1,sticky="w")
l2.grid(column=0, row=21, pady=1, padx=1,sticky="w")
save_loc.grid(column=3, row=21, padx=1,sticky="w")
statusbar.grid(column=0,row=25,pady=5, padx=5,columnspan=10)



text_area.focus()
root.mainloop()