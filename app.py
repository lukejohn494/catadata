import numpy as np
from scipy.optimize import minimize
from scipy.optimize import fsolve
import time
from copy import deepcopy
import os
import sys
from ase import Atom, Atoms
from ase.io import read,write
from ase.visualize import view
import glob

global start
start=os.getcwd()

try:
    import Tkinter as tk
except:
    import tkinter as tk

class Catadata(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class MenuBar(tk.Menu):
    def __init__(self, master):
        tk.Menu.__init__(self, master)
        
        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)
        
        helpMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help",underline=0, menu=helpMenu)
        helpMenu.add_command(label="Help", underline=1, command=lambda: master.switch_frame(Help))
        helpMenu.add_command(label="About", underline=1, command=lambda: master.switch_frame(About))
        
    def quit(self):
        sys.exit(0)        
        
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        '''
        root = Tk()
        menu = Menu()
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=master.switch_frame(StartPage))
        filemenu.add_command(label="Open...", command=master.switch_frame(StartPage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.switch_frame(StartPage))
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=master.switch_frame(StartPage))
        helpmenu.add_command(label="About...", command=lambda: master.switch_frame(About))
        '''
        
        tk.Label(self, text="Welcome to Catadata", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Label(self, text="version 0", font=('Helvetica', 12)).pack()
        tk.Button(self, text="Start a new project",
                  command=lambda: master.switch_frame(New1)).pack()
        tk.Button(self, text="Continue an existing project",
                  command=lambda: master.switch_frame(CurrentProject)).pack()
        tk.Button(self, text="Settings",
                  command=lambda: master.switch_frame(Settings)).pack()
        tk.Button(self, text="About",fg="red",
                  command=lambda: master.switch_frame(About)).pack()
        
        
        
class New1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def btn1():
            global traj1
            global projname
            traj1=e2.get()
            view(read(traj1))
            projname=e1.get()
        tk.Label(self, text="Please name this project", font=('Helvetica', 18)).pack()#(side="left")
        e1=tk.Entry(self)
        e1.insert(0, 'moppy1')
        e1.pack()#(side="right")
        tk.Label(self, text="Please insert the directory leading to the trajectory.", font=('Helvetica', 18),wraplength=450).pack()#(side="left")
        e2=tk.Entry(self)
        e2.insert(0, 'init.traj')
        e2.pack()#(side="right")
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: [btn1(),master.switch_frame(New2)]).pack()
        #[funct1(),funct2()]
        
        
        
class New2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def btn2():
            global traj1
            global list1
            #traj1=self.parent.filesuccess(self.ids.firsttraj.text)
            list1=""
            m1=read(traj1)
            for atom in m1:
                if atom.tag==10:
                    list1=list1+atom.symbol+", "+str(atom.tag)+", "
            print(list1)
        tk.Label(self, text="Great, for our reference, we need to change atoms for screening. Please take a minute to tag atoms as the number 10. Then save the file. Structure opening soon...", font=('Helvetica', 18),wraplength=450).pack()
        tk.Label(self, text="When done press continue", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: [btn2(),master.switch_frame(New3)]).pack()
        
        
        
        
class New3(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Just to confirm, you have tagged the following atoms: ", font=('Helvetica', 18),wraplength=450).pack()
        e3=tk.Entry(self)
        e3.insert(0, list1)
        e3.pack()
        tk.Label(self, text="If not, go back, if so, press continue:", font=('Helvetica', 18)).pack(side="top")
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: master.switch_frame(New4)).pack()
        
        
        
        
        
class New4(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def btn3():
            global filscr
            filscr=[]
            sepp=e4.get().replace(" ","").split(',')
            m1=read(traj1)
            for chg in sepp:
                trp=deepcopy(m1)
                for atom in trp:
                    if atom.tag==10:
                        atom.symbol=chg
                write(chg+'_screen.traj',trp)
                filscr.append(chg+"_screen.traj")
        tk.Label(self, text="Separated by commas, please insert the elements (besides the current (Mo) to screen this study:", font=('Helvetica', 18),wraplength=450).pack(side="top")
        e4=tk.Entry(self)
        e4.insert(0, 'Ti,W,Zr,Cr')
        e4.pack()
        tk.Label(self, text="Please insert the directory leading to the trajectory.", font=('Helvetica', 18)).pack(side="top")
        e5=tk.Entry(self)
        e5.insert(0, 'moppy')
        e5.pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: [btn3(),master.switch_frame(New5)]).pack()
        
        
        
