import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageTk
import io
import configparser
# Obtener todos los formatos soportados por Pillow
FORMATOS_IMAGEN = [ext[1:].upper() for ext in Image.registered_extensions().keys()]

# Añadir manualmente el formato WEBP si no está registrado automáticamente
if "WEBP" not in FORMATOS_IMAGEN:
    FORMATOS_IMAGEN.append("WEBP")

# Configuración para el archivo INI
config_file = "config.ini"
config = configparser.ConfigParser()

# Función para cargar la configuración del archivo INI
def cargar_configuracion():
    if config.read(config_file):
        entry_ancho.insert(0, config.getint('Imagen', 'ancho', fallback=300))
        entry_alto.insert(0, config.getint('Imagen', 'alto', fallback=300))
        slider_calidad.set(config.getint('Imagen', 'calidad', fallback=100))
        formato_var.set(config.get('Imagen', 'formato', fallback="JPEG"))

        # Configuraciones de colores
        fondo_color = config.get('Colores', 'fondo', fallback="#FFFFFF")
        root.config(bg=fondo_color)
    else:
        config['Imagen'] = {
            'ancho': '300',
            'alto': '300',
            'calidad': '100',
            'formato': 'JPEG'
        }
        config['Colores'] = {
            'fondo': '#FFFFFF',
        }
        with open(config_file, 'w') as file:
            config.write(file)

# Función para guardar la configuración en el archivo INI
def guardar_configuracion():
    config['Imagen'] = {
        'ancho': entry_ancho.get(),
        'alto': entry_alto.get(),
        'calidad': str(slider_calidad.get()),
        'formato': formato_var.get()
    }
    config['Colores'] = {
        'fondo': root.cget('bg'),
    }
    with open(config_file, 'w') as file:
        config.write(file)

# Función para cambiar el color de fondo
def cambiar_color_fondo():
    color_fondo = colorchooser.askcolor()[1]
    if color_fondo:
        root.config(bg=color_fondo)
        for widget in root.winfo_children():
            widget.config(bg=color_fondo)

# Crear un apartado de configuración
def abrir_configuracion():
    config_window = tk.Toplevel(root)
    config_window.title("Configuración de Colores")
    
    tk.Label(config_window, text="Color de Fondo:").pack(pady=5)
    btn_fondo = tk.Button(config_window, text="Cambiar Color de Fondo", command=cambiar_color_fondo)
    btn_fondo.pack(pady=5)
    
    tk.Button(config_window, text="Guardar Configuración", command=guardar_configuracion).pack(pady=10)

# Función para mostrar la ayuda
def mostrar_ayuda():
    mensaje_ayuda = (
        "Las funciones que tiene el adaptador son las siguientes: \n \n"
        "Redimensionamiento automático: Ajusta el tamaño de las imágenes según las necesidades del diseño responsivo.\n \n"
        "Compresión: Reduce el tamaño del archivo para mejorar la velocidad de carga, sin perder calidad visual. \n \n"
        "Conversión de formatos: Transforma las imágenes a formatos más eficientes como WebP u otros.\n \n"
        "Carga diferida (lazy loading): Carga las imágenes solo cuando son visibles en la pantalla."
    )
    messagebox.showinfo("Ayuda", mensaje_ayuda)


# Función para seleccionar una imagen
def seleccionar_imagen():
    global img_original, img_preview
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff;*.webp")])
    if ruta_imagen:
        img_original = Image.open(ruta_imagen)
        mostrar_imagen_original(img_original)
        
        label_dimensiones_original.config(text=f"Dimensiones Originales: {img_original.width} x {img_original.height} px")
        entry_ancho.delete(0, tk.END)
        entry_ancho.insert(0, img_original.width)
        entry_alto.delete(0, tk.END)
        entry_alto.insert(0, img_original.height)
        
        btn_modificar.config(state=tk.NORMAL)
        btn_guardar.config(state=tk.NORMAL)

# Función para mostrar la imagen original en el canvas
def mostrar_imagen_original(imagen):
    global img_preview
    img_preview = ImageTk.PhotoImage(imagen)
    canvas_original.create_image(0, 0, anchor=tk.NW, image=img_preview)
    canvas_original.config(scrollregion=canvas_original.bbox(tk.ALL))

# Función para mostrar la imagen modificada en el canvas
def mostrar_imagen_modificada(imagen):
    global img_modificada
    img_modificada = ImageTk.PhotoImage(imagen)
    canvas_modificada.create_image(0, 0, anchor=tk.NW, image=img_modificada)
    canvas_modificada.config(scrollregion=canvas_modificada.bbox(tk.ALL))

