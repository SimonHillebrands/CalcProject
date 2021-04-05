from tkinter import *
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from scipy.integrate import quad
from scipy.optimize import fsolve
from scipy.optimize import newton



from numpy import sin
from numpy import cos
from numpy import tan
from numpy import arcsin
from numpy import arccos
from numpy import arctan
from numpy import hypot
from numpy import arctan2
from numpy import sinh
from numpy import cosh
from numpy import tanh
from numpy import arcsinh
from numpy import arccosh
from numpy import arctanh
from numpy import exp
from numpy import sqrt



f = Figure(figsize=(5,5), dpi = 100)
ax = f.add_subplot(111, projection='3d')

#converts the input into something python can evaluate
def cleanFunction(f):
    f = f.replace("^","**")
    

    mathList=dir(np)  #List of math functions
    mathList.reverse()

    #Adds 'np.' to any math functions
    for i in range(len(mathList)):
       if mathList[i] in f:
          # f = f.replace(mathList[i],"np." + mathList[i])
         #  f = f.replace("np.np.","np.")
         pass
    return(f)

def solveVolumeDisk(f,xmin=0, xmax=2):
    
    f = cleanFunction(f)

    def integrand1(x):
        return(eval(f))

    def integrand2(x):
        return(np.pi*integrand1(x)**2)

    def findRoots(func):
        return(fsolve(func,0))

   # result = findRoots(integrand1)
    #if(len(result)>1):
     #   i = quad((integrand1), result[0], result[1])
    #else:
    try:
        i = quad((integrand2), xmin, xmax)
    except TypeError:
        i = quad((integrand2), 0, xmax)

    return(i[0])

def solveVolumeWasher(f,g,xmin=0,xmax=2):
    
    f = cleanFunction(f)
    g = cleanFunction(g)

    def integrand1(x):
        return(eval(f))

    def integrand2(x):
        return(eval(g))

    def integrand3(x):
        return(np.pi*integrand1(x)**2)
    
    def integrand4(x):
        return(np.pi*integrand2(x)**2)

    def integrand5(x):
        return(integrand4(x)-integrand3(x))

    def findIntersection(fun1,fun2,x0):
        return fsolve(lambda x : fun1(x) - fun2(x),x0)

    #result = findIntersection(integrand1,integrand2,[0,2])


    #fsolve(f, [1.0, 2.0])
    i = quad((integrand5), xmin, xmax)
    #i2 = quad((integrand4), result[0], result[1])
    #i = i1 - i2
    return(i[0])

def plot(f,g,xmin=0,xmax=2):

   

    u = np.linspace(xmin, xmax, 60)
    v = np.linspace(0, 2*np.pi, 60)
    U, V = np.meshgrid(u, v)

    X = U

    f = cleanFunction(f)
    print(f)

    Y1 = (eval(f))*np.cos(V)
    Z1 = (eval(f))*np.sin(V)

    ax.clear()
    
    f = eval(f.lower())
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');
    #ax.contour(u,0*u,[i*u for i in range(xmin,xmax,60)])
    l1 = ax.plot_wireframe(u,0*u,[(f*-1)*i for i in range(-1,2,60)])

    plt.setp(l1,linewidth=3,color = 'black')

    #ax.plot_surface(u,0*u,[i*u for i in range(len(u))])
    ax.plot_surface(X, Y1, Z1, alpha=0.3, color='red', rstride=6, cstride=12)


    #Checks to see if there is a value in g(x)
    if(len(g)>0):
        
        g = cleanFunction(g)

        Y2 = (eval(g))*np.cos(V)
        Z2 = (eval(g))*np.sin(V)

        g = eval(g.lower())

        l2 = ax.plot_wireframe(u,0*u,[(g)*i for i in range(-1,2,60)])
        plt.setp(l2,linewidth=3,color = 'black')
        
        ax.plot_surface(X, Y2, Z2,alpha=0.3, color='blue', rstride=6, cstride=12)