class New5(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def btn4():
            global filcop1
            global inname
            global scrps
            scrps=e7.get()
            filcop1=os.getcwd()+"/"+scrps
            inname=e8.get()
        tk.Label(self, text="We successfully made the folders and the files. We now need to optimize. Please insert submission script directory here: This will default to our built in script if empty", font=('Helvetica', 18),wraplength=450).pack(side="top")
        e6=tk.Entry(self)
        e6.insert(0, '')
        e6.pack()
        tk.Label(self, text="If you have a collection of scripts in a folder to include, place folder directory: (this will use built in structures if empty). ", font=('Helvetica', 18),wraplength=450).pack(side="top")
        e7=tk.Entry(self)
        e7.insert(0, 'script')
        e7.pack()
        tk.Label(self, text="What name do you want for the initial trajectory?", font=('Helvetica', 18)).pack(side="top")
        e8=tk.Entry(self)
        e8.insert(0, 'init.traj')
        e8.pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: [btn4(),master.switch_frame(New6)]).pack()
        
        
        
class New6(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def btn5():
            global subs
            subs=""
            try:
                os.mkdir(projname)
            except:
                1+1
            os.chdir(projname)
            for iu in filscr:
                iuy=iu.replace("_screen.traj","")
                try:
                    os.mkdir(iuy)
                except:
                    1+1
                os.system("cp ../"+iu+" "+iuy+"/"+inname)
                os.system("cp -a "+filcop1+"/ "+iuy+"/")
                os.chdir(iuy)
                #os.system("sbatch struc3.sub")
                subs+="submitted\n"
                os.chdir("../")
        tk.Label(self, text="Please take a moment to check the file structures before we submit these scripts for optimization.", font=('Helvetica', 18),wraplength=450).pack(side="top")
        tk.Label(self, text="When ready, please press continue, to delete these scripts and start over, press main menu", font=('Helvetica', 18),wraplength=450).pack(side="top")
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: [btn5(),master.switch_frame(New7)]).pack()
        

        
class New7(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Submitting your jobs to the local cluster...", font=('Helvetica', 18)).pack(side="top")
        e9=tk.Entry(self)
        e9.insert(0, subs)
        e9.pack()
        tk.Label(self, text="Congrats! You've completed setup and submission of structural optimization", font=('Helvetica', 18),wraplength=450).pack(side="top")
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: master.switch_frame(StartPage)).pack()

        
        
class CurrentProject(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Welcome again, how can we help?", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Run adsorption calculations",
                  command=lambda: master.switch_frame(Adsorption1)).pack()
        tk.Button(self, text="Run electronic structure calculations",
                  command=lambda: master.switch_frame(New2)).pack()
        tk.Button(self, text="Further surface/slab analysis (photos!)",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Run vibrational calculations",
                  command=lambda: master.switch_frame(New2)).pack()
        tk.Button(self, text="Model/analyze a chemical reaction",
                  command=lambda: master.switch_frame(New2)).pack()
        tk.Button(self, text="Extract all data from screening study",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Run a learning analysis from dataset",
                  command=lambda: master.switch_frame(New2)).pack()
        tk.Button(self,text="Error checking",
                  command=lambda: master.switch_frame(Error_Check)).pack()
        tk.Button(self, text="Go back to main menu",
                  command=lambda: master.switch_frame(StartPage)).pack()
        #[funct1(),funct2()]
       
class Adsorption1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def abtn1():
            global adsy
            global allad
            global adser
            global pr1
            global exp
            exp=e11.get()
            pr1=e10.get()
            os.chdir(start)
            if "altsite.traj" not in os.listdir(os.getcwd()+"/"+pr1+"/"):
                os.system("cp "+start+"/"+exp+" "+start+"/"+pr1+"/"+"altsite.traj")
            adser=e01.get()
            adsy=adser.split(",")
            '''
            for at in ads:
                aty=read(at+".traj")
                allad.append(aty)
            mf=read(exp)
            write(pr1+"/before.traj",mf)
            mf2=read(pr1+"/before.traj")
            view(mf2)
            '''
            view(read(start+"/"+pr1+"/"+"altsite.traj"))
        tk.Label(self, text="Type the directory of the project here", font=('Helvetica', 18)).pack()
        e10=tk.Entry(self)
        e10.insert(0, 'moppy1')
        e10.pack()
        tk.Label(self, text="In a list separated by commas (no space), please list the adsorbates you wish to adsorb on surface. Press complete when done or alternative load adsorbate files using the button below. PLEASE place adsorbate files in project folder and name XX.traj", font=('Helvetica', 18),wraplength=450).pack()
        e01=tk.Entry(self)
        e01.insert(0, 'O,S,P')
        e01.pack()
        tk.Label(self, text="Enter the directory with the trajectory you'd like to model adsorption for:", font=('Helvetica', 18),wraplength=450).pack()
        e11=tk.Entry(self)
        e11.insert(0, 'moppy1/Ti/init.traj')
        e11.pack()
        tk.Label(self, text="When done press continue", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Load adsorbates",
                  command=lambda: [abtn1(),master.switch_frame(Adsorption2)]).pack()  
        
        
        
        
