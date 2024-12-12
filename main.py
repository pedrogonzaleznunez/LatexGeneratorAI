import tkinter as tk
from tkinter import messagebox, filedialog
import ollama
import subprocess
import os

def delete_files():
    try:
        os.remove("output.tex")
    except FileNotFoundError:
        pass
    try:
        os.remove("output.pdf")
    except FileNotFoundError:
        pass
    try:
        os.remove("output.log")
    except FileNotFoundError:
        pass
    try:
        os.remove("output.aux")
    except FileNotFoundError:
        pass


def generar_pdf():

    delete_files()

    pre_prompt = r"""
Eres un asistente especializado en generar únicamente código en LaTeX para diagramas en TikZ. Cualquier respuesta debe estar exclusivamente en formato LaTeX, sin explicaciones ni texto adicional. Devuelve solo el código en un formato compilable.

Reglas importantes:
1. Salida esperada: Solo código en LaTeX, sin comentarios, explicaciones, ni contenido adicional.
2. Estructura del documento: Configura correctamente las librerías necesarias en cada respuesta.
3. Librerías permitidas: 
   - shapes.geometric
   - arrows.meta
   - positioning
   - fit
   - calc
   - matrix
   - decorations.pathreplacing
   - decorations.markings
4. Evitar errores:
   - La primera página del PDF no debe estar vacía. El contenido debe comenzar directamente en la primera página.
   - Asegúrate de que los diagramas largos se acomoden verticalmente y no se salgan de los márgenes.
5. Márgenes y formato:
   - Usa la clase `article` con márgenes ajustados mediante el paquete `geometry`.
   - Configura los diagramas para que ocupen una sola página en formato vertical si son largos.
6. Estilo claro:
   - Define los estilos de los nodos y las flechas explícitamente usando el comando `/.style`.
7. Compilación directa: El código debe ser compatible con `pdflatex` y no debe requerir configuraciones adicionales.
8. Recorda establecer distancia entre bloques SIEMPRE

Aquí tienes ejemplos que debes seguir:

    1. Diagrama de bloques sencillo:

        \documentclass[a4paper]{article}
        \usepackage[margin=1in]{geometry}
        \usepackage{tikz}
        \usetikzlibrary{shapes.geometric, arrows.meta, positioning}
        
        \begin{document}
        \begin{tikzpicture}[
          block/.style={draw, rectangle, minimum width=2.5cm, minimum height=1cm, align=center},
          arrow/.style={->, thick}
        ]
        
        \node[block] (A) {Inicio};
        \node[block, below=1.5cm of A] (B) {Proceso};
        \node[block, below=1.5cm of B] (C) {Fin};
        
        \draw[arrow] (A) -- (B);
        \draw[arrow] (B) -- (C);
        
        \end{tikzpicture}
        \end{document}

	2.	Diagrama extenso en formato vertical:
	
        \documentclass[a4paper]{article}
        \usepackage[margin=1in]{geometry}
        \usepackage{tikz}
        \usetikzlibrary{shapes.geometric, arrows.meta, positioning, fit}
        
        \begin{document}
        
        \begin{tikzpicture}[
          block/.style={draw, rectangle, minimum width=3cm, minimum height=1cm, align=center, fill=blue!20},
          arrow/.style={->, thick}
        ]
        
        \node[block] (A) {Inicio};
        \node[block, below=1.5cm of A] (B) {Paso 1};
        \node[block, below=1.5cm of B] (C) {Paso 2};
        \node[block, below=1.5cm of C] (D) {Paso 3};
        \node[block, below=1.5cm of D] (E) {Fin};
        
        \draw[arrow] (A) -- (B);
        \draw[arrow] (B) -- (C);
        \draw[arrow] (C) -- (D);
        \draw[arrow] (D) -- (E);
        
        \end{tikzpicture}
        
        \end{document}
    
    3. necesito un diagrama donde expliques el proceso industrial del papel:
    
        \documentclass[a4paper]{article}
        \usepackage[margin=1in]{geometry}
        \usepackage{tikz}
        \usetikzlibrary{shapes.geometric, arrows.meta, positioning, fit}
        
        \begin{document}
        
        \begin{tikzpicture}[
        block/.style={draw, rectangle, minimum width=3cm, minimum height=1cm, align=center, fill=blue!20},
        arrow/.style={->, thick},
        node distance=2.5cm and 1.5cm % Define distancias estándar entre nodos
        ]
        
        % Nodos
        \node[block] (A) {Madera};
        \node[block, right of=A] (B) {Trituración};
        \node[block, right of=B] (C) {Blandeo};
        \node[block, right of=C] (D) {Coagulación};
        \node[block, below=2cm of D] (E) {Prensa};
        \node[block, right of=E] (F) {Secado};
        \node[block, right of=F] (G) {Laminación};
        \node[block, right of=G] (H) {Papel};
        
        % Flechas
        \draw[arrow] (A) -- (B);
        \draw[arrow] (B) -- (C);
        \draw[arrow] (C) -- (D);
        \draw[arrow] (D) -- (E);
        \draw[arrow] (E) -- (F);
        \draw[arrow] (F) -- (G);
        \draw[arrow] (G) -- (H);
        
        \end{tikzpicture}
        
        \end{document}
        
    A continuacion te dejo ejemplos mal hechos para que tengas en cuenta que errores NO cometer:
    
    prompt: necesito que me muestres como derivar una función f(x) = 5x^2 + 6x + 1 
en un diagrama de bloques 

    respuesta (codigo mal hecho):
        \documentclass[a4paper]{article}
        \usepackage[margin=1in]{geometry}
        \usepackage{tikz}
        \usetikzlibrary{shapes.geometric, arrows.meta, positioning}
        
        \begin{document}
        \begin{tikzpicture}[
        block/.style={draw, rectangle, minimum width=3cm, minimum height=1cm, align=center},
        arrow/.style={->, thick}
        ]
        
        \node[block] (F) {f(x) = 5x^2 + 6x + 1};
        \node[block, below of=F] (G) {Regla de potencia};
        \node[block, right of=G] (H) {Derivada de x^n = n*x^(n-1)};
        \node[block, below of=H] (I) {Derivada del término 5x^2};
        \node[block, below of=I] (J) {10x};
        \node[block, right of=I] (K) {Derivada del término 6x};
        \node[block, below of=K] (L) {6};
        \node[block, right of=K] (M) {Derivada del término constante};
        \node[block, below of=M] (N) {0};
        
        \draw[arrow] (F) -- (G);
        \draw[arrow] (G) -- (H);
        \draw[arrow] (H) -- (I);
        \draw[arrow] (I) -- (J);
        \draw[arrow] (G) -- (K);
        \draw[arrow] (K) -- (L);
        \draw[arrow] (G) -- (M);
        \draw[arrow] (M) -- (N);
        
        \end{tikzpicture}
        \end{document}
    
    correccion (codigo bien hecho):
    
        \documentclass[a4paper]{article}
        \usepackage[margin=1in]{geometry}
        \usepackage{tikz}
        \usetikzlibrary{shapes.geometric, arrows.meta, positioning}
        
        \begin{document}
        
        \begin{tikzpicture}[
          block/.style={draw, rectangle, minimum width=3.5cm, minimum height=1cm, align=center, font=\small},
          arrow/.style={->, thick},
          node distance=1.5cm and 2.5cm % Distancia predeterminada entre nodos
        ]
        
        \node[block] (F) {f(x) = 5x^{2} + 6x + 1};
        \node[block, below of=F] (G) {Regla de potencia};
        \node[block, below of=G] (H) {Derivada: $x^{n} \rightarrow n \cdot x^{n-1}$};
        
        \node[block, below left=2cm and 2cm of H] (I) {Derivada de $5x^{2}$};
        \node[block, below=1.5cm of I] (J) {10x};
        
        \node[block, below=2cm of H] (K) {Derivada de $6x$};
        \node[block, below=1.5cm of K] (L) {6};
        
        \node[block, below right=2cm and 2cm of H] (M) {Derivada del término constante};
        \node[block, below=1.5cm of M] (N) {0};
        
        \draw[arrow] (F) -- (G);
        \draw[arrow] (G) -- (H);
        
        \draw[arrow] (H) -- (I);
        \draw[arrow] (I) -- (J);
        
        \draw[arrow] (H) -- (K);
        \draw[arrow] (K) -- (L);
        
        \draw[arrow] (H) -- (M);
        \draw[arrow] (M) -- (N);
        
        \end{tikzpicture}
        
        \end{document}
        
        
    otro ejemplo mal hecho:
    
    prompt: explicame la fotosintesis en un diagrama de 7 bloques 

    respuesta (codigo mal hecho):
        \documentclass[a4paper]{article}
        \usepackage{tikz}
        \usetikzlibrary{shapes,arrows,auto}
        
        \begin{document}
        \begin{tikzpicture}[
          block/.style={draw, rectangle, minimum width=3cm, minimum height=1.5cm, align=center, font=\small},
          arrow/.style={->, thick}
        ]
        \node[block] (1) {Luz solar};
        \node[block, below of=1] (2) { clorofila };
        \node[block, below of=2] (3) { Absorción de luz };
        \node[block, below of=3] (4) {  H₂O (agua) + CO₂ (dióxido de carbono)};
        \node[block, below of=4] (5) { Reacciones químicas };
        \node[block, below of=5] (6) { Glucosa (C₆H₁₂O₆) };
        \node[block, below of=6] (7) { Oxígeno (O₂) }; 
        
        \draw[arrow] (1) -- (2);
        \draw[arrow] (2) -- (3);
        \draw[arrow] (3) -- (4);
        \draw[arrow] (4) -- (5);
        \draw[arrow] (5) -- (6);
        \draw[arrow] (5) -- (7); 
        
        \end{tikzpicture}
        \end{document}
        
    correccion (codigo bien hecho):

        \documentclass[a4paper]{article}
        \usepackage{tikz}
        \usetikzlibrary{shapes,arrows,auto}
        
        \begin{document}
        \begin{tikzpicture}[
          block/.style={draw, rectangle, minimum width=3cm, minimum height=1.5cm, align=center, font=\small},
          arrow/.style={->, thick}
        ]
        \node[block] (luz_solar) {Luz solar};
        \node[block, below of=luz_solar] (clorofila) {Clorofila};
        \node[block, below of=clorofila] (absorcion) {Absorción de luz};
        \node[block, below of=absorcion] (agua_co2) {H₂O (agua) + CO₂ (dióxido de carbono)};
        \node[block, below of=agua_co2] (reacciones) {Reacciones químicas};
        \node[block, below of=reacciones] (glucosa) {Glucosa (C₆H₁₂O₆)};
        \node[block, below of=glucosa] (oxigeno) {Oxígeno (O₂)};
        
        \draw[arrow] (luz_solar) -- (clorofila);
        \draw[arrow] (clorofila) -- (absorcion);
        \draw[arrow] (absorcion) -- (agua_co2);
        \draw[arrow] (agua_co2) -- (reacciones);
        \draw[arrow] (reacciones) -- (glucosa);
        \draw[arrow] (reacciones) -- (oxigeno);
        
        \end{tikzpicture}
        \end{document}




    
    Responde solo con el código en formato compilable. Cada bloque debe estar ajustado verticalmente si el contenido es largo, y ningún diagrama debe salir 
    márgenes definidos.
    
    Ahora necesito que respondas unicamente con codigo latex, y siguiendo todas las reglas mencionadas.
    Este es el prompt que debes seguir:
    
    """

    prompt = text_input.get("1.0", tk.END).strip()  # Obtener el texto del input

    if not prompt:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un prompt.")
        return

    prompt = pre_prompt + prompt

        # Generar el código LaTeX usando Ollama
    messages = [{"role": "user", "content": prompt}]
    response = ollama.chat("gemma2", messages=messages)

    # print("####################################")
    # print(response.message.content)
    # print("####################################")

    latex_content = response.message.content

    # Envolver el contenido LaTeX con los encabezados necesarios
    # crear archivos output.tex y output.pdf

    os.system("touch output.tex")
    os.system("touch output.pdf")
    os.chmod("output.tex", 0o777)
    os.chmod("output.pdf", 0o777)

    latex_file = "output.tex"
    pdf_file = "output.pdf"

    with open(latex_file, "w") as f:
        f.write(latex_content)


    # Compilar el archivo LaTeX a PDF
    subprocess.run(["pdflatex", "-interaction=nonstopmode", latex_file], check=True)

    # Mostrar un mensaje de éxito y habilitar el botón de descarga
    messagebox.showinfo("Éxito", "El PDF se ha generado correctamente.")
    download_button.config(state=tk.NORMAL)
    download_button.config(command=lambda: descargar_pdf(pdf_file))

