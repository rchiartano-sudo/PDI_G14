# app_editor_tkinter_yiq.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageFilter, ImageOps
import numpy as np
import os

class EditorImagenesTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes - IPDI - Espacio YIQ")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.imagen_original = None
        self.imagen_actual = None
        self.imagen_tk = None
        
        # Coeficientes YIQ
        self.coef_luminancia = 1.0
        self.coef_saturacion = 1.0
        
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
        right_frame = tk.Frame(main_frame, bg='#f0f0f0', width=350)
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
        
        # Grupo: Transformaciones YIQ
        frame_yiq = tk.LabelFrame(right_frame, text="🌈 Espacio YIQ", font=('Arial', 10, 'bold'),
                                bg='#f0f0f0', fg='#333333')
        frame_yiq.pack(fill=tk.X, pady=(0, 10))
        
        # Luminancia (Y)
        tk.Label(frame_yiq, text="Luminancia (Y) - Coeficiente a:", 
                bg='#f0f0f0', font=('Arial', 9)).pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        frame_luminancia = tk.Frame(frame_yiq, bg='#f0f0f0')
        frame_luminancia.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        self.slider_luminancia = tk.Scale(frame_luminancia, from_=0.1, to=2.0, resolution=0.1,
                                        orient=tk.HORIZONTAL, command=self.ajustar_yiq,
                                        bg='#f0f0f0', length=200)
        self.slider_luminancia.set(1.0)
        self.slider_luminancia.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.lbl_luminancia = tk.Label(frame_luminancia, text="1.0", bg='#f0f0f0', 
                                      font=('Arial', 9), width=5)
        self.lbl_luminancia.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Saturación (I,Q)
        tk.Label(frame_yiq, text="Saturación (I,Q) - Coeficiente b:", 
                bg='#f0f0f0', font=('Arial', 9)).pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        frame_saturacion = tk.Frame(frame_yiq, bg='#f0f0f0')
        frame_saturacion.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        self.slider_saturacion = tk.Scale(frame_saturacion, from_=0.0, to=2.0, resolution=0.1,
                                         orient=tk.HORIZONTAL, command=self.ajustar_yiq,
                                         bg='#f0f0f0', length=200)
        self.slider_saturacion.set(1.0)
        self.slider_saturacion.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.lbl_saturacion = tk.Label(frame_saturacion, text="1.0", bg='#f0f0f0', 
                                      font=('Arial', 9), width=5)
        self.lbl_saturacion.pack(side=tk.RIGHT, padx=(5, 0))
        
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
        
        btn_bn = tk.Button(frame_botones_yiq, text="Blanco/Negro", command=lambda: self.set_yiq(1.0, 0.0),
                          bg='#000000', fg='white', font=('Arial', 8), width=10)
        btn_bn.pack(side=tk.LEFT, padx=(2, 0))
        
        # Grupo: Transformaciones tradicionales
        frame_transform = tk.LabelFrame(right_frame, text="🎨 Transformaciones", font=('Arial', 10, 'bold'),
                                      bg='#f0f0f0', fg='#333333')
        frame_transform.pack(fill=tk.X, pady=(0, 10))
        
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
        
        # Grupo: Información
        frame_info = tk.LabelFrame(right_frame, text="📊 Información", font=('Arial', 10, 'bold'),
                                 bg='#f0f0f0', fg='#333333')
        frame_info.pack(fill=tk.BOTH, expand=True)
        
        self.text_info = tk.Text(frame_info, height=10, width=30, font=('Arial', 9),
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
        # Matriz de conversión RGB -> YIQ
        matriz_rgb_yiq = np.array([
            [0.299, 0.587, 0.114],
            [0.595716, -0.274453, -0.321263],
            [0.211456, -0.522591, 0.311135]
        ])
        
        return np.dot(rgb, matriz_rgb_yiq.T)
    
    def yiq_to_rgb(self, yiq):
        """Convierte YIQ a RGB normalizado"""
        # Matriz de conversión YIQ -> RGB
        matriz_yiq_rgb = np.array([
            [1.0, 0.9563, 0.6210],
            [1.0, -0.2721, -0.6474],
            [1.0, -1.1070, 1.7046]
        ])
        
        return np.dot(yiq, matriz_yiq_rgb.T)
    
    def aplicar_yiq(self, imagen, a=1.0, b=1.0):
        """
        Aplica transformación YIQ a la imagen
        a: coeficiente de luminancia (Y)
        b: coeficiente de saturación (I,Q)
        """
        if imagen is None:
            return None
        
        # Convertir imagen a array numpy y normalizar
        img_array = np.array(imagen, dtype=np.float32) / 255.0
        
        # Aplicar transformación a cada pixel
        resultado = np.zeros_like(img_array)
        
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                if img_array.ndim == 3:  # Imagen color
                    rgb = img_array[i, j, :3]
                    
                    # 1. Convertir RGB -> YIQ
                    yiq = self.rgb_to_yiq(rgb)
                    
                    # 2. Aplicar coeficientes
                    y = yiq[0] * a  # Y' = a * Y
                    i_val = yiq[1] * b  # I' = b * I
                    q_val = yiq[2] * b  # Q' = b * Q
                    
                    # 3. Chequear límites
                    y = np.clip(y, 0.0, 1.0)  # Y' <= 1
                    i_val = np.clip(i_val, -0.5957, 0.5957)  # -0.5957 < I' < 0.5957
                    q_val = np.clip(q_val, -0.5226, 0.5226)  # -0.5226 < Q' < 0.5226
                    
                    # 4. Convertir Y'I'Q' -> R'G'B'
                    yiq_modificado = np.array([y, i_val, q_val])
                    rgb_modificado = self.yiq_to_rgb(yiq_modificado)
                    
                    # 5. Asegurar valores en [0, 1] y convertir a bytes
                    rgb_modificado = np.clip(rgb_modificado, 0.0, 1.0)
                    resultado[i, j, :3] = rgb_modificado
                    
                    # Mantener canal alpha si existe
                    if img_array.shape[2] == 4:
                        resultado[i, j, 3] = img_array[i, j, 3]
                
                else:  # Imagen escala de grises
                    # Para imágenes en escala de grises, solo ajustar luminancia
                    gris = img_array[i, j]
                    gris_modificado = np.clip(gris * a, 0.0, 1.0)
                    resultado[i, j] = gris_modificado
        
        # Convertir de vuelta a bytes
        resultado = (resultado * 255).astype(np.uint8)
        return Image.fromarray(resultado)
    
    def ajustar_yiq(self, event=None):
        """Ajusta luminancia y saturación usando sliders"""
        if self.imagen_original is None:
            return
        
        a = self.slider_luminancia.get()
        b = self.slider_saturacion.get()
        
        # Actualizar labels
        self.lbl_luminancia.config(text=f"{a:.1f}")
        self.lbl_saturacion.config(text=f"{b:.1f}")
        
        # Aplicar transformación YIQ
        self.imagen_actual = self.aplicar_yiq(self.imagen_original, a, b)
        self.mostrar_imagen()
        self.actualizar_informacion()
    
    def set_yiq(self, a, b):
        """Establece valores específicos de YIQ"""
        self.slider_luminancia.set(a)
        self.slider_saturacion.set(b)
        self.ajustar_yiq()
    
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
                
                # Resetear sliders YIQ
                self.slider_luminancia.set(1.0)
                self.slider_saturacion.set(1.0)
                self.lbl_luminancia.config(text="1.0")
                self.lbl_saturacion.config(text="1.0")
                
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
        
        a = self.slider_luminancia.get()
        b = self.slider_saturacion.get()
        
        info = f"""📊 Información de la imagen:

• Dimensiones: {self.imagen_actual.width} x {self.imagen_actual.height}
• Modo: {self.imagen_actual.mode}
• Formato: {self.imagen_original.format if self.imagen_original.format else 'N/A'}

🌈 Transformación YIQ:
- Luminancia (a): {a:.1f}
- Saturación (b): {b:.1f}

Efectos esperados:
- a < 1.0: Imagen más oscura
- a > 1.0: Imagen más clara (puede generar artefactos)
- b < 1.0: Colores menos saturados
- b = 0.0: Blanco y negro
- b > 1.0: Colores más saturados
"""
        self.text_info.insert(tk.END, info)
        self.text_info.config(state=tk.DISABLED)
    
    def actualizar_estado_controles(self):
        habilitar = self.imagen_actual is not None
        state = tk.NORMAL if habilitar else tk.DISABLED
        
        self.combo_transform.config(state=state)
        self.slider_luminancia.config(state=state)
        self.slider_saturacion.config(state=state)
    
    def restaurar_original(self):
        if self.imagen_original is not None:
            self.imagen_actual = self.imagen_original.copy()
            self.slider_luminancia.set(1.0)
            self.slider_saturacion.set(1.0)
            self.lbl_luminancia.config(text="1.0")
            self.lbl_saturacion.config(text="1.0")
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