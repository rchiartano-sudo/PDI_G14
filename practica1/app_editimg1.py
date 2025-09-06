
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageFilter, ImageOps
import numpy as np
import os

class EditorImagenesComparativo:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes - Vista Comparativa")
        self.root.geometry("1200x750")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.imagen_original = None
        self.imagen_actual = None
        self.imagen_original_tk = None
        self.imagen_actual_tk = None
        
        # Coeficientes YIQ
        self.coef_luminancia = 1.0
        self.coef_saturacion = 1.0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel superior - Imágenes comparativas
        frame_imagenes = tk.Frame(main_frame, bg='#f0f0f0')
        frame_imagenes.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame para imagen original
        frame_original = tk.LabelFrame(frame_imagenes, text="🖼️ Imagen Original", 
                                     font=('Arial', 10, 'bold'), bg='#f0f0f0')
        frame_original.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.label_original = tk.Label(frame_original, bg='#e0e0e0', 
                                     text="Carga una imagen para comenzar", 
                                     font=('Arial', 12), relief=tk.SUNKEN, bd=1)
        self.label_original.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para imagen modificada
        frame_modificada = tk.LabelFrame(frame_imagenes, text="🎨 Imagen Modificada", 
                                       font=('Arial', 10, 'bold'), bg='#f0f0f0')
        frame_modificada.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.label_modificada = tk.Label(frame_modificada, bg='#e0e0e0', 
                                       text="Los cambios aparecerán aquí", 
                                       font=('Arial', 12), relief=tk.SUNKEN, bd=1)
        self.label_modificada.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel inferior - Controles
        panel_controles = tk.Frame(main_frame, bg='#f0f0f0')
        panel_controles.pack(fill=tk.X, pady=(10, 0))
        
        # Grupo: Archivo
        frame_archivo = tk.LabelFrame(panel_controles, text="📁 Archivo", 
                                    font=('Arial', 10, 'bold'), bg='#f0f0f0')
        frame_archivo.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        btn_cargar = tk.Button(frame_archivo, text="Cargar Imagen", command=self.cargar_imagen,
                              bg='#4CAF50', fg='white', font=('Arial', 10), padx=10, pady=5, width=15)
        btn_cargar.pack(padx=5, pady=5)
        
        btn_guardar = tk.Button(frame_archivo, text="Guardar Imagen", command=self.guardar_imagen,
                               bg='#2196F3', fg='white', font=('Arial', 10), padx=10, pady=5, width=15)
        btn_guardar.pack(padx=5, pady=5)
        
        btn_original = tk.Button(frame_archivo, text="Restaurar Original", command=self.restaurar_original,
                                bg='#FF9800', fg='white', font=('Arial', 10), padx=10, pady=5, width=15)
        btn_original.pack(padx=5, pady=5)
        
        # Grupo: Transformaciones YIQ
        frame_yiq = tk.LabelFrame(panel_controles, text="🌈 Espacio YIQ", 
                                font=('Arial', 10, 'bold'), bg='#f0f0f0')
        frame_yiq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Luminancia (Y)
        tk.Label(frame_yiq, text="Luminancia (Y) - Coeficiente a:", 
                bg='#f0f0f0', font=('Arial', 9)).pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        self.slider_luminancia = tk.Scale(frame_yiq, from_=0.1, to=2.0, resolution=0.1,
                                        orient=tk.HORIZONTAL, command=self.ajustar_yiq,
                                        bg='#f0f0f0', length=150)
        self.slider_luminancia.set(1.0)
        self.slider_luminancia.pack(padx=5, pady=(0, 5))
        
        self.lbl_luminancia = tk.Label(frame_yiq, text="1.0", bg='#f0f0f0', 
                                      font=('Arial', 9))
        self.lbl_luminancia.pack(pady=(0, 10))
        
        # Saturación (I,Q)
        tk.Label(frame_yiq, text="Saturación (I,Q) - Coeficiente b:", 
                bg='#f0f0f0', font=('Arial', 9)).pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        self.slider_saturacion = tk.Scale(frame_yiq, from_=0.0, to=2.0, resolution=0.1,
                                         orient=tk.HORIZONTAL, command=self.ajustar_yiq,
                                         bg='#f0f0f0', length=150)
        self.slider_saturacion.set(1.0)
        self.slider_saturacion.pack(padx=5, pady=(0, 5))
        
        self.lbl_saturacion = tk.Label(frame_yiq, text="1.0", bg='#f0f0f0', 
                                      font=('Arial', 9))
        self.lbl_saturacion.pack(pady=(0, 10))
        
        # Botones predefinidos YIQ
        frame_botones_yiq = tk.Frame(frame_yiq, bg='#f0f0f0')
        frame_botones_yiq.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        btn_oscuro = tk.Button(frame_botones_yiq, text="Oscuro", command=lambda: self.set_yiq(0.7, 1.0),
                              bg='#333333', fg='white', font=('Arial', 8), width=8)
        btn_oscuro.pack(side=tk.LEFT, padx=(0, 2))
        
        btn_claro = tk.Button(frame_botones_yiq, text="Claro", command=lambda: self.set_yiq(1.3, 1.0),
                             bg='#CCCCCC', fg='black', font=('Arial', 8), width=8)
        btn_claro.pack(side=tk.LEFT, padx=2)
        
        btn_desaturar = tk.Button(frame_botones_yiq, text="Desaturar", command=lambda: self.set_yiq(1.0, 0.5),
                                 bg='#888888', fg='white', font=('Arial', 8), width=8)
        btn_desaturar.pack(side=tk.LEFT, padx=2)
        
        btn_bn = tk.Button(frame_botones_yiq, text="B/N", command=lambda: self.set_yiq(1.0, 0.0),
                          bg='#000000', fg='white', font=('Arial', 8), width=8)
        btn_bn.pack(side=tk.LEFT, padx=(2, 0))
        
        # Grupo: Transformaciones tradicionales
        frame_transform = tk.LabelFrame(panel_controles, text="🎨 Transformaciones", 
                                      font=('Arial', 10, 'bold'), bg='#f0f0f0')
        frame_transform.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.transform_var = tk.StringVar()
        self.combo_transform = ttk.Combobox(frame_transform, textvariable=self.transform_var,
                                          state='readonly', font=('Arial', 9), width=15)
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
        self.combo_transform.pack(padx=5, pady=5)
        
        # Grupo: Información
        frame_info = tk.LabelFrame(panel_controles, text="📊 Información", 
                                 font=('Arial', 10, 'bold'), bg='#f0f0f0')
        frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.text_info = tk.Text(frame_info, height=8, width=40, font=('Arial', 9),
                               bg='#ffffff', relief=tk.SUNKEN, bd=1)
        scrollbar = tk.Scrollbar(frame_info, orient=tk.VERTICAL, command=self.text_info.yview)
        self.text_info.configure(yscrollcommand=scrollbar.set)
        
        self.text_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self.text_info.insert(tk.END, "Esperando imagen...\n")
        self.text_info.config(state=tk.DISABLED)
        
        # Estado inicial
        self.actualizar_estado_controles()
    
    def rgb_to_yiq(self, rgb):
        """Convierte RGB normalizado a YIQ"""
        matriz_rgb_yiq = np.array([
            [0.299, 0.587, 0.114],
            [0.595716, -0.274453, -0.321263],
            [0.211456, -0.522591, 0.311135]
        ])
        return np.dot(rgb, matriz_rgb_yiq.T)
    
    def yiq_to_rgb(self, yiq):
        """Convierte YIQ a RGB normalizado"""
        matriz_yiq_rgb = np.array([
            [1.0, 0.9563, 0.6210],
            [1.0, -0.2721, -0.6474],
            [1.0, -1.1070, 1.7046]
        ])
        return np.dot(yiq, matriz_yiq_rgb.T)
    
    def aplicar_yiq(self, imagen, a=1.0, b=1.0):
        """Aplica transformación YIQ a la imagen"""
        if imagen is None:
            return None
        
        img_array = np.array(imagen, dtype=np.float32) / 255.0
        resultado = np.zeros_like(img_array)
        
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                if img_array.ndim == 3:
                    rgb = img_array[i, j, :3]
                    yiq = self.rgb_to_yiq(rgb)
                    
                    y = yiq[0] * a
                    i_val = yiq[1] * b
                    q_val = yiq[2] * b
                    
                    y = np.clip(y, 0.0, 1.0)
                    i_val = np.clip(i_val, -0.5957, 0.5957)
                    q_val = np.clip(q_val, -0.5226, 0.5226)
                    
                    yiq_modificado = np.array([y, i_val, q_val])
                    rgb_modificado = self.yiq_to_rgb(yiq_modificado)
                    rgb_modificado = np.clip(rgb_modificado, 0.0, 1.0)
                    resultado[i, j, :3] = rgb_modificado
                    
                    if img_array.shape[2] == 4:
                        resultado[i, j, 3] = img_array[i, j, 3]
                else:
                    gris = img_array[i, j]
                    gris_modificado = np.clip(gris * a, 0.0, 1.0)
                    resultado[i, j] = gris_modificado
        
        resultado = (resultado * 255).astype(np.uint8)
        return Image.fromarray(resultado)
    
    def ajustar_yiq(self, event=None):
        """Ajusta luminancia y saturación"""
        if self.imagen_original is None:
            return
        
        a = self.slider_luminancia.get()
        b = self.slider_saturacion.get()
        
        self.lbl_luminancia.config(text=f"{a:.1f}")
        self.lbl_saturacion.config(text=f"{b:.1f}")
        
        self.imagen_actual = self.aplicar_yiq(self.imagen_original, a, b)
        self.mostrar_imagenes_comparativas()
        self.actualizar_informacion()
    
    def set_yiq(self, a, b):
        """Establece valores específicos de YIQ"""
        self.slider_luminancia.set(a)
        self.slider_saturacion.set(b)
        self.ajustar_yiq()
    
    def cargar_imagen(self):
        """Carga una imagen desde archivo"""
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
                
                self.slider_luminancia.set(1.0)
                self.slider_saturacion.set(1.0)
                self.lbl_luminancia.config(text="1.0")
                self.lbl_saturacion.config(text="1.0")
                
                self.mostrar_imagenes_comparativas()
                self.actualizar_informacion()
                self.actualizar_estado_controles()
                
                messagebox.showinfo("Éxito", f"Imagen cargada correctamente\nDimensiones: {self.imagen_original.size}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
    
    def mostrar_imagenes_comparativas(self):
        """Muestra ambas imágenes lado a lado"""
        if self.imagen_original is None:
            return
        
        # Mostrar imagen original
        self.mostrar_imagen(self.imagen_original, self.label_original, "Original")
        
        # Mostrar imagen modificada
        if self.imagen_actual:
            self.mostrar_imagen(self.imagen_actual, self.label_modificada, "Modificada")
        else:
            self.label_modificada.config(image='', text="Los cambios aparecerán aquí")
    
    def mostrar_imagen(self, imagen, label, tipo):
        """Muestra una imagen en un label específico"""
        # Calcular tamaño disponible
        width = label.winfo_width() - 20
        height = label.winfo_height() - 20
        
        if width < 10 or height < 10:
            width, height = 300, 200
        
        # Redimensionar imagen
        imagen_redimensionada = imagen.copy()
        imagen_redimensionada.thumbnail((width, height), Image.Resampling.LANCZOS)
        
        # Convertir a PhotoImage
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
        
        # Guardar referencia y actualizar label
        if tipo == "Original":
            self.imagen_original_tk = imagen_tk
        else:
            self.imagen_actual_tk = imagen_tk
        
        label.configure(image=imagen_tk, text="")
    
    def actualizar_informacion(self):
        """Actualiza la información de la imagen"""
        if self.imagen_actual is None:
            return
        
        self.text_info.config(state=tk.NORMAL)
        self.text_info.delete(1.0, tk.END)
        
        a = self.slider_luminancia.get()
        b = self.slider_saturacion.get()
        
        info = f"""📊 INFORMACIÓN COMPARATIVA:

🖼️ IMAGEN ORIGINAL:
• Dimensiones: {self.imagen_original.width} x {self.imagen_original.height}
• Modo: {self.imagen_original.mode}

🎨 IMAGEN MODIFICADA:
• Dimensiones: {self.imagen_actual.width} x {self.imagen_actual.height}
• Modo: {self.imagen_actual.mode}

🌈 TRANSFORMACIÓN YIQ:
• Luminancia (a): {a:.1f}
• Saturación (b): {b:.1f}

EFECTOS APLICADOS:
- a < 1.0: Imagen más oscura
- a > 1.0: Imagen más clara
- b < 1.0: Colores menos saturados
- b = 0.0: Blanco y negro completo
"""
        self.text_info.insert(tk.END, info)
        self.text_info.config(state=tk.DISABLED)
    
    def actualizar_estado_controles(self):
        """Habilita/deshabilita controles según estado"""
        habilitar = self.imagen_actual is not None
        state = tk.NORMAL if habilitar else tk.DISABLED
        
        self.combo_transform.config(state=state)
        self.slider_luminancia.config(state=state)
        self.slider_saturacion.config(state=state)
    
    def restaurar_original(self):
        """Restaura la imagen original"""
        if self.imagen_original is not None:
            self.imagen_actual = self.imagen_original.copy()
            self.slider_luminancia.set(1.0)
            self.slider_saturacion.set(1.0)
            self.lbl_luminancia.config(text="1.0")
            self.lbl_saturacion.config(text="1.0")
            self.mostrar_imagenes_comparativas()
            self.actualizar_informacion()
    
    def guardar_imagen(self):
        """Guarda la imagen modificada"""
        if self.imagen_actual is None:
            messagebox.showwarning("Advertencia", "No hay imagen para guardar")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Guardar Imagen Modificada",
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
                messagebox.showinfo("Éxito", f"Imagen modificada guardada en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen:\n{str(e)}")
    
    def aplicar_transformacion(self, event):
        """Aplica transformaciones tradicionales"""
        if self.imagen_actual is None:
            return
        
        transformacion = self.transform_var.get()
        
        try:
            if transformacion == "Invertir Colores":
                self.imagen_actual = ImageOps.invert(self.imagen_actual.convert('RGB'))
            elif transformacion == "Escala de Grises":
                self.imagen_actual = self.imagen_actual.convert('L').convert('RGB')
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
            
            self.mostrar_imagenes_comparativas()
            self.actualizar_informacion()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar transformación:\n{str(e)}")
        
        self.combo_transform.current(0)
    
    def on_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        self.mostrar_imagenes_comparativas()

def main():
    root = tk.Tk()
    app = EditorImagenesComparativo(root)
    
    # Configurar eventos
    root.bind('<Configure>', app.on_resize)
    
    # Forzar redimensionamiento inicial después de un breve delay
    root.after(100, app.mostrar_imagenes_comparativas)
    
    root.mainloop()

if __name__ == "__main__":
    main()