# Función para descargar el archivo PDF generado
def descargar_pdf(pdf_file):
    try:
        # Mostrar un diálogo para guardar el archivo PDF
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            initialfile=pdf_file
        )
        if save_path:
            # Mover el archivo PDF a la ubicación seleccionada
            os.replace(pdf_file, save_path)
            messagebox.showinfo("Descarga", f"PDF guardado en: {save_path}")
        else:
            messagebox.showinfo("Cancelado", "No se guardó el archivo.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")


# Configuración de la ventana principal de Tkinter
root = tk.Tk()
root.title("diagramToLatexAI")  # Título de la ventana
root.geometry("500x400")  # Tamaño de la ventana

# Etiqueta
label = tk.Label(root, text="Ingresa tu prompt para generar el código LaTeX", font=("Arial", 14))
label.pack(pady=10)

# Caja de texto para ingresar el prompt
text_input = tk.Text(root, height=5, width=50)
text_input.pack(pady=10)

# Botón para generar el PDF
generate_button = tk.Button(root, text="Generar PDF", font=("Arial", 12), command=generar_pdf)
generate_button.pack(pady=20)

# Botón para descargar el PDF (inicialmente deshabilitado)
download_button = tk.Button(root, text="Descargar PDF", font=("Arial", 12), state=tk.DISABLED)
download_button.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()