# Función para modificar la imagen (tamaño y calidad) y mostrar la imagen modificada
def modificar_imagen():
    global img_original
    if img_original:
        try:
            nuevo_ancho = int(entry_ancho.get())
            nuevo_alto = int(entry_alto.get())
            calidad = slider_calidad.get()
            formato_seleccionado = formato_var.get().upper()

            img_redimensionada = img_original.resize((nuevo_ancho, nuevo_alto))
            with io.BytesIO() as output:
                img_redimensionada.save(output, format=formato_seleccionado, quality=calidad if formato_seleccionado == "JPEG" else None)
                output.seek(0)
                img_modificada_pillow = Image.open(output)
                mostrar_imagen_modificada(img_modificada_pillow)

            label_dimensiones_modificada.config(text=f"Dimensiones Modificadas: {img_redimensionada.width} x {img_redimensionada.height} px")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.")
    else:
        messagebox.showerror("Error", "Por favor, selecciona una imagen primero.")

# Función para guardar la imagen modificada
def guardar_imagen():
    if img_original:
        try:
            nuevo_ancho = int(entry_ancho.get())
            nuevo_alto = int(entry_alto.get())
            calidad = slider_calidad.get()

            img_redimensionada = img_original.resize((nuevo_ancho, nuevo_alto))
            formato_seleccionado = formato_var.get().upper()
            ruta_guardado = filedialog.asksaveasfilename(defaultextension=f".{formato_seleccionado.lower()}",
                                                         filetypes=[(formato_seleccionado, f"*.{formato_seleccionado.lower()}")])
            if ruta_guardado:
                if formato_seleccionado == "JPEG":
                    img_redimensionada.save(ruta_guardado, formato_seleccionado, quality=calidad)
                else:
                    img_redimensionada.save(ruta_guardado, formato_seleccionado)
                messagebox.showinfo("Éxito", "Imagen guardada exitosamente.")
                
                guardar_configuracion()  # Guardar configuración al guardar la imagen
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.")
    else:
        messagebox.showerror("Error", "Por favor, selecciona una imagen primero.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Adaptador de Fotos")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

menu_ayuda = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Mostrar Ayuda", command=mostrar_ayuda)

menu_config = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Configuración", menu=menu_config)
menu_config.add_command(label="Configuración de Colores", command=abrir_configuracion)

frame_original = tk.Frame(root)
frame_original.grid(row=0, column=0, padx=10, pady=10)

frame_modificada = tk.Frame(root)
frame_modificada.grid(row=0, column=1, padx=10, pady=10)

canvas_original = tk.Canvas(frame_original, width=300, height=300, bg="white")
canvas_original.pack(side=tk.LEFT)

scroll_y_original = tk.Scrollbar(frame_original, orient="vertical", command=canvas_original.yview)
scroll_x_original = tk.Scrollbar(frame_original, orient="horizontal", command=canvas_original.xview)
canvas_original.configure(yscrollcommand=scroll_y_original.set, xscrollcommand=scroll_x_original.set)
scroll_y_original.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x_original.pack(side=tk.BOTTOM, fill=tk.X)

canvas_modificada = tk.Canvas(frame_modificada, width=300, height=300, bg="white")
canvas_modificada.pack(side=tk.LEFT)

scroll_y_modificada = tk.Scrollbar(frame_modificada, orient="vertical", command=canvas_modificada.yview)
scroll_x_modificada = tk.Scrollbar(frame_modificada, orient="horizontal", command=canvas_modificada.xview)
canvas_modificada.configure(yscrollcommand=scroll_y_modificada.set, xscrollcommand=scroll_x_modificada.set)
scroll_y_modificada.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x_modificada.pack(side=tk.BOTTOM, fill=tk.X)

btn_seleccionar = tk.Button(root, text="Seleccionar Imagen", command=seleccionar_imagen)
btn_seleccionar.grid(row=1, column=0, padx=10, pady=10)

label_dimensiones_original = tk.Label(root, text="Dimensiones Originales:")
label_dimensiones_original.grid(row=2, column=0, padx=10, pady=10)

label_dimensiones_modificada = tk.Label(root, text="Dimensiones Modificadas:")
label_dimensiones_modificada.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Ancho:").grid(row=3, column=0, padx=10, pady=10)
entry_ancho = tk.Entry(root, width=10)
entry_ancho.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Alto:").grid(row=4, column=0, padx=10, pady=10)
entry_alto = tk.Entry(root, width=10)
entry_alto.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root, text="Calidad:").grid(row=5, column=0, padx=10, pady=10)
slider_calidad = tk.Scale(root, from_=1, to=100, orient="horizontal")
slider_calidad.grid(row=5, column=1, padx=10, pady=10)

tk.Label(root, text="Formato:").grid(row=6, column=0, padx=10, pady=10)
formato_var = tk.StringVar()
combobox_formato = ttk.Combobox(root, textvariable=formato_var, values=FORMATOS_IMAGEN, state="readonly")
combobox_formato.grid(row=6, column=1, padx=10, pady=10)

btn_modificar = tk.Button(root, text="Modificar Imagen", command=modificar_imagen, state=tk.DISABLED)
btn_modificar.grid(row=7, column=0, padx=10, pady=10)

btn_guardar = tk.Button(root, text="Guardar Imagen", command=guardar_imagen, state=tk.DISABLED)
btn_guardar.grid(row=7, column=1, padx=10, pady=10)

cargar_configuracion()
root.mainloop()