class Adsorption2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def abtn2():
            global filcop2
            global mxo
            global mxe
            mxe=e13.get()
            filcop2=os.getcwd()+"/"+mxe
            mpr=read(pr1+"/altsite.traj")
            mxp=[]
            mxyy=[]
            mxo=e12.get()
            for atom in mpr:
                if atom.symbol=="He":
                    mxp.append(atom)
            mxy=[]
            myu=os.getcwd()
            print(pr1+"/.")
            for fily in os.listdir(os.getcwd()+"/"+pr1+"/"):
                try:
                    dny=read(pr1+"/"+fily+"/"+mxo)
                    mxyy=[]
                    os.chdir(pr1+"/"+fily+"/")
                except:
                    continue
                for ax,ap in enumerate(adsy): 
                    mxyyy=[]
                    try:
                        os.mkdir(ap)
                    except:
                        1+1
                    os.chdir(ap)
                    for atx,atm in enumerate(mxp):
                        dncy=deepcopy(dny)
                        atm.symbol=ap
                        dncy.append(atm)
                        try:
                            os.mkdir(str(atx))
                        except:
                            1+1
                        write(str(atx)+"/init.traj",dncy)
                        os.system("cp -a "+filcop2+"/ "+os.getcwd()+"/"+str(atx)+"/")
                        mxyyy.append(Atoms(dncy))
                    os.chdir('../')
                    mxyy.append(mxyyy)
                os.chdir("../../")
                mxy.append(mxyy)
        tk.Label(self, text="We now need to confirm the predetermined sites for the adsorption. Please check now here. If you are not content, please add/delete a Helium atom over each potential site and save as altsite.traj. Find example here", font=('Helvetica', 18),wraplength=450).pack()
        tk.Label(self, text="Important: what is the output file in the main directory? Need to know this in order to place adsorbates", font=('Helvetica', 18),wraplength=450).pack()
        e12=tk.Entry(self)
        e12.insert(0, 'init.traj')
        e12.pack()
        tk.Label(self, text="Awesome, all folders have been set. Please reference the folder where scripts are located", font=('Helvetica', 18),wraplength=450).pack()
        e13=tk.Entry(self)
        e13.insert(0, 'script2')
        e13.pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Load adsorbates",
                  command=lambda: [abtn2(),master.switch_frame(Adsorption3)]).pack()
        
        
        
        
        
class Adsorption3(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Great, please confirm all information", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Delete files",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Confirm files",
                  command=lambda: master.switch_frame(Adsorption4)).pack()        
        #[funct1(),funct2()]
        
        
        
        
class Adsorption4(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Awesome, all folders have been set. Would you like to submit jobs using a script?", font=('Helvetica', 18),wraplength=450).pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="confirm and run using sbatch",
                  command=lambda: master.switch_frame(Adsorption5)).pack()
        
        
        
        
