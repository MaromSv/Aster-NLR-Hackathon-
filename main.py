import customtkinter as ctk
from tkinter import Canvas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataclasses import dataclass

from starGeneratorGui import StarGenerator

class starScribbler:
        
    def __init__(self):
        self.origin = (0, 0)
        self.vertexList = []
        self.edgesList = []
        self.dragBlock = False
        self.line = None
        self.canvasId = 0
        self.toplevel_window = None

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.geometry("1200x1000")
        self.root.title("Star Scribbler")
        self.root.update()

        self.labelTitle = ctk.CTkLabel(master=self.root, text="stArtist", font=('TkDefaultFont', 80))
        self.labelTitle.place(relx=0.4, rely=0)

        self.frame = ctk.CTkFrame(master=self.root,
                                  height= self.root.winfo_height()*0.9,
                                  width = self.root.winfo_width()*0.95,
                                  fg_color="darkblue")
        
        self.frame.place(relx=0.025, rely=0.1)

        self.buttonClearCanvas = ctk.CTkButton(master = self.root,
                               text="Clear canvas",
                               width=250,
                               height=40,
                               command=self.clearCanvas)
        self.buttonClearCanvas.place(relx=0.025,rely=0.95)

        self.buttonClearCanvas = ctk.CTkButton(master = self.root,
                               text="Undo",
                               width=250,
                               height=40,
                               command=self.undo)
        self.buttonClearCanvas.place(relx=0.025,rely=0.90)

        self.buttonGenerate = ctk.CTkButton(master = self.root,
                               text="Generate",
                               width=250,
                               height=90,
                               command=self.generate)
        self.buttonGenerate.place(relx=0.77, rely=0.90)

        self.canvas = ctk.CTkCanvas(master=self.frame, height= self.root.winfo_height()*0.775,
                                  width = self.root.winfo_width()*0.95)
       
        self.canvas.pack(expand=1)

        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.canvas.bind("<ButtonRelease-3>", self.rightClick)
        self.canvas.bind("<B1-Motion>", self.drag)

        self.root.update()

        self.root.mainloop()
    
    def clearCanvas(self):
        print(self.vertexList)
        print(self.edgesList)
        self.canvas.delete("all")
        self.vertexList = []
        self.edgesList = []
        self.root.update()

    def undo(self):
        self.canvas.delete(self.canvasId-1)
        self.canvas.delete(self.canvasId)
        self.canvasId -= 2

    def generate(self):
        print(self.vertexList)
        print(self.edgesList)

        self.toplevel_window = StarGenerator(self.root)
        #data = StarData()
        #data.draw_canvas()
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel(self.root)  
        else:
            self.toplevel_window.focus()
        """

    def rightClick(self, e):
        self.startEdge = True
        self.dragBlock = True


    def drag(self, e):
        if self.dragBlock == False and self.line is not None:
            self.canvas.coords(self.line, self.origin[0], self.origin[1], e.x, e.y)

    def release(self, e):
        self.draw = True
        self.dragBlock = True

        if len(self.vertexList) < 1:
            self.startEdge = True

        self.vertexX = e.x
        self.vertexY = e.y
        self.drawGraph()

    def drawGraph(self):
        # Drag point to another closest element if possible
        if len(self.vertexList) >= 1:
            point = Vertex(0, self.vertexX, self.vertexY)
            
            for vertex in self.vertexList:
                distance = Graph().getDistance(vertex, point) 
                if distance < 20:
                    self.draw = False
                    self.vertexX, self.vertexY = vertex.x, vertex.y
                    break

        # Check if vertex can be added
        if self.draw == True:
            if self.startEdge == False or len(self.vertexList) == 0:
                self.vertexList.append(Vertex(len(self.vertexList), self.vertexX, self.vertexY))
                self.canvasId = self.canvas.create_oval(self.vertexX-15, self.vertexY-15, self.vertexX+15, self.vertexY+15, fill="yellow", tags=("circle",))
                
            else:
                self.dragBlock = True
                return 0
        
        # Inserting endpoint vertex
        if self.startEdge == False:
            startPoint = Graph().getClosestVertexIndex(self.vertexList, self.origin)
            endPoint = Graph().getClosestVertexIndex(self.vertexList, (self.vertexX, self.vertexY))
        
            # Swap starting and ending vertex accordingly
            if startPoint > endPoint:
                (startPoint, endPoint) = (endPoint, startPoint)

            proposedEdge = Edge(self.vertexList[startPoint], self.vertexList[endPoint])
            
            # Check if edge is valid
            if startPoint != endPoint and (proposedEdge in self.edgesList) == False:
                self.canvas.coords(self.line, self.origin[0], self.origin[1], self.vertexX, self.vertexY)
                self.edgesList.append(proposedEdge)
                
                self.startEdge = True
                self.origin = (self.vertexX, self.vertexY)
                self.line = self.canvas.create_line(self.origin[0], self.origin[1], self.vertexX, self.vertexY, width=2, smooth=True)
                self.dragBlock = False
            else:
                self.canvas.coords(self.line, 0, 0, 0, 0)
                

        # Inserting startpoint vertex
        else:
            self.origin = (self.vertexX, self.vertexY)
            self.line = self.canvas.create_line(self.origin[0], self.origin[1], self.vertexX, self.vertexY, width=2, smooth=True)
            self.dragBlock = False

        # Lift circle to the top
        self.canvas.tag_raise("circle")
        self.startEdge = not self.startEdge

@dataclass
class Vertex:
    index: int
    x: float
    y: float

@dataclass
class Edge:
    vertex1: Vertex
    vertex2: Vertex

class Graph:
    def getDistance(self, vertex1, vertex2):
        return ((vertex1.x - vertex2.x)**2 + (vertex1.y - vertex2.y)**2)**0.5
    
    def getClosestVertexIndex(self, vertexList, origin):
        distances = []
        for vertex in vertexList:
            distances.append(self.getDistance(vertex, Vertex(0, origin[0], origin[1])))
        
        return distances.index(min(distances))


if __name__ == "__main__":        
    CTK_Window = starScribbler()
    #data = StarData()
    #data.draw_canvas()