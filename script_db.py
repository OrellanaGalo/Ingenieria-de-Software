import sqlite3
import chardet
import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

# Crear la base de datos y la tabla.
def crearBaseDatos():
	db_ruta = os.path.join(os.getcwd(), 'personal.db')

	os.makedirs(os.path.dirname(db_ruta), exist_ok=True)

	conn = sqlite3.connect(db_ruta)
	cursor = conn.cursor()

	cursor.execute('''
	CREATE TABLE IF NOT EXISTS personal (
		dni TEXT PRIMARY KEY,
		nombre TEXT,
		apellido TEXT,
		fecha_nac TEXT,
		sexo TEXT,
		direccion TEXT
	)
	''')
	conn.commit()
	conn.close()

def detectarCodificacion(filepath):
	with open(filepath, 'rb') as file:
		rawdata = file.read()
		result = chardet.detect(rawdata)
		return result['encoding']

# Importar datos desde un archivo CSV a la base de datos.
def importarDatos():
	# Seleccionar archivo CSV
	filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
	if not filepath:
		return
	
	encoding = detectarCodificacion(filepath)

	try:
		# Leer archivo CSV
		with open(filepath, newline='', encoding=encoding) as csvfile:
			try:
				sniffer = csv.Sniffer()
				sample = csvfile.read(1024)
				csvfile.seek(0)
				dialect = sniffer.sniff(sample)
				reader = csv.DictReader(csvfile, dialect=dialect)
			except csv.Error:
				# Si no se puede detectar, usa uno por defecto.
				csvfile.seek(0)
				reader = csv.DictReader(csvfile, delimiter=';')

			# Validar columnas requeridas.
			if not {'documento', 'nombre1', 'nombre2', 'apellido', 'fecha_nac', 'sexo', 'direccion'}.issubset(reader.fieldnames):
				raise ValueError("El archivo CSV no contiene las columnas requeridas.")

			# Omitir lineas vacias.
			reader = filter(lambda row: any(row.values()), reader)

			# Conectar a la base de datos
			conn = sqlite3.connect('personal.db')
			cursor = conn.cursor()

			for row in reader:
				
				cursor.execute('''
				INSERT OR IGNORE INTO personal (dni, nombre, apellido, fecha_nac, sexo, direccion)
				VALUES (?, ?, ?, ?, ?, ?)
				''', (
					row['documento'],  # Columna del número de documento
					row['nombre1'] + ' ' + (row['nombre2'] if row['nombre2'] else ''),  # Concatenar nombre1 y nombre2
					row['apellido'],
					row['fecha_nac'],
					row['sexo'],
					row['direccion']
				))

			conn.commit()
			conn.close()
			messagebox.showinfo("Importación completada", "Los datos se han importado correctamente.")
	except Exception as e:
		messagebox.showerror("Error", str(e))

# Consultar datos usando la clave DNI.
def consultarDatos():
	def mostrarDatos():
		dni = dni_entry.get()
		conn = sqlite3.connect('personal.db')
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM personal WHERE dni = ?", (dni,))
		record = cursor.fetchone()
		conn.close()
		if record:
			result_label.config(text=f"DNI: {record[0]}\nNombre: {record[1]}\nApellido: {record[2]}\nFecha de Nacimiento: {record[3]}\nSexo: {record[4]}\nDireccion: {record[5]}")
		else:
			result_label.config(text="No se encontraron datos para ese DNI")

	for widget in main_frame.winfo_children():
		widget.destroy()

	# Agregar los campos y botones para consulta
	tk.Label(main_frame, text="Consultar Datos", font=("Arial", 14, "bold")).pack(pady=10)

	tk.Label(main_frame, text="Ingrese DNI:").pack(pady=5)
	dni_entry = tk.Entry(main_frame)
	dni_entry.pack(pady=5)

	consultar_button = tk.Button(main_frame, text="Consultar", command=mostrarDatos)
	consultar_button.pack(pady=5)

	result_label = tk.Label(main_frame, text="")
	result_label.pack(pady=10)

	volver_button = tk.Button(main_frame, text="Volver atras", command=iniciarVentanaPrincipal)
	volver_button.pack(pady=10)

# Exportar datos de la base de datos a un archivo CSV.
def exportarDatos():
	conn = sqlite3.connect('personal.db')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM personal")
	records = cursor.fetchall()
	conn.close()

	ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
	if not ruta:
		return

	with open(ruta, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(['dni', 'nombre', 'apellido', 'fecha_nac', 'sexo', 'direccion'])
		writer.writerows(records)

	messagebox.showinfo("Exportacion", "Datos exportados correctamente")

def visualizarDatos():
	conn = sqlite3.connect('personal.db')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM personal")
	records = cursor.fetchall()
	conn.close()

	tk.Label(main_frame, text="Datos Almacenados", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=10)

	# Limpiar la ventana actual
	for widget in main_frame.winfo_children():
		widget.destroy()

	# Crear una lista para mostrar los registros
	listbox = tk.Listbox(main_frame, width=121, height=25)
	listbox.grid(row=0, column=0, padx=10, pady=5)

	# Agregar registros a la lista
	for record in records:
		listbox.insert(tk.END, f"DNI: {record[0]}, Nombre: {record[1]}, Apellido: {record[2]}, "
                               f"Fecha Nac: {record[3]}, Sexo: {record[4]}, Dirección: {record[5]}")
	
	# Boton para cerrar la ventana.
	volver_button = tk.Button(main_frame, text="Volver atras", command=iniciarVentanaPrincipal)
	volver_button.grid(row=1, column=0, pady=0)

# Volver a la pantalla principal
def iniciarVentanaPrincipal():
    # Limpiar la ventana actual
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Título
    tk.Label(main_frame, text="Gestión de Base de Datos Personal", 
             bg=frame_color, font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=10)

    # Botones de funciones
    tk.Button(main_frame, text="Crear BD", command=crearBaseDatos, bg=button_color, fg=button_text_color, font=("Arial", 10, "bold"), width=15).grid(row=1, column=0, padx=10)
    tk.Button(main_frame, text="Importar Datos", command=importarDatos, bg=button_color, fg=button_text_color, font=("Arial", 10, "bold"), width=15).grid(row=1, column=1, padx=10)
    tk.Button(main_frame, text="Consultar Datos", command=consultarDatos, bg=button_color, fg=button_text_color, font=("Arial", 10, "bold"), width=15).grid(row=1, column=2, padx=10)
    tk.Button(main_frame, text="Exportar Datos", command=exportarDatos, bg=button_color, fg=button_text_color, font=("Arial", 10, "bold"), width=15).grid(row=1, column=3, padx=10)
    tk.Button(main_frame, text="Visualizar Datos", command=visualizarDatos, bg=button_color, fg=button_text_color, font=("Arial", 10, "bold"), width=15).grid(row=1, column=4, padx=10)

# Ventana principal.
root = tk.Tk()
root.title("Gestion de base de datos personal")
root.geometry("850x500")
root.resizable(False, False)

# Colores y estilos
bg_color = "#f0f4f7"  # Fondo claro
button_color = "#4CAF50"  # Verde para botones
button_text_color = "#000000"
frame_color = "#d9e8f5"

root.configure(bg=bg_color)

# Crear marco principal
main_frame = tk.Frame(root, bg=frame_color, bd=2, relief="solid")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=760, height=450)

# Iniciar la ventana principal.
iniciarVentanaPrincipal()

# Iniciar la aplicación
root.mainloop()