class Adsorption5(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Submitting jobs ... ", font=('Helvetica', 18)).pack()
        e14=tk.Entry(self)
        e14.insert(0, '')
        e14.pack()
        tk.Label(self, text="Congrats, you have completed jobs {111111..222222} to run adsorption.", font=('Helvetica', 18),wraplength=450).pack()
        e15=tk.Entry(self)
        e15.insert(0, '')
        e15.pack()
        tk.Button(self, text="Done",
                  command=lambda: master.switch_frame(StartPage)).pack()       
        #[funct1(),funct2()]
        
class Error_Check(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Welcome again, how can we help?", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Compare DOS.pickle to a trajectory",
                  command=lambda: master.switch_frame(Dos_Traj1)).pack()
        tk.Button(self, text="Compare DOS.pickle files to charge density files",
                  command=lambda: master.switch_frame(Dos_Bader1)).pack()
        tk.Button(self, text="Check for high fmax in all folders",
                  command=lambda: master.switch_frame(FmaxCheck1)).pack()
        tk.Button(self, text="Go back to project analysis",
                  command=lambda: master.switch_frame(CurrentProject)).pack()
        
class Dos_Traj1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def ebtn1():
            ############################
            global emp
            global m5
            global errchk
            os.chdir(start)
            osp=os.getcwd()
            dirz=er1.get()
            m3=er2.get()
            os.chdir(dirz)
            errchk=""
            import numpy
            from ase import Atoms
            for folder, subfolders, files in os.walk(dirz):
                for name in files:
                    if name in [m3]:
                        fpath=os.path.abspath(folder)
                        os.chdir(fpath)
                        try:
                            f= open("calcdir/pdos.log","r")
                        except:
                            try:
                                f= open("dirdos/pdos.log","r")
                            except:
                                errchk=errchk+fpath+"\n"
                                continue
                        f2=f.readlines()

                        #makes the block text into a list of strings
                        sn=0
                        lisp=[]
                        for l in f2:
                                if "read from pseudo" in l:
                                        sn=1
                                        continue
                                if "k = " in l:
                                        sn=0
                                        break
                                if sn==1:
                                        lisp.append(l)
                        lisp.pop(0)
                        catoms=[]
                        v=1
                        for z,i in enumerate(lisp):
                                q=i.split(" ")
                                #print(q) #looking for a good way to split
                                for s,t in enumerate(q): #q is the string, t is a character
                                        if 'atom' in t:
                                                try:
                                                        u=float(q[s+3])
                                                        g=s+4
                                                except:
                                                        u=float(q[s+2])
                                                        g=s+3
                                                if z==0:
                                                        catoms.append(q[g].replace('(','').replace(')','').replace('1','').replace(',',''))
                                              
                                                if u!=v:
                                                        catoms.append(q[g].replace('(','').replace(')','').replace('1','').replace(',',''))
                                                        v+=1
                        catoms.sort()
                        #print(catoms)
                        #Analyzing Atoms object
                        m=read(m3)
                        m2=m.get_chemical_symbols()
                        m2.sort()
                        #print(m2)
                        m5=m.get_chemical_symbols()
                        if m2==catoms:
                                emp="These are equivalent"
                        else:
                                errchk=errchk+fpath+"\n"
            ###########################################
            
            os.chdir(osp)
        tk.Label(self, text="Type the directory of the project here", font=('Helvetica', 18)).pack()
        er1=tk.Entry(self)
        er1.insert(0, '/home/lukejohn/moppy/Mo2C/')
        er1.pack()
        tk.Label(self, text="What is the name of the atoms trajectory?", font=('Helvetica', 18),wraplength=450).pack()
        er2=tk.Entry(self)
        er2.insert(0, 'out.traj')
        er2.pack()
        tk.Label(self, text="To start press continue", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: [ebtn1(),master.switch_frame(Dos_Traj2)]).pack()         

        
class Dos_Traj2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="The results...", font=('Helvetica', 18)).pack()
        tk.Label(self, text="Here are the erroneous folders:", font=('Helvetica', 18)).pack()
        if len(errchk)==0:
            tk.Label(self, text="None", font=('Helvetica', 18)).pack()
        else:
            tk.Label(self, text=errchk, font=('Helvetica', 11)).pack()
        #tk.Label(self, text=m5, font=('Helvetica', 18)).pack()
        tk.Button(self, text="Go back to main menu",
                  command=lambda: master.switch_frame(CurrentProject)).pack()

class Dos_Bader1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def ebtn1():
            global emp
            global m5
            global atomsread
            global dirz1
            global prntread
            global thrper
            os.chdir(start)
            osp=os.getcwd()
            dirz1=db1.get()
            atomsread=db2.get()
            thrper=db3.get()
            os.chdir(dirz)
            prntread=[]
            execfile("dos_bader_compare.py")
        tk.Label(self, text="Type the full directory of the project here", font=('Helvetica', 18)).pack()
        db1=tk.Entry(self)
        db1.insert(0, '/home/lukejohn/moppy/Mo2C/')
        db1.pack()
        tk.Label(self, text="What is the name of the atoms trajectory of relevance?", font=('Helvetica', 18),wraplength=450).pack()
        db2=tk.Entry(self)
        db2.insert(0, 'out.traj')
        db2.pack()
        tk.Label(self, text="What is the error threshold for comparison? (%)", font=('Helvetica', 18),wraplength=450).pack()
        db3=tk.Entry(self)
        db3.insert(0, '75')
        db3.pack()
        tk.Label(self, text="To start press continue", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: [ebtn1(),master.switch_frame(Error_Check2)]).pack()         


