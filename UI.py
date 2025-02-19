from Pipeline import TextToGraphPipeline
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import os

class KnowledgeGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Grafos de Conocimiento")
        self.max_characters = 500
        self.file_name = ""  # Atributo inicializado como cadena vacía

        # Estilo y configuración principal
        window_width = 900
        window_height = 600

        # Centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int((screen_height - window_height) / 2)
        position_right = int((screen_width - window_width) / 2)

        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.root.configure(bg="#F8FAFC")

        # Asegurar que la ventana principal esté siempre al frente al inicio
        self.root.lift()  # Levantar la ventana al frente
        self.root.attributes('-topmost', True)
        self.root.after(500, lambda: self.root.attributes('-topmost', False))  # Desactivar después de un pequeño retraso

        # Fondo decorativo con una imagen temática
        self.background_image = ImageTk.PhotoImage(Image.open("icons/background_graphs.webp").resize((900, 600), Image.Resampling.LANCZOS))
        background_label = tk.Label(self.root, image=self.background_image, bg="#F8FAFC", bd=0)
        background_label.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

        # Contenedor principal centrado
        main_frame = tk.Frame(self.root, bg="#FFFFFF", bd=0, highlightthickness=0, relief="flat")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

        # Iconos con bordes redondeados
        self.manual_icon = ImageTk.PhotoImage(Image.open("icons/manual.webp").resize((64, 64), Image.Resampling.LANCZOS))
        self.file_icon = ImageTk.PhotoImage(Image.open("icons/file.webp").resize((64, 64), Image.Resampling.LANCZOS))

        # Encabezado
        header_frame = tk.Frame(main_frame, bg="#FFFFFF")
        header_frame.pack(pady=40)

        title_label = tk.Label(header_frame, text="Generador de Grafos de Conocimiento", font=("Helvetica", 20, "bold"), bg="#FFFFFF", fg="#333")
        title_label.pack()

        subtitle_label = tk.Label(header_frame, text="Elija una opción para ingresar el texto:", font=("Helvetica", 14), bg="#FFFFFF", fg="#666")
        subtitle_label.pack(pady=5)

        # Opciones principales con bordes redondeados y colores suaves
        options_frame = tk.Frame(main_frame, bg="#FFFFFF")
        options_frame.pack(pady=40)

        manual_button = tk.Button(options_frame, text="Texto Manual", command=self.open_manual_window, font=("Helvetica", 14), image=self.manual_icon, compound="top", bg="#B8D8E8", fg="#333", relief="flat", padx=20, pady=20, bd=0, highlightthickness=0, borderwidth=2, highlightcolor="#D1EAF7")
        manual_button.grid(row=0, column=0, padx=40, pady=10, ipadx=10, ipady=10)

        file_button = tk.Button(options_frame, text="Importar Archivo", command=self.open_file_window, font=("Helvetica", 14), image=self.file_icon, compound="top", bg="#B8D8E8", fg="#333", relief="flat", padx=20, pady=20, bd=0, highlightthickness=0, borderwidth=2, highlightcolor="#D1EAF7")
        file_button.grid(row=0, column=1, padx=40, pady=10, ipadx=10, ipady=10)

        # Pie de página
        footer_label = tk.Label(main_frame, text="Transforma texto en grafos de conocimiento para representar relaciones y conceptos de manera clara y accesible.", font=("Helvetica", 10), bg="#FFFFFF", fg="#999")
        footer_label.pack(side="bottom", pady=20)

    def open_manual_window(self):
        manual_window = Toplevel(self.root)
        manual_window.transient(self.root)  # Hacerla dependiente de la ventana principal
        manual_window.grab_set()
        manual_window.title("Ingresar texto manualmente")
        manual_window.geometry("600x400+200+150")
        manual_window.configure(bg="#FFFFFF")

        # Asegurar que la ventana secundaria aparezca al frente
        manual_window.attributes('-topmost', True)
        manual_window.after(100, lambda: manual_window.attributes('-topmost', False))

        # Título
        label = tk.Label(manual_window, text=f"Ingrese su texto (máx. {self.max_characters} caracteres):", font=("Helvetica", 12), bg="#FFFFFF", fg="#333")
        label.pack(pady=10)

        # Cuadro de texto
        text_entry = tk.Text(manual_window, height=10, width=60, font=("Helvetica", 12), wrap="word", bg="#F7F9FB", fg="#333", relief="flat", bd=1)
        text_entry.pack(pady=10)

        # Etiqueta de conteo de caracteres
        char_count_label = tk.Label(manual_window, text=f"Caracteres usados: 0/{self.max_characters}", font=("Helvetica", 10), bg="#FFFFFF", fg="#666")
        char_count_label.pack(pady=5)

        def update_character_count(event=None):
            text_content = text_entry.get("1.0", "end-1c")
            text_length = len(text_content)

            char_count_label.config(text=f"Caracteres usados: {text_length}/{self.max_characters}")

            if text_length > self.max_characters:
                char_count_label.config(fg="red")
            else:
                char_count_label.config(fg="#666")

        text_entry.bind("<KeyRelease>", update_character_count)

        # Botón para enviar
        submit_button = tk.Button(manual_window, text="Generar Grafo", command=lambda: self.generate_graph(text_entry, manual_window), font=("Helvetica", 12), bg="#B8D8E8", fg="black", relief="flat")
        submit_button.pack(pady=10)

    def open_file_window(self):
        # Crear ventana secundaria
        file_window = Toplevel(self.root)
        file_window.transient(self.root)  # Hacerla dependiente de la principal
        file_window.grab_set()
        file_window.title("Importar texto desde archivo")
        file_window.geometry("600x400+250+200")
        file_window.configure(bg="#FFFFFF")

        # Asegurar que la ventana secundaria aparezca al frente
        file_window.attributes('-topmost', True)
        file_window.after(100, lambda: file_window.attributes('-topmost', False))

        # Diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(parent=file_window, filetypes=[("Archivos de texto", "*.txt")])

        if not file_path:
            # Si el usuario cancela, cerrar la ventana de archivo
            file_window.destroy()
            return

        try:
            # Leer el contenido del archivo
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.file_name = os.path.splitext(os.path.basename(file_path))[0]
        except Exception as e:
            # Mostrar error si ocurre un problema al leer el archivo
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            file_window.destroy()
            return

        # Título
        label = tk.Label(file_window, text=f"Edite su texto (máx. {self.max_characters} caracteres):", font=("Helvetica", 12), bg="#FFFFFF", fg="#333")
        label.pack(pady=10)

        # Cuadro de texto
        text_entry = tk.Text(file_window, height=10, width=60, font=("Helvetica", 12), wrap="word", bg="#F7F9FB", fg="#333", relief="flat", bd=1)
        text_entry.insert("1.0", content)
        text_entry.pack(pady=10)

        # Etiqueta de conteo de caracteres
        char_count_label = tk.Label(file_window, text=f"Caracteres usados: {len(content)}/{self.max_characters}", font=("Helvetica", 10), bg="#FFFFFF", fg="#666")
        char_count_label.pack(pady=5)

        def update_character_count(event=None):
            text_content = text_entry.get("1.0", "end-1c")
            text_length = len(text_content)

            char_count_label.config(text=f"Caracteres usados: {text_length}/{self.max_characters}")

            if text_length > self.max_characters:
                char_count_label.config(fg="red")
            else:
                char_count_label.config(fg="#666")

        text_entry.bind("<KeyRelease>", update_character_count)

        # Actualizar el color del contador al cargar el texto
        update_character_count()

        # Botón para enviar
        submit_button = tk.Button(file_window, text="Enviar", command=lambda: self.generate_graph(text_entry, file_window), font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat")
        submit_button.pack(pady=10)

    def generate_graph(self, text_entry, window):
        text = text_entry.get("1.0", "end-1c")
        if len(text) > self.max_characters:
            messagebox.showerror("Error", f"El texto excede el límite máximo de {self.max_characters} caracteres.")
            return

        # Crear ventana de progreso
        progress_window = Toplevel(self.root)
        progress_window.title("Progreso de Generación de Grafo")
        progress_window.geometry("400x200")
        progress_window.configure(bg="#FFFFFF")
        progress_label = tk.Label(progress_window, text="Iniciando...", font=("Helvetica", 12), bg="#FFFFFF", fg="#333", wraplength=350, justify="center")
        progress_label.pack(pady=20)

        # Asegurar que la ventana de progreso aparezca al frente
        progress_window.attributes('-topmost', True)
        # progress_window.after(100, lambda: progress_window.attributes('-topmost', False))

        

        def update_progress(message):
            progress_label.config(text=message)
            progress_window.update_idletasks()
            # Ocultar la imagen de cargando si el mensaje es de error o éxito
            
            if "Error" in message or "error" in message:
                progress_label.config(fg="#FF0000")  # Rojo

            elif "correctamente" in message:
                progress_label.config(fg="#333")  # Negro (predeterminado)  

        # Procesar el texto
        def process_pipeline():
            pipeline = TextToGraphPipeline(progress_callback=update_progress)
            pipeline.create_graph(text, file_name=self.file_name)

            # Cambiar el color del botón según el resultado
            success = "correctamente" in progress_label.cget("text")
            close_button_color = "#4CAF50" if success else "#FF0000"

            # Mostrar un botón para cerrar la ventana al finalizar
            close_button = tk.Button(
                progress_window,
                text="Cerrar",
                command=progress_window.destroy,
                font=("Helvetica", 12),
                bg=close_button_color,
                fg="white",
                relief="flat"
            )
            close_button.pack(pady=20)

        # Intervalo ajustado para iniciar el procesamiento
        self.root.after(1000, process_pipeline)  # Iniciar el procesamiento después de 1 segundo
        window.destroy()

