from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import os
from datetime import datetime
from tkinter import messagebox
from getpass import getuser


root=Tk()

about_this_application='''

Hi,

This application is created for searching a list of IPs from hundreds of network device backup folder. This can be be used for other use cases as well.

Source code for this is available in : https://github.com/sibisita/Multi-Search/blob/main/multi-search.py


Sibi

'''

def to_escape_error():
    try:
        search_main_func()
    except:
        logs_entry("Some error Occured!! Close this application.")


def new_window():
    window11 = Toplevel(root)
    window11.title("About This Application!")
    a11=Text(window11)
    a11.insert(INSERT,about_this_application)
    a11.pack()

Current_working_directory = ("/".join(os.getcwd().split("\\")))
search_location1 = Current_working_directory
save_location1 = Current_working_directory
chvar=IntVar()
chvar.set(0)#checkbox variable
number_of_files_to_search=0

def logs_entry(log):
    statusbar.configure(state='normal')
    statusbar.insert(END, log+"\n")
    statusbar.configure(state='disabled')
    statusbar.yview(END)
    root.update_idletasks()

def search_one_file(search_value_list,file_path,save_file_handler,local_counter):
    data=[]
    try:
        with open(file_path,"r") as f1:
            data=f1.readlines()
        #time.sleep(0.05)# rest of 50ms
        logs_entry("Now reading : \n"+file_path)
    except:
        logs_entry("\n\nError while reading : \n"+file_path+"\n\n")
        return local_counter

    first_find={} #To include the file name for the first find of each values
    
    for value in search_value_list:
        first_find[value]=True
        
    index=0   
    
    for line in data:
        for value in search_value_list:
            if value in line.lower():
            
                if first_find[value]:
                    save_file_handler[value].write("\n\n*****"+file_path+"*****\n")
                    first_find[value]=False
                save_file_handler[value].write(str(index)+" : "+line)
                local_counter[value]+=1
        index+=1
    #time.sleep(0.05)# rest of 50ms
    return local_counter



def file_path_func():
    files_all=[]
    if chvar.get() == 0: 
        for (root_dir,_,files) in os.walk(search_location1, topdown=True):
            if search_location1==root_dir:
                for i in files:
                    files_all.append(root_dir+"/"+i)        
    else:  
        for (root_dir,_,files) in os.walk(search_location1, topdown=True):
            for i in files:
                files_all.append(root_dir+"/"+i)
    return files_all

def search_in_folder():
    temp_var = filedialog.askdirectory()
    if temp_var != "":
        global search_location1
        search_location1 = temp_var
        l1.configure(text=search_location1)

def save_in_folder():
    temp_var = filedialog.askdirectory()
    if temp_var != "":
        global save_location1 
        save_location1 = temp_var
        l2.configure(text=save_location1)


def search_main_func():
    
    search.configure(state="disabled")
    start_time=datetime.now() #Start time to calculate time taken

    # Creating folder to save result
    i=1
    global save_location1
    multi_search_folder=save_location1+str("/Multi-Search")
    lenght_multi_search_folder=len(multi_search_folder)
    while(os.path.exists(multi_search_folder)):
        multi_search_folder=multi_search_folder[:lenght_multi_search_folder]+str(i)
        i+=1
    os.mkdir(multi_search_folder)
    
    # Extracting values from screen
    search_values=(text_area.get("1.0","end")).lower().splitlines()
    search_value_set=set(search_values)
    search_value_set.remove("")
    
    #initiating counter for each value
    counter={}
    for x in search_value_set:
        counter[x]=0

    file_path_list = file_path_func() 
    global number_of_files_to_search #for getting an idea of how much time is required
    number_of_files_to_search = len(file_path_list)

    completed_files_count=0
    f1={} #To handle multiple files
    for value in search_value_set:
        f1[value]=open(multi_search_folder+"/"+value+".txt","a+")
    for i in file_path_list:
        counter = search_one_file (search_value_set,i,f1,counter)
        completed_files_count+=1
        file_count.configure(text="Search progress stats : {} / {} Completed".format(completed_files_count,number_of_files_to_search))
        root.update()
        
    for value in search_value_set:
        f1[value].close()
        #logic to delete empty files from save folder
        if counter[value]==0:
            os.remove(multi_search_folder+"/"+value+".txt")
            logs_entry("deleted Empty file : "+multi_search_folder+"/"+value+".txt")

    

    end_time=datetime.now() #End time of the whole search operation.
    completed_in=(end_time-start_time).total_seconds() #time taken calculated in seconds

    logs_entry("Search of {} files completed in {} seconds.\n\n".format(completed_files_count,completed_in))

    with open(multi_search_folder+"/logfile.log","w+") as f1:
        f1.write("Search of {} files completed in {} seconds.\n\n".format(completed_files_count,completed_in))
        global search_location1
        f1.write("Search conducted by '"+getuser()+"' at "+search_location1+"\n\n")
        f1.write(metadata_area.get("1.0","end"))
        f1.write("\n\nSearched Values\t:\tCount\n")
        f1.write("\n"+str(counter).replace(", ","\n").replace(":","\t\t:\t")[1:-1])

    MsgBox = messagebox.askquestion ('Exit Application','Search Completed. Press Yes to exit.\n Press no to verify logs. ',icon = 'info')
    if MsgBox == 'yes':
        root.destroy()
    else:
        output_window.grid(column=11,row=1,pady=5, padx=5, rowspan=100,sticky="nw")
        output_window.configure(state='normal')
        output_window.insert(END, "Search of {} files completed in {} seconds.\n\n".format(completed_files_count,completed_in))
        output_window.insert(END, "\n\nSearched Values  \t:\tCount\n")
        output_window.insert(END, str(counter).replace(", ","\n").replace(":","\t\t:\t")[1:-1])
        output_window.configure(state='disabled')
        output_window.yview(END)
        output_lable.grid(column=11, row=0,sticky="w",columnspan=2)
        search.grid_forget()
        reset.grid(column=3, row=6)
    