class Dos_Bader2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="The results...", font=('Helvetica', 18)).pack()
        tk.Label(self, text="Here are the erroneous folders:", font=('Helvetica', 18)).pack()
        if len(errchk)==0:
            tk.Label(self, text="None", font=('Helvetica', 18)).pack()
        else:
            tk.Label(self, text=errchk, font=('Helvetica', 11)).pack()
        #tk.Label(self, text=m5, font=('Helvetica', 18)).pack()
        tk.Button(self, text="Go back to main menu",
                  command=lambda: master.switch_frame(CurrentProject)).pack()

class FmaxCheck1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        def ebtn1():
            global atomsread2
            global dirz2
            global fread
            os.chdir(start)
            osp=os.getcwd()
            dirz2=fm1.get()
            atomsread2=fm2.get()
            os.chdir(dirz2)
            fread=""
            import glob
            import numpy.linalg as LA
            for folder, subfolders, files in os.walk(dirz2):
                for name in files:
                    if name in [atomsread2]:
                        fpath=os.path.abspath(folder)
                        os.chdir(fpath)
                        try:
                            m=read(name)
                        except:
                            fread=fread+"Can't open in  "+fpath.replace('/mnt/io2/scratch_alevoj1/shared/org/','')+'\n'
                            continue
                        n=m.get_forces()
                        n2=[LA.norm(n[i,:]) for i in range(0,n.shape[0])]
                        n3=max(n2)
                        if n3>0.05:
                            fread=fread+fpath.replace('/mnt/io2/scratch_alevoj1/shared/org/','')+'\n'
        tk.Label(self, text="Type the full directory of the project here", font=('Helvetica', 18)).pack()
        fm1=tk.Entry(self)
        fm1.insert(0, '/home/lukejohn/moppy/Mo2C/')
        fm1.pack()
        tk.Label(self, text="What is the name of the atoms trajectory of relevance?", font=('Helvetica', 18),wraplength=450).pack()
        fm2=tk.Entry(self)
        fm2.insert(0, 'Relax3.traj')
        fm2.pack()
        tk.Label(self, text="To start press continue", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Continue",
                  command=lambda: [ebtn1(),master.switch_frame(FmaxCheck2)]).pack()         


class FmaxCheck2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="The results...", font=('Helvetica', 18)).pack()
        tk.Label(self, text="Here are the erroneous directories:", font=('Helvetica', 18)).pack()
        if len(fread)==0:
            tk.Label(self, text="None", font=('Helvetica', 18)).pack()
        else:
            tk.Label(self, text=fread, font=('Helvetica', 11)).pack()
        tk.Button(self, text="Go back to main menu",
                  command=lambda: master.switch_frame(CurrentProject)).pack()
        
class Settings(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Welcome again, how can we help?", font=('Helvetica', 18)).pack()
        tk.Button(self, text="Change QE settings for structural optimization",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Change QE settings for adsorption calculations",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Change python version",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Go back to main menu",
                  command=lambda: master.switch_frame(StartPage)).pack()

class About(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="About Catadata v0", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Label(self, text="Catadata was homebrewed in the Vojvodic lab in order to simplify running atomistic screening studies on materials using DFT. The effort is spearheaded by Luke Johnson, with continual additions from other lab members. Created in December 2019.", font=('Helvetica', 12),wraplength=450).pack()
        tk.Label(self, text="Soon to come: \n Submissions \n Multi-Atom adsorbate screening \n Electronic structure analysis \n Reaction modelling \n Mixed termination screening \n ", font=('Helvetica', 12),wraplength=450,fg="green").pack()
        tk.Button(self, text="Go back to main menu",
                  command=lambda: master.switch_frame(StartPage)).pack()
        
class Help(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Helo Catadata", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Label(self, text="Catadata is made as user friendly as possible. However, issues can arise with the software. Ensure you follow all instructions to the T. Made a mistake? Please feel free to restart the program and delete any created files. Submission has been suppressed for now to ensure optimal editing through v0. \n If you have any questions, please contact the software master, Luke Johnson -> \n lukejohn at seas.upenn.edu \n ", font=('Helvetica', 12),wraplength=450).pack()
        tk.Button(self, text="Go back to main menu",
                  command=lambda: master.switch_frame(StartPage)).pack()
        
if __name__ == "__main__":
    app = Catadata()
    app.mainloop()
