# -----------------------------------------------------------------------------
# -----  Implementación de librerías tkinter and matplotlib    ----------------
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter.ttk import Combobox, Button, Label
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from tkinter import Tk, Button
from tkinter import messagebox
# -----------------------------------------------------------------------------
# ------------  Importamos los datos desde un DB almacenada    ----------------
# -----------------------------------------------------------------------------

with open('JSON/cant_crimenes.txt', 'r') as file:
    cant_crimines = json.load(file)

with open('JSON/areas.txt', 'r') as file:
    areas = json.load(file)

with open('JSON/grafo.txt', 'r') as file:
    grafo = json.load(file)

# -----------------------------------------------------------------------------
# -----------------------------  Grafo vació    -------------------------------
# -----------------------------------------------------------------------------

G = nx.Graph()


for area, num_area in areas.items():  # agregar nodos
    G.add_node(num_area, label=area)

# Agregar aristas al grafo con los números correspondientes
for num_area, neighbors in grafo["AREA"].items():
    for neighbor, weight in neighbors.items():
        G.add_edge(num_area, neighbor, weight=weight)


# -----------------------------------------------------------------------------
# ---------------------  Función implementada con disktra    ------------------
# -----------------------------------------------------------------------------
def Buscar_Ruta_Corta():
    area_origen = area1.get()  #Obtener datos
    area_destino = area2.get()

    if area_origen == area_destino:
        messagebox.showwarning("Alerta", "Areas Iguales")
        return

    try:
        id_origin = areas[area_origen]
        id_destino = areas[area_destino]

        ruta_corta = nx.dijkstra_path(G, id_origin, id_destino, weight='weight')
        calcular_distancia = nx.dijkstra_path_length(G, id_origin, id_destino, weight='weight')

        Area_Visitada = [G.nodes[num]['label'] for num in ruta_corta]
        areas_seguras = "\n -> ".join(Area_Visitada)
        resultado.config(

            text=f"RUTA RECOMENDADA Y SEGURA:\n\n "
                 f"-> {areas_seguras}\n\n"
                 f"Distancia: {calcular_distancia} Kilómetros Apróx.")

        edges = list(zip(ruta_corta, ruta_corta[1:]))
        ax.clear()  # Limpiar al pantalla
        pos = nx.spring_layout(G)
        labels = {num: G.nodes[num]['label'] for num in G.nodes}

        node_colors = ['#DC4E30' if cant_crimines[G.nodes[node]['label']] > 100
                       else '#6AA1DF' for node in G.nodes]

        nx.draw(G, pos, with_labels=True, labels=labels,
                node_color=node_colors, node_size=600,
                edge_color='gray', ax=ax)

        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='green', width=2.0, ax=ax)

        canvas.draw()

        for num in ruta_corta:
        #        resultado.config(text="Alerta: El camino pasa por áreas con alto riesgo de crimen.")
            if cant_crimines[G.nodes[num]['label']] > 100:
                messagebox.showwarning("Alerta", "Zonas con alto riesgo de crimen!!")
                break

    except KeyError:
        resultado.config(text="Error!!")


# -----------------------------------------------------------------------------
# -------------------------  Crear la ventana principal  ----------------------
# -----------------------------------------------------------------------------
ventana = tk.Tk()
ventana.geometry("800x650")
ventana.configure(bg="#3A2C6C")
ventana.title("Trabajo Final - Universidad Peruana de Ciencias Aplicadas")
ventana.iconbitmap("JSON/U.ico")


# -----------------------------------------------------------------------------
# -----------------------  Listas desplegables en label  ----------------------
# -----------------------------------------------------------------------------

label1 = tk.Label(ventana, text="Área de origen:")

label1.place(x=10, y=40, width=100, height=30)
area1 = Combobox(ventana, values=list(areas.keys()))
area1.place(x=120, y=40, width=120, height=30)

label2 = tk.Label(ventana, text="Área de destino:")
label2.place(x=10, y=80, width=100, height=30)
area2 = Combobox(ventana, values=list(areas.keys()))
area2.place(x=120, y=80, width=120, height=30)

# -----------------------------------------------------------------------------
# ------------------  Botón para calcular la ruta más corta  ------------------
# -----------------------------------------------------------------------------
btn = Button(ventana, text="Buscar ruta", command=Buscar_Ruta_Corta, bg="yellow", fg="black")
btn.place(x=110, y=130, width=100, height=30)

# -----------------------------------------------------------------------------
# --------------  Label para mostrar los resultados del camino  ---------------
# -----------------------------------------------------------------------------
resultado = Label(ventana, text="", wraplength=780, justify="left")
resultado.place(x=20, y=210, width=255, height=400)

# -----------------------------------------------------------------------------
# ---------------------  Figura para mostrar el grafo  ------------------------
# -----------------------------------------------------------------------------
fig = plt.Figure(figsize=(10, 7))
ax = fig.add_subplot(111)

# -----------------------------------------------------------------------------
# ------------------------  Grafo inicial al ejecutar  ------------------------
# -----------------------------------------------------------------------------
pos = nx.spring_layout(G)
labels = {num: G.nodes[num]['label'] for num in G.nodes}
nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue',
        node_size=800, edge_color='gray', ax=ax)

# -----------------------------------------------------------------------------
# ---------------------------  Posición del gráfico  --------------------------
# -----------------------------------------------------------------------------
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.draw()
canvas.get_tk_widget().place(x=300, y=0, width=1150)

# -----------------------------------------------------------------------------
# ---------------------------  Ventana Principal  -----------------------------
# -----------------------------------------------------------------------------

ventana.mainloop()

# -----------------------------------------------------------------------------
# -----------------------------  Fin del código  ------------------------------
# -----------------------------------------------------------------------------