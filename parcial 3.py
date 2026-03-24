import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import threading
import sqlite3

# ---------------- CONFIGURACIÓN DE VOZ ---------------- #
try:
    import pyttsx3
    AUDIO_DISPONIBLE = True
except ImportError:
    AUDIO_DISPONIBLE = False

# ---------------- BASE DE DATOS Y SESIÓN ---------------- #
USUARIO_ACTUAL = None

def init_db():
    conn = sqlite3.connect("progreso_meses.db")
    cursor = conn.cursor()
    # Tabla con columnas para récords de los dos juegos
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario TEXT UNIQUE,
                        contrasena TEXT,
                        record_test INTEGER DEFAULT 0,
                        record_ordenar INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def actualizar_record(tipo_juego, nuevo_puntaje):
    global USUARIO_ACTUAL
    if not USUARIO_ACTUAL: return
    
    conn = sqlite3.connect("progreso_meses.db")
    cursor = conn.cursor()
    
    columna = "record_test" if tipo_juego == "test" else "record_ordenar"
    
    # Solo actualizamos si el nuevo puntaje es mayor al guardado
    cursor.execute(f"SELECT {columna} FROM usuarios WHERE usuario=?", (USUARIO_ACTUAL,))
    resultado = cursor.fetchone()
    actual = resultado[0] if resultado else 0
    
    if nuevo_puntaje > actual:
        cursor.execute(f"UPDATE usuarios SET {columna}=? WHERE usuario=?", (nuevo_puntaje, USUARIO_ACTUAL))
        conn.commit()
        retorno = True
    else:
        retorno = False
    
    conn.close()
    return retorno

# ---------------- ESTILOS ---------------- #
COLOR_FONDO = "#FFF9E3"
COLOR_BOTON_MENU = "#FFD166"
COLOR_BOTON_ACCION = "#06D6A0"
COLOR_BOTON_VOLVER = "#EF476F"
COLOR_BOTON_AUDIO = "#118AB2"
COLOR_TEXTO = "#444444"

FUENTE_TITULO = ("Comic Sans MS", 28, "bold")
FUENTE_NORMAL = ("Comic Sans MS", 18, "bold")
FUENTE_DATOS = ("Comic Sans MS", 14, "bold")
FUENTE_BOTON_GRANDE = ("Comic Sans MS", 16, "bold") # <-- ¡Aquí está la que faltaba!

# ---------------- VENTANA Y LOGICA ---------------- #
root = tk.Tk()
root.title("Aventuras con los Meses")
root.geometry("1200x900")
root.config(bg=COLOR_FONDO)

frames = {}

def mostrar_frame(nombre):
    if nombre == "menu": actualizar_labels_menu() 
    for f in frames.values(): f.pack_forget()
    if nombre in frames:
        frames[nombre].pack(fill="both", expand=True)

def reproducir_audio(texto):
    if not AUDIO_DISPONIBLE: return
    def hablar():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(texto)
            engine.runAndWait()
        except: pass
    threading.Thread(target=hablar, daemon=True).start()