def reset_func():
    output_window.grid_forget()
    output_lable.grid_forget()
    global search_location1,save_location1,number_of_files_to_search
    search_location1 = Current_working_directory
    l1.configure(text=search_location1)
    save_location1 = Current_working_directory
    l2.configure(text=save_location1)
    chvar.set(0)#checkbox variable
    number_of_files_to_search=0
    metadata_area.delete("1.0",END)
    metadata_area.insert(END,"Metadata : \n\n")
    text_area.delete("1.0",END)
    output_window.configure(state="normal")
    output_window.delete("1.0",END)
    statusbar.configure(state="normal")
    statusbar.delete("1.0",END)
    statusbar.insert(INSERT, "Here comes the logs\n\n")
    statusbar.configure(state='disabled')
    reset.grid_forget()
    search.grid(column=3, row=6)
    search.configure(state="normal")
    file_count.configure(text="Search progress stats will appear here!!!")
    root.update_idletasks()


def resource_path(relative_path):
    try:
        base_path = os.sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#front end
root.title("Multi-Search")
ttk.Label(root, text="Enter the values to be searched below: ",font=("Times New Roman", 15)).grid(column=0, row=0,sticky="w",columnspan=2)
text_area = scrolledtext.ScrolledText(root, wrap=WORD, width=30, height=15,font=("Times New Roman", 12))
search=Button(root,text="Search",bg="green",fg="yellow",font=20,command= to_escape_error)
reset=ttk.Button(root,text="Reset",command= reset_func)
about=ttk.Button(root,text="About",width=8,command=new_window)
metadata_area = scrolledtext.ScrolledText(root, wrap=WORD, width=25, height=10,font=("Times New Roman", 12))
metadata_area.configure(state='normal')
metadata_area.insert(END, "Metadata : \n\n")
subdir=ttk.Checkbutton(root,text="Use subdirectory",variable=chvar)
l1=ttk.Label(root, text=search_location1)
search_loc=ttk.Button(root,text="Browse search folder",command=search_in_folder)
l2=ttk.Label(root, text=save_location1)
save_loc=ttk.Button(root,text="Browse Save folder",command=save_in_folder)
space=ttk.Label(root, text=" ")
file_count=ttk.Label(root, text="Search progress stats will appear here!!!",font=("Times New Roman", 14))
statusbar=scrolledtext.ScrolledText(root, wrap=WORD, width=60, height=15,font=("Times New Roman", 12))
statusbar.insert(INSERT, "Here comes the logs\n\n")
statusbar.configure(state='disabled')
output_window=scrolledtext.ScrolledText(root, wrap=WORD, width=30, height=30,state='disabled',font=("Times New Roman", 12))
output_lable=ttk.Label(root, text="Searched values and their number of occurances: ",font=("Times New Roman", 10))
try:
    photo = PhotoImage(file = resource_path("icon.png"))
    root.iconphoto(False,photo)
except:
    pass



#grid position
text_area.grid(column=0, row=2, pady=1, padx=1,sticky="w",rowspan=15,columnspan=2)
search.grid(column=3, row=6)
about.grid(column=4, row=0,padx=5,sticky=N+E)
metadata_area.grid(column=3, row=8, padx=1,sticky="w",columnspan=3)
subdir.grid(column=4, row=20, padx=20,sticky=N+W)
l1.grid(column=0, row=18, pady=1, padx=1,sticky="w")
search_loc.grid(column=3, row=18, padx=1,sticky="w")
space.grid(column=0, row=20, pady=1, padx=1,sticky="w")
l2.grid(column=0, row=21, pady=1, padx=1,sticky="w")
save_loc.grid(column=3, row=21, padx=1,sticky="w")
file_count.grid(column=0,row=25,pady=10, padx=10)
statusbar.grid(column=0,row=27,pady=5, padx=5,columnspan=10,sticky=W)

text_area.focus()
root.mainloop()