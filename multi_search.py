from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import os,time
from datetime import datetime
from tkinter import messagebox
from getpass import getuser
from threading import Thread
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


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
        logs_entry("Some error Occured!! Close this application.\n\n"+str(os.sys.exc_info()))


def new_window():
    window11 = Toplevel(root)
    window11.title("About This Application!")
    a11=Text(window11)
    a11.insert(INSERT,about_this_application)
    a11.pack()

Current_working_directory = ("/".join(os.getcwd().split("\\")))
search_location1 = "Folder to search not selected."
save_location1 = Current_working_directory
chvar=IntVar(root)
chvar.set(0)#checkbox variable
number_of_files_to_search=0

def logs_entry(log,end="\n"):
    statusbar.configure(state='normal')
    statusbar.insert(END, log+end)
    statusbar.configure(state='disabled')
    statusbar.yview(END)
    root.update_idletasks()

def search_one_file(arguments):
    search_value_list=arguments[0]
    file_path=arguments[1]
    save_file_handler=arguments[2]
    first_find={} #To include the file name for the first find of each values
    local_counter={}
    for value in search_value_list:
        first_find[value]=True
        local_counter[value]=0
    read_file=True   
    

    data=[]
    try:
        with open(file_path,"r") as f1:
            data=f1.readlines()
    except:
        read_file=False
        return(read_file,local_counter)
        
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
    return(read_file,local_counter)
    



