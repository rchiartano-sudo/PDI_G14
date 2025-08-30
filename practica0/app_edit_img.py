# app_editor_tkinter.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageFilter, ImageOps
import numpy as np
import os

class EditorImagenesTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes - IPDI")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.imagen_original = None
        self.imagen_actual = None
        self.imagen_tk = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Imagen
        left_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.SUNKEN, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.label_imagen = tk.Label(left_frame, bg='#e0e0e0', text="Carga una imagen para comenzar", 
                                    font=('Arial', 12), relief=tk.SUNKEN, bd=1)
        self.label_imagen.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel derecho - Controles
        right_frame = tk.Frame(main_frame, bg='#f0f0f0', width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Grupo: Archivo
        frame_archivo = tk.LabelFrame(right_frame, text="📁 Archivo", font=('Arial', 10, 'bold'), 
                                    bg='#f0f0f0', fg='#333333')
        frame_archivo.pack(fill=tk.X, pady=(0, 10))
        
        btn_cargar = tk.Button(frame_archivo, text="Cargar Imagen", command=self.cargar_imagen,
                              bg='#4CAF50', fg='white', font=('Arial', 10), padx=10, pady=5)
        btn_cargar.pack(fill=tk.X, padx=5, pady=5)
        
        btn_guardar = tk.Button(frame_archivo, text="Guardar Imagen", command=self.guardar_imagen,
                               bg='#2196F3', fg='white', font=('Arial', 10), padx=10, pady=5)
        btn_guardar.pack(fill=tk.X, padx=5, pady=5)
        
        btn_original = tk.Button(frame_archivo, text="Restaurar Original", command=self.restaurar_original,
                                bg='#FF9800', fg='white', font=('Arial', 10), padx=10, pady=5)
        btn_original.pack(fill=tk.X, padx=5, pady=5)
        
        # Grupo: Transformaciones
        frame_transform = tk.LabelFrame(right_frame, text="🎨 Transformaciones", font=('Arial', 10, 'bold'),
                                      bg='#f0f0f0', fg='#333333')
        frame_transform.pack(fill=tk.X, pady=(0, 10))
        
        # Combobox de transformaciones
        self.transform_var = tk.StringVar()
        self.combo_transform = ttk.Combobox(frame_transform, textvariable=self.transform_var,
                                          state='readonly', font=('Arial', 9))
        self.combo_transform['values'] = (
            'Seleccionar...',
            'Invertir Colores',
            'Escala de Grises',
            'Rotar 90° Derecha',
            'Rotar 90° Izquierda',
            'Espejo Horizontal',
            'Espejo Vertical',
            'Desenfoque',
            'Realce de Bordes',
            'Sepia',
            'Negativo',
            'Cuantizar Colores'
        )
        self.combo_transform.current(0)
        self.combo_transform.bind('<<ComboboxSelected>>', self.aplicar_transformacion)
        self.combo_transform.pack(fill=tk.X, padx=5, pady=5)
        
        # Botones de transformaciones rápidas
        frame_botones = tk.Frame(frame_transform, bg='#f0f0f0')
        frame_botones.pack(fill=tk.X, padx=5, pady=5)
        
        btn_invertir = tk.Button(frame_botones, text="Invertir", command=self.invertir_colores,
                               bg='#E91E63', fg='white', font=('Arial', 9), width=10)
        btn_invertir.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_grises = tk.Button(frame_botones, text="Grises", command=self.convertir_grises,
                              bg='#607D8B', fg='white', font=('Arial', 9), width=10)
        btn_grises.pack(side=tk.LEFT)
        
        # Grupo: Ajustes
        frame_ajustes = tk.LabelFrame(right_frame, text="⚙️ Ajustes", font=('Arial', 10, 'bold'),
                                    bg='#f0f0f0', fg='#333333')
        frame_ajustes.pack(fill=tk.X, pady=(0, 10))
        
        # Brillo
        tk.Label(frame_ajustes, text="Brillo:", bg='#f0f0f0', font=('Arial', 9)).pack(anchor=tk.W, padx=5)
        self.slider_brillo = tk.Scale(frame_ajustes, from_=-100, to=100, orient=tk.HORIZONTAL,
                                    command=self.ajustar_brillo_contraste, bg='#f0f0f0')
        self.slider_brillo.set(0)
        self.slider_brillo.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        # Contraste
        tk.Label(frame_ajustes, text="Contraste:", bg='#f0f0f0', font=('Arial', 9)).pack(anchor=tk.W, padx=5)
        self.slider_contraste = tk.Scale(frame_ajustes, from_=-100, to=100, orient=tk.HORIZONTAL,
                                       command=self.ajustar_brillo_contraste, bg='#f0f0f0')
        self.slider_contraste.set(0)
        self.slider_contraste.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        # Grupo: Información
        frame_info = tk.LabelFrame(right_frame, text="📊 Información", font=('Arial', 10, 'bold'),
                                 bg='#f0f0f0', fg='#333333')
        frame_info.pack(fill=tk.BOTH, expand=True)
        
        self.text_info = tk.Text(frame_info, height=8, width=30, font=('Arial', 9),
                               bg='#ffffff', relief=tk.SUNKEN, bd=1)
        scrollbar = tk.Scrollbar(frame_info, orient=tk.VERTICAL, command=self.text_info.yview)
        self.text_info.configure(yscrollcommand=scrollbar.set)
        
        self.text_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self.text_info.insert(tk.END, "Esperando imagen...\n")
        self.text_info.config(state=tk.DISABLED)
        
        # Estado inicial
        self.actualizar_estado_controles()
    
    def cargar_imagen(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=(
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("Todos los archivos", "*.*")
            )
        )
        
        if file_path:
            try:
                self.imagen_original = Image.open(file_path)
                self.imagen_actual = self.imagen_original.copy()
                
                self.mostrar_imagen()
                self.actualizar_informacion()
                self.actualizar_estado_controles()
                
                messagebox.showinfo("Éxito", f"Imagen cargada correctamente\nDimensiones: {self.imagen_original.size}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
    
    def guardar_imagen(self):
        if self.imagen_actual is None:
            messagebox.showwarning("Advertencia", "No hay imagen para guardar")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Guardar Imagen",
            defaultextension=".png",
            filetypes=(
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("BMP", "*.bmp"),
                ("TIFF", "*.tiff")
            )
        )
        
        if file_path:
            try:
                self.imagen_actual.save(file_path)
                messagebox.showinfo("Éxito", f"Imagen guardada en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen:\n{str(e)}")
    
    def mostrar_imagen(self):
        if self.imagen_actual is None:
            return
        
        # Redimensionar imagen para que quepa en el panel
        max_width = self.label_imagen.winfo_width() - 20
        max_height = self.label_imagen.winfo_height() - 20
        
        if max_width < 10 or max_height < 10:
            max_width, max_height = 600, 400
        
        imagen_redimensionada = self.imagen_actual.copy()
        imagen_redimensionada.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Convertir a PhotoImage para Tkinter
        self.imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
        self.label_imagen.configure(image=self.imagen_tk, text="")
    
    def actualizar_informacion(self):
        if self.imagen_actual is None:
            return
        
        self.text_info.config(state=tk.NORMAL)
        self.text_info.delete(1.0, tk.END)
        
        info = f"""📊 Información de la imagen:

• Dimensiones: {self.imagen_actual.width} x {self.imagen_actual.height}
• Modo: {self.imagen_actual.mode}
• Formato: {self.imagen_actual.format if self.imagen_actual.format else 'N/A'}

Transformaciones aplicadas:
- Brillo: {self.slider_brillo.get()}
- Contraste: {self.slider_contraste.get()}
"""
        self.text_info.insert(tk.END, info)
        self.text_info.config(state=tk.DISABLED)
    
    def actualizar_estado_controles(self):
        habilitar = self.imagen_actual is not None
        state = tk.NORMAL if habilitar else tk.DISABLED
        
        self.combo_transform.config(state=state)
        self.slider_brillo.config(state=state)
        self.slider_contraste.config(state=state)
    
    def restaurar_original(self):
        if self.imagen_original is not None:
            self.imagen_actual = self.imagen_original.copy()
            self.slider_brillo.set(0)
            self.slider_contraste.set(0)
            self.mostrar_imagen()
            self.actualizar_informacion()
    
    def aplicar_transformacion(self, event):
        if self.imagen_actual is None:
            return
        
        transformacion = self.transform_var.get()
        
        try:
            if transformacion == "Invertir Colores":
                self.invertir_colores()
            elif transformacion == "Escala de Grises":
                self.convertir_grises()
            elif transformacion == "Rotar 90° Derecha":
                self.imagen_actual = self.imagen_actual.rotate(-90, expand=True)
            elif transformacion == "Rotar 90° Izquierda":
                self.imagen_actual = self.imagen_actual.rotate(90, expand=True)
            elif transformacion == "Espejo Horizontal":
                self.imagen_actual = ImageOps.mirror(self.imagen_actual)
            elif transformacion == "Espejo Vertical":
                self.imagen_actual = ImageOps.flip(self.imagen_actual)
            elif transformacion == "Desenfoque":
                self.imagen_actual = self.imagen_actual.filter(ImageFilter.BLUR)
            elif transformacion == "Realce de Bordes":
                self.imagen_actual = self.imagen_actual.filter(ImageFilter.EDGE_ENHANCE)
            elif transformacion == "Sepia":
                self.aplicar_sepia()
            elif transformacion == "Negativo":
                self.imagen_actual = ImageOps.invert(self.imagen_actual)
            elif transformacion == "Cuantizar Colores":
                self.imagen_actual = self.imagen_actual.quantize(colors=16)
            
            self.mostrar_imagen()
            self.actualizar_informacion()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar transformación:\n{str(e)}")
        
        # Resetear combobox
        self.combo_transform.current(0)
    
    def invertir_colores(self):
        if self.imagen_actual:
            self.imagen_actual = ImageOps.invert(self.imagen_actual.convert('RGB'))
            self.mostrar_imagen()
            self.actualizar_informacion()
    
    def convertir_grises(self):
        if self.imagen_actual:
            self.imagen_actual = self.imagen_actual.convert('L').convert('RGB')
            self.mostrar_imagen()
            self.actualizar_informacion()
    
    def aplicar_sepia(self):
        if self.imagen_actual:
            # Convertir a array numpy para procesamiento
            img_array = np.array(self.imagen_actual)
            
            # Aplicar filtro sepia
            sepia_filter = np.array([[0.393, 0.769, 0.189],
                                   [0.349, 0.686, 0.168],
                                   [0.272, 0.534, 0.131]])
            
            if img_array.ndim == 3:
                sepia_img = np.dot(img_array, sepia_filter.T)
                sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
                self.imagen_actual = Image.fromarray(sepia_img)
            
            self.mostrar_imagen()
            self.actualizar_informacion()
    
    def ajustar_brillo_contraste(self, event=None):
        if self.imagen_original is None:
            return
        
        brillo = self.slider_brillo.get() / 100.0
        contraste = 1.0 + (self.slider_contraste.get() / 100.0)
        
        # Convertir a array numpy para procesamiento
        img_array = np.array(self.imagen_original, dtype=np.float32)
        
        # Aplicar brillo
        img_ajustada = img_array + (brillo * 255)
        
        # Aplicar contraste
        if img_array.ndim == 3:
            img_ajustada = (img_ajustada - 127.5) * contraste + 127.5
        else:
            img_ajustada = (img_ajustada - 127.5) * contraste + 127.5
        
        # Asegurar valores dentro del rango
        img_ajustada = np.clip(img_ajustada, 0, 255).astype(np.uint8)
        
        self.imagen_actual = Image.fromarray(img_ajustada)
        self.mostrar_imagen()
        self.actualizar_informacion()
    
    def on_resize(self, event):
        self.mostrar_imagen()

def main():
    root = tk.Tk()
    app = EditorImagenesTkinter(root)
    
    # Configurar evento de redimensionamiento
    root.bind('<Configure>', app.on_resize)
    
    root.mainloop()

if __name__ == "__main__":
    main()