class GraphTool(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args,**kwargs)
        container = tk.Frame(self)

        container.pack(side="top",fill="both", expand = True )

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (GraphPage, PageOne):
            
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GraphPage)

    def show_frame(self,cont):
        
        frame = self.frames[cont]
        frame.tkraise()
class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text = "Graph Page")
        label.grid(row=0, column = 2)
        #label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Help",command=lambda:controller.show_frame(PageOne))
        button1.grid(row=0,column=3)

        label1 = tk.Label(self,text = "f(x)=")
        label1.grid(row = 2,column=0)

        label2 = tk.Label(self,text = "g(x)=")
        label2.grid(row = 3,column=0)

        label3 = tk.Label(self,text = "xmin:")
        label3.grid(row = 5,column=0)

        label4 = tk.Label(self,text = "xmax:")
        label4.grid(row = 6,column=0)       

        label5 = tk.Label(self,text = "Volume:")
        label5.grid(row = 4,column=0)   

        self.entry1 = tk.Entry(self)
        self.entry1.grid(row =2,column = 1)

        self.entry2 = tk.Entry(self)
        self.entry2.grid(row =3,column = 1)

        self.entry3 = tk.Entry(self)
        self.entry3.grid(row =5,column = 1)

        self.entry4 = tk.Entry(self)
        self.entry4.grid(row =6,column = 1)

        self.entry5 = tk.Entry(self)
        self.entry5.grid(row =4,column = 1)        


        self.button2 = tk.Button(self, text="Enter",command=lambda:self.graph())
        self.button2.grid(row = 0,column = 0)
        #self.button2.pack()

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z');

        ax.mouse_init()

        frame = tk.Frame(self)
        frame.grid(row=4, column=2)


        canvas = FigureCanvasTkAgg(f, frame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand = True)
        ax.mouse_init()
        #toolbar = NavigationToolbar2TkAgg(canvas,frame)
        #toolbar.update()
       # canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand = True)

        ax.mouse_init()

    def graph(self):
        
        f = self.entry1.get()
        g = self.entry2.get()
        
        f = f.replace("x","U")
        g = g.replace("x","U")

        trip = False
        try:
            xmin = int(self.entry3.get())
            xmax = int(self.entry4.get())
            plot(f,g,xmin,xmax)

            f = f.replace("U","x")
            g = g.replace("U","x")

            if(len(g)>0): 
                volume = solveVolumeWasher(f,g,xmin,xmax)
                self.entry5.delete(0,END)
                self.entry5.insert(0,volume)
            else:
                volume = solveVolumeDisk(f,xmin,xmax)
                self.entry5.delete(0,END)
                self.entry5.insert(0,volume)
            trip = True

        except ValueError:
            plot(f,g)

            f = f.replace("U","x")
            g = g.replace("U","x")
            #trip makes sure entry5 isnt output to twice
            if(not(trip)):
                if(len(g)>0):       
                    volume = solveVolumeWasher(f,g)
                    self.entry5.delete(0,END)
                    self.entry5.insert(0,volume)
                else:
                    volume = solveVolumeDisk(f)
                    self.entry5.delete(0,END)
                    self.entry5.insert(0,volume)


            

class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text = "Help")
        label.grid(pady=10, padx=10)
        button1 = tk.Button(self, text="Back",command=lambda:controller.show_frame(GraphPage))
        button1.grid(row=0,column=0)

        helpTxt = """
        Type a function into f(x) and/or g(x)
        Click the Enter button to graph it 
        A function in f(x) will generate a revolved function and calculate volume using the disc method
        Adding a function in g(x) in addition to f(x) will generate two revolved functions and calculate volume using the washer methods
        Use the xmin and xmax text boxes to set the domain
        Use the mouse to rotate the graph, use right click to zoom
        Wiggle the graph to update it
        """

        label2 = tk.Label(self,text = helpTxt)
        label2.grid(pady=10, padx=10)
        


app = GraphTool()

app.mainloop()