import sqlite3
import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

# Crear la base de datos y la tabla.
def crearBaseDatos():
	db_ruta = '/home/ubuntu/Desktop/universidad/ingenieria_de_software/personal.db'

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

# Importar datos desde un archivo CSV a la base de datos.
def importarDatos():
	# Seleccionar archivo CSV
	filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
	if not filepath:
		return

	# Conectar a la base de datos
	conn = sqlite3.connect('personal.db')
	cursor = conn.cursor()

	# Leer archivo CSV
	with open(filepath, newline='', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile)
		print("Columnas disponibles:", reader.fieldnames)  # Mostrar nombres de columnas

	for row in reader:
		try:
			cursor.execute('''
			INSERT INTO personal (dni, nombre, apellido, fecha_nac, sexo, direccion)
			VALUES (?, ?, ?, ?, ?, ?)
			''', (
				row['documento'],  # Columna del número de documento
				row['nombre1'] + ' ' + (row['nombre2'] if row['nombre2'] else ''),  # Concatenar nombre1 y nombre2
				row['apellido'],
				row['fecha_nac'],
				row['sexo'],
				row['direccion']
			))
		except KeyError as e:
			messagebox.showerror("Error", f"Clave faltante en la fila: {e}")
			break

	conn.commit()
	conn.close()
	messagebox.showinfo("Importación completada", "Los datos se han importado correctamente.")


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

	consulta_window = tl.Toplevel()
	consulta_window.title("Consultar Datos")

	tk.Label(consulta_window, text="Ingrese DNI:").pack(pady=5)
	dni_entry = tk.Entry(consulta_window)
	dni_entry.pack(pady=5)

	consultar_button = tk.Button(consulta_window, text="Consultar", command=mostrarDatos)
	consultar_button.pack(pady=5)

	result_label = tk.Label(consulta_window, text="")
	result_label.pack(pady=10)

# Exportar datos de la base de datos a un archivo CSV.
def exportarDatos():
	conn = sqlite3.connect('personal.db')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM personal")
	records = cursor.fetchall()
	conn.close()

	ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
	if not ruta:
		return

	with open(ruta, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(['dni', 'nombre', 'apellido', 'fecha_nac', 'sexo', 'direccion'])
		writer.writerows(records)

	messagebox.showinfo("Exportacion", "Datos exportados correctamente")

# Ventana principal.
root = tk.Tk()
root.title("Gestion de base de datos personal")

# Botones para las funciones.
crear_db_button = tk.Button(root, text="Crear base de datos", command=crearBaseDatos)
crear_db_button.pack(pady=10)

importar_button = tk.Button(root, text="Importar datos", command=importarDatos)
importar_button.pack(pady=10)

consultar_button = tk.Button(root, text="Consultar datos", command=consultarDatos)
consultar_button.pack(pady=10)

exportar_button = tk.Button(root, text="Exportar datos", command=exportarDatos)
exportar_button.pack(pady=10)

# Iniciar la aplicacion.
root.mainloop()