# ---------------- PANTALLAS DE ACCESO ---------------- #
def crear_login():
    f = tk.Frame(root, bg=COLOR_FONDO); frames["login"] = f
    tk.Label(f, text="🚀 ¡Bienvenido!", font=FUENTE_TITULO, bg=COLOR_FONDO).pack(pady=40)
    
    tk.Label(f, text="Tu Nombre:", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack()
    e_u = tk.Entry(f, font=FUENTE_NORMAL, justify="center"); e_u.pack(pady=10)
    
    tk.Label(f, text="Tu Clave:", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack()
    e_p = tk.Entry(f, font=FUENTE_NORMAL, show="*", justify="center"); e_p.pack(pady=10)

    def login():
        global USUARIO_ACTUAL
        conn = sqlite3.connect("progreso_meses.db")
        c = conn.cursor()
        c.execute("SELECT usuario FROM usuarios WHERE usuario=? AND contrasena=?", (e_u.get(), e_p.get()))
        res = c.fetchone()
        if res:
            USUARIO_ACTUAL = res[0]
            mostrar_frame("menu")
        else:
            messagebox.showerror("Oops", "Usuario o clave no encontrados")
        conn.close()

    tk.Button(f, text="¡Entrar a Jugar!", font=FUENTE_NORMAL, bg=COLOR_BOTON_ACCION, fg="white", command=login, width=15).pack(pady=20)
    tk.Button(f, text="Registrarse", font=("Comic Sans MS", 12), bg=COLOR_BOTON_MENU, command=lambda: mostrar_frame("registro")).pack()

def crear_registro():
    f = tk.Frame(root, bg=COLOR_FONDO); frames["registro"] = f
    tk.Label(f, text="📝 Crea tu Perfil", font=FUENTE_TITULO, bg=COLOR_FONDO).pack(pady=40)
    
    tk.Label(f, text="Elige un Nombre:", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack()
    e_u = tk.Entry(f, font=FUENTE_NORMAL, justify="center"); e_u.pack(pady=10)
    
    tk.Label(f, text="Crea una Clave:", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack()
    e_p = tk.Entry(f, font=FUENTE_NORMAL, show="*", justify="center"); e_p.pack(pady=10)

    def registrar():
        u, p = e_u.get(), e_p.get()
        if not u or not p: 
            messagebox.showwarning("Atención", "Rellena todos los campos")
            return
        try:
            conn = sqlite3.connect("progreso_meses.db")
            c = conn.cursor()
            c.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (u, p))
            conn.commit()
            conn.close()
            messagebox.showinfo("¡Bien!", "¡Cuenta creada! Ya puedes entrar.")
            mostrar_frame("login")
        except:
            messagebox.showerror("Error", "Ese nombre ya está en uso.")

    tk.Button(f, text="Guardar Perfil", font=FUENTE_NORMAL, bg=COLOR_BOTON_ACCION, fg="white", command=registrar, width=15).pack(pady=20)
    tk.Button(f, text="Volver", font=("Comic Sans MS", 12), command=lambda: mostrar_frame("login")).pack()

# ---------------- MENÚ CON RÉCORDS ---------------- #
lbl_records = None

def actualizar_labels_menu():
    global lbl_records, USUARIO_ACTUAL
    if not USUARIO_ACTUAL: return
    conn = sqlite3.connect("progreso_meses.db")
    c = conn.cursor()
    c.execute("SELECT record_test, record_ordenar FROM usuarios WHERE usuario=?", (USUARIO_ACTUAL,))
    resultado = c.fetchone()
    if resultado:
        r_test, r_ord = resultado
        lbl_records.config(text=f"👤 Jugador: {USUARIO_ACTUAL}\n🏆 Mejor Test: {r_test}/10 | 🧩 Mejor Orden: {r_ord}/12")
    conn.close()

def crear_menu():
    global lbl_records
    f = tk.Frame(root, bg=COLOR_FONDO); frames["menu"] = f
    
    tk.Label(f, text="📅 Aprende los Meses", font=FUENTE_TITULO, bg=COLOR_FONDO).pack(pady=20)
    
    perfil_box = tk.LabelFrame(f, text=" Mi Progreso ", font=FUENTE_DATOS, bg="white", padx=20, pady=10)
    perfil_box.pack(pady=10)
    lbl_records = tk.Label(perfil_box, text="", font=FUENTE_DATOS, bg="white", fg="#555")
    lbl_records.pack()

    tk.Button(f, text="📖 Aprender", font=FUENTE_NORMAL, bg=COLOR_BOTON_MENU, width=20, 
              command=lambda: mostrar_frame("aprender")).pack(pady=10)
    tk.Button(f, text="❓ Test de Imágenes", font=FUENTE_NORMAL, bg=COLOR_BOTON_MENU, width=20, 
              command=empezar_test).pack(pady=10)
    tk.Button(f, text="🧩 Ordenar el Año", font=FUENTE_NORMAL, bg=COLOR_BOTON_MENU, width=20, 
              command=lambda: mostrar_frame("ordenar")).pack(pady=10)
    
    tk.Button(f, text="🚪 Cerrar Sesión", font=("Comic Sans MS", 12), bg=COLOR_BOTON_VOLVER, fg="white", 
              command=lambda: mostrar_frame("login")).pack(pady=20)

# ---------------- LÓGICA DE JUEGOS ---------------- #
MESES_LISTA = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def empezar_test():
    f = frames["test"] = tk.Frame(root, bg=COLOR_FONDO)
    st = {"n": 0, "p": 0, "cor": ""}
    
    lbl_q = tk.Label(f, text="", font=FUENTE_NORMAL, bg=COLOR_FONDO); lbl_q.pack(pady=10)
    img_l = tk.Label(f, bg=COLOR_FONDO); img_l.pack(pady=10)
    btn_container = tk.Frame(f, bg=COLOR_FONDO); btn_container.pack(pady=10)

    def sig():
        if st["n"] == 10:
            subio = actualizar_record("test", st["p"])
            msg = f"¡Terminaste!\nPuntaje: {st['p']}/10"
            if subio: msg += "\n¡NUEVO RÉCORD! 🏆"
            messagebox.showinfo("Fin del Juego", msg)
            mostrar_frame("menu"); return
        
        st["n"] += 1; lbl_q.config(text=f"Pregunta {st['n']} de 10")
        st["cor"] = random.choice(MESES_LISTA)
        
        path = f"imagenes/{st['cor']}.png"
        if os.path.exists(path):
            img = ImageTk.PhotoImage(Image.open(path).resize((250, 250)))
            img_l.config(image=img); img_l.image = img
        else:
            img_l.config(image='', text=f"Imagen: {st['cor']}")
        
        [w.destroy() for w in btn_container.winfo_children()]
        ops = random.sample(MESES_LISTA, 3)
        if st["cor"] not in ops: ops[0] = st["cor"]
        random.shuffle(ops)
        
        for o in ops:
            tk.Button(btn_container, text=o.capitalize(), font=FUENTE_NORMAL, bg=COLOR_BOTON_MENU, width=12,
                      command=lambda x=o: validar(x)).pack(side="left", padx=10)

    def validar(r):
        if r == st["cor"]: st["p"] += 1; reproducir_audio("¡Correcto!")
        else: reproducir_audio(f"Era {st['cor']}")
        sig()

    sig(); mostrar_frame("test")

def crear_aprender():
    f = tk.Frame(root, bg=COLOR_FONDO); frames["aprender"] = f
    tk.Label(f, text="Presiona un mes", font=FUENTE_NORMAL, bg=COLOR_FONDO).pack(pady=20)
    cont = tk.Frame(f, bg=COLOR_FONDO); cont.pack()
    for i, m in enumerate(MESES_LISTA):
        tk.Button(cont, text=m.capitalize(), font=("Comic Sans MS", 12), width=10, height=2,
                  command=lambda x=m: detalle(x)).grid(row=i//4, column=i%4, padx=5, pady=5)
    tk.Button(f, text="🏠 Volver", bg=COLOR_BOTON_VOLVER, fg="white", command=lambda: mostrar_frame("menu")).pack(pady=30)

def detalle(m):
    reproducir_audio(m)
    f = frames["detalle"] = tk.Frame(root, bg=COLOR_FONDO)
    tk.Label(f, text=m.capitalize(), font=FUENTE_TITULO, bg=COLOR_FONDO).pack(pady=20)
    path = f"imagenes/{m}.png"
    if os.path.exists(path):
        img = ImageTk.PhotoImage(Image.open(path).resize((350, 350)))
        l = tk.Label(f, image=img, bg=COLOR_FONDO); l.image = img; l.pack()
    tk.Button(f, text="🔊 Escuchar", font=FUENTE_NORMAL, bg=COLOR_BOTON_AUDIO, fg="white", command=lambda: reproducir_audio(m)).pack(pady=10)
    tk.Button(f, text="⬅ Atrás", font=FUENTE_NORMAL, bg=COLOR_BOTON_VOLVER, fg="white", command=lambda: mostrar_frame("aprender")).pack(pady=10)
    mostrar_frame("detalle")

# ---------------- JUEGO ORDENAR ---------------- #
def crear_ordenar():
    f = tk.Frame(root, bg=COLOR_FONDO); frames["ordenar"] = f
    cv = tk.Canvas(f, width=1100, height=580, bg="white", bd=2, relief="sunken"); cv.pack(pady=10)
    cajas = []
    for i in range(12):
        x, y = (550 + (0 if i<6 else 1)*280), (i if i<6 else i-6)*85 + 25
        rid = cv.create_rectangle(x, y, x+220, y+65, fill="#F9F9F9", outline="#CCC")
        cv.create_text(x-30, y+45, text=f"{i+1}º", font=FUENTE_DATOS)
        cajas.append({"coords": (x, y, x+220, y+65), "mes": MESES_LISTA[i], "id": rid, "o": None})
    
    m_shuf = MESES_LISTA.copy(); random.shuffle(m_shuf)
    items = {}
    for i, m in enumerate(m_shuf):
        mx, my = 120 + (0 if i<6 else 1)*180, (i if i<6 else i-6)*85 + 50
        r = cv.create_rectangle(mx-75, my-25, mx+75, my+25, fill=COLOR_BOTON_ACCION, tags="drag")
        t = cv.create_text(mx, my, text=m.capitalize(), fill="white", font=FUENTE_BOTON_GRANDE, tags="drag")
        items[r] = {"t": t, "m": m, "ox": mx, "oy": my}

    drag = {"i": None, "x": 0, "y": 0}
    def _start(e):
        it_ids = cv.find_closest(e.x, e.y)
        if it_ids:
            it = it_ids[0]
            if "drag" in cv.gettags(it):
                if cv.type(it) == "text": it -= 1
                drag.update({"i": it, "x": e.x, "y": e.y})
                cv.tag_raise(it); cv.tag_raise(items[it]["t"])
                reproducir_audio(items[it]["m"])

    def _do(e):
        if drag["i"]:
            dx, dy = e.x-drag["x"], e.y-drag["y"]
            cv.move(drag["i"], dx, dy); cv.move(items[drag["i"]]["t"], dx, dy)
            drag["x"], drag["y"] = e.x, e.y

    def _stop(e):
        if not drag["i"]: return
        it, f = drag["i"], False
        for c in cajas:
            if c["o"] == items[it]["m"]: c["o"] = None
            if c["coords"][0] < e.x < c["coords"][2] and c["coords"][1] < e.y < c["coords"][3]:
                cx, cy = (c["coords"][0]+c["coords"][2])/2, (c["coords"][1]+c["coords"][3])/2
                cv.coords(it, cx-75, cy-25, cx+75, cy+25); cv.coords(items[it]["t"], cx, cy)
                c["o"] = items[it]["m"]; f = True; break
        if not f:
            cv.coords(it, items[it]["ox"]-75, items[it]["oy"]-25, items[it]["ox"]+75, items[it]["oy"]+25)
            cv.coords(items[it]["t"], items[it]["ox"], items[it]["oy"])
        drag["i"] = None

    cv.bind("<ButtonPress-1>", _start); cv.bind("<B1-Motion>", _do); cv.bind("<ButtonRelease-1>", _stop)
    
    b_f = tk.Frame(f, bg=COLOR_FONDO); b_f.pack()
    tk.Button(b_f, text="✅ Revisar", font=FUENTE_NORMAL, bg=COLOR_BOTON_ACCION, fg="white", 
              command=lambda: val_ord(cajas, cv)).pack(side="left", padx=20)
    tk.Button(b_f, text="🏠 Menú", font=FUENTE_NORMAL, bg=COLOR_BOTON_VOLVER, fg="white", 
              command=lambda: mostrar_frame("menu")).pack(side="left")

def val_ord(cajas, cv):
    p = 0
    for c in cajas:
        if c["o"] == c["mes"]: p += 1; cv.itemconfig(c["id"], outline="#06D6A0", width=4)
        else: cv.itemconfig(c["id"], outline="#EF476F", width=4)
    subio = actualizar_record("ordenar", p)
    msg = f"Meses correctos: {p}/12"
    if subio: msg += "\n¡NUEVO RÉCORD PERSONAL! 🏆"
    messagebox.showinfo("Resultado", msg)

# ---------------- INICIO ---------------- #
init_db()
crear_login(); crear_registro(); crear_menu(); crear_aprender(); crear_ordenar()
mostrar_frame("login")
root.mainloop()