def file_path_func( files_all,chvar):
    try :
        if chvar == 0: 
            for (root_dir,_,files) in os.walk(search_location1, topdown=True):
                if search_location1==root_dir:
                    for i in files:
                        files_all.append(root_dir+"/"+i)        
        else:  
            for (root_dir,_,files) in os.walk(search_location1, topdown=True):
                for i in files:
                    files_all.append(root_dir+"/"+i)
    except:
        logs_entry("Some error Occured!! Not able to find files.\n\n"+str(os.sys.exc_info()))
    

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

    # Extracting values from screen
    search_values=(text_area.get("1.0","end")).lower().splitlines()
    search_value_set=list(set(search_values))
    if "" in search_value_set:
        search_value_set.remove("")
    if len(search_value_set)==0:
        search.configure(state="normal")
        messagebox.showinfo ("Search Box Empty!!",'Enter Values to search!!')
        return
    global search_location1
    if (search_location1=="Folder to search not selected."):
        search.configure(state="normal")
        messagebox.showinfo ("Search folder not selected!!",'Select a folder to search!')
        return

    # Creating folder to save result
    i=1
    global save_location1
    multi_search_folder=save_location1+str("/MultiSearch")
    lenght_multi_search_folder=len(multi_search_folder)
    while(os.path.exists(multi_search_folder)):
        multi_search_folder=multi_search_folder[:lenght_multi_search_folder]+str(i)
        i+=1
    os.mkdir(multi_search_folder)
    
    #initiating counter for each value
    counter={}
    for x in search_value_set:
        counter[x]=0

    file_path_list = []
    t=Thread(target=file_path_func, args=(file_path_list,chvar.get()))
    t.start()
    logs_entry("\n Analysing the search request...",end="")
    while(t.is_alive()):
        logs_entry("#",end="")
        time.sleep(0.5)
        root.update()
    global number_of_files_to_search #for getting an idea of how much time is required
    number_of_files_to_search = len(file_path_list)
    logs_entry("\n{} Files found. \n".format(number_of_files_to_search))


    #Here we address the invalid filename bug
    search_value_save_path={}

    
    f1={} #To handle multiple files
    for value in search_value_set: 
        temp=value#storing original in temp
        try :
            invalid_filname_char=["/","\\","?","*","\"",">","<","|",":"]
            for i in invalid_filname_char:
                if i in value:
                    raise Exception()
                    
            lenght_value=len(value)
            i=1
            while(os.path.exists(multi_search_folder+"/"+value+".txt")):
                value=value[:lenght_value]+str(i)
                i+=1
            search_value_save_path[temp]=(multi_search_folder+"/"+value+".txt")  
            f1[temp]=open(search_value_save_path [temp] ,"a+")
            f1[temp].write("Searched for : "+temp+"\nSaved at "+multi_search_folder+"/"+value+".txt\n")
        except:
            value=temp
            invalid_filname_char=["/","\\","?","*","\"",">","<","|",":"]
            invalid_char_dictionary={
                "/":"ForwardSlash",
                "\\":"BackSlash",
                "?": "QuestionMark",
                "*":"Asterisk",
                "\"":"DoubleQoutes",
                ">":"GreaterThan",
                "<":"LessThan",
                "|":"UprightSlash",
                ":":"Colon"
                }
            for i in invalid_filname_char:
                while i in value:
                    value=value.replace(i,invalid_char_dictionary[i])
            lenght_value=len(value)
            i=1
            while(os.path.exists(multi_search_folder+"/"+value+".txt")):
                value=value[:lenght_value]+str(i)
                i+=1
            search_value_save_path[temp]=(multi_search_folder+"/"+value+".txt"  )
            f1[temp]=open(search_value_save_path [temp] ,"a+")
            f1[temp].write("Searched for : "+temp+"\nSaved at "+multi_search_folder+"/"+value+".txt\n")           
                    

    completed_files_count=0

    with ThreadPoolExecutor(max_workers=8) as executor:
        
        future_to_file = {
            executor.submit(search_one_file, [search_value_set,i,f1,counter]): i for i in file_path_list
        }
        for future in as_completed(future_to_file):
            res = future.result()  # read the future object for result
            filename = future_to_file[future]  # match result back to filename
            if res[0]:
                logs_entry("Completed : \n"+filename)
            else:
                logs_entry("\n\nError while reading : \n"+filename+"\n\n")
            for value in search_value_set:
                counter[value]+=res[1][value]
            completed_files_count+=1
            file_count.configure(text="Search progress stats : {} / {} Completed".format(completed_files_count,number_of_files_to_search))
            root.update()
        
    for value in search_value_set:
        f1[value].close()
        #logic to delete empty files from save folder
        if counter[value]==0:
            os.remove(search_value_save_path [value])
            logs_entry("deleted Empty file : "+search_value_save_path [value])
    FILEBROWSER_PATH=os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    subprocess.run([FILEBROWSER_PATH, os.path.normpath(multi_search_folder)])

    end_time=datetime.now() #End time of the whole search operation.
    completed_in=(end_time-start_time).total_seconds() #time taken calculated in seconds

    logs_entry("Search of {} files completed in {} seconds.\n\n".format(completed_files_count,completed_in))

    with open(multi_search_folder+"/logfile.log","w+") as f1:
        f1.write("Search of {} files completed in {} seconds.\n\n".format(completed_files_count,completed_in))
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
    search_location1 = "Folder to search not selected."
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
root.title("MultiSearch")
ttk.Label(root, text="Enter the values to be searched in below box. ",font=("Times New Roman", 12)).grid(column=0, row=0,sticky="w",columnspan=2)
ttk.Label(root, text="   Each line is treated as a seperate value.",font=("Times New Roman", 10)).grid(column=0, row=1,sticky="w",)
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
l1.grid(column=0, row=18, pady=10, padx=5,sticky="w")
search_loc.grid(column=3, row=18, padx=1,sticky="w")
space.grid(column=0, row=20, pady=1, padx=1,sticky="w")
l2.grid(column=0, row=21, pady=10, padx=5,sticky="w")
save_loc.grid(column=3, row=21, padx=1,sticky="w")
file_count.grid(column=0,row=25,pady=10, padx=10)
statusbar.grid(column=0,row=27,pady=5, padx=5,columnspan=10,sticky=W)

text_area.focus()
root.mainloop()