import threading
from tkinter import *
from tkinter import filedialog
from moviepy.editor import *
from yt_dlp import YoutubeDL
import imageio_ffmpeg as ffmpeg

conversion_en_progreso = False

def convertir_a_mp3(url, output_path, label_advertencia, boton_convertir, boton_carpeta):
    # Deshabilitar el botón "Convertir a MP3"
    boton_convertir.config(state=DISABLED)
    # Deshabilitar el botón "Elegir carpeta"
    boton_carpeta.config(state=DISABLED)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg.get_ffmpeg_exe(),
        'keepvideo': False,
        'playlistend': 1  # Convertir solo el primer video de la lista de reproducción
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            label_advertencia.config(text="Conversión finalizada. Archivo MP3 guardado correctamente.", fg="green")
        except Exception as e:
            label_advertencia.config(text=f"Error durante la conversión: {str(e)}", fg="red")

    # Reiniciar la variable de conversión en progreso
    global conversion_en_progreso
    conversion_en_progreso = False

    # Habilitar el botón "Convertir a MP3" después de la conversión
    boton_convertir.config(state=NORMAL)
    # Habilitar el botón "Elegir carpeta" después de la conversión
    boton_carpeta.config(state=NORMAL)

def elegir_carpeta():
    carpeta = filedialog.askdirectory()
    entry_carpeta.delete(0, END)
    entry_carpeta.insert(0, carpeta)

def convertir():
    url = entry_url.get()
    carpeta = entry_carpeta.get()
    if not url:
        label_advertencia.config(text="¡Debes ingresar una URL!", fg="red")
        return
    if not carpeta:
        label_advertencia.config(text="¡Debes elegir una carpeta de destino!", fg="red")
        return

    global conversion_en_progreso
    if conversion_en_progreso:
        return
    conversion_en_progreso = True

    label_advertencia.config(text="Convirtiendo el video en audio...", fg="dark goldenrod")

    thread = threading.Thread(target=convertir_a_mp3, args=(url, carpeta, label_advertencia, boton_convertir, boton_carpeta))
    thread.start()

# Crear la ventana de la aplicación
root = Tk()
root.title("ConvertYTMP3")

# Obtener el ancho y alto de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Obtener el ancho y alto de la ventana
window_width = 590
window_height = 130

# Calcular las coordenadas para centrar la ventana en la pantalla
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# Establecer la posición de la ventana en el centro de la pantalla
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Evitar que la ventana se pueda redimensionar
root.resizable(False, False)

# Crear widgets
label_url = Label(root, text="URL:")
entry_url = Entry(root, width=50)
label_carpeta = Label(root, text="Carpeta:")
entry_carpeta = Entry(root, width=50)
boton_carpeta = Button(root, text="Elegir carpeta", command=elegir_carpeta)
boton_convertir = Button(root, text="Convertir a MP3", command=convertir)
label_advertencia = Label(root, fg="red")

# Posicionar widgets en la ventana
label_url.grid(row=0, column=0, padx=5, pady=5, sticky=W)
entry_url.grid(row=0, column=1, padx=5, pady=5)
label_carpeta.grid(row=1, column=0, padx=5, pady=5, sticky=W)
entry_carpeta.grid(row=1, column=1, padx=5, pady=5)
boton_carpeta.grid(row=1, column=2, padx=5, pady=5)
boton_convertir.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
label_advertencia.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Ejecutar la ventana de la aplicación
root.mainloop()
