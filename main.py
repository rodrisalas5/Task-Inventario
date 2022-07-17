import sqlite3
import os
from peewee import *


def cls():
    os.system('cls')

db = SqliteDatabase('productos.db')

# Creo base de datos
class Articulos(Model):
    codigo = TextField(primary_key = True, unique = True)
    tipo = TextField()
    modelo = TextField()
    color = TextField()
    cantidad = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([Articulos])

def verificar_PK(cod_a_verificar):
    rows = Articulos.select().order_by(Articulos.codigo.asc())
    for row in rows:
        if row.codigo == cod_a_verificar:
            print("\nERROR, codigo ya existente")
            return False

def mostrar_PK():
    rows = Articulos.select().order_by(Articulos.codigo.asc())
    for row in rows:
        print(row)

def obtener_stock(codigo_a_buscar):
    rows = Articulos.select().order_by(Articulos.codigo.asc())
    for row in rows:
        row_cod = str(row)
        if row_cod == codigo_a_buscar:
            return row.cantidad

def obtener_stock_por_codigo():
    while True:
        codigo = input("\nIngrese el codigo: ")
        if len(codigo) == 3:
            codigo_a_buscar = codigo[0]+"-"+codigo[1]+"-"+codigo[2]
            break
        else:
            print("Reintentar, recuerde que el codigo es de 3 digitos")
    rows = Articulos.select().order_by(Articulos.codigo.asc())
    for row in rows:
        row_cod = str(row)
        if row_cod == codigo_a_buscar:
            print(f"\nCodigo: {row.codigo} === Cantidad: {row.cantidad}")
            return
    print("Codigo no registrado en el sistema")

def crear_producto(tipos_dict):
    x = 1
    cls()
    print("--------Crear producto--------")
    for i in tipos_dict.keys():
        print("\t",x," ",i)
        x = x + 1
    tipo_num = int(input("Tipo: "))-1
    tipo = list(tipos_dict.keys())[tipo_num]

    modelo_dict = list(tipos_dict.values())[tipo_num]
    
    x = 1
    cls()
    for i in modelo_dict.keys():
        print("\t",x," ",i)
        x = x + 1
    modelo_num = int(input("Modelo: "))-1
    modelo = list(modelo_dict.keys())[modelo_num]

    color_list = modelo_dict[modelo]
    
    x = 1
    cls()
    for i in color_list:
        print("\t",x," ",i)
        x = x + 1
    color_num = int(input("Color: "))-1
    color = color_list[color_num]

    cod_a_verificar = "{}-{}-{}".format(tipo_num,modelo_num,color_num)

    if verificar_PK(cod_a_verificar) == False:
        return 
    else:
        info = ["{}-{}-{}".format(tipo_num,modelo_num,color_num), tipo, modelo, color]
        data = Articulos(codigo = info[0], tipo = info[1], modelo = info[2], color = info[3], cantidad = 0)
        data.save(force_insert = True)
        print("\nProducto agregado al sistema exitosamente!!!")
        return

def obtener_diccionarios():
    con = sqlite3.connect("tipos.db")
    cur = con.cursor()
    
    tablas = []
    for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
        tablas.append(row[0])
    
    tipos = {}
    for tabla in tablas:
        tipo = {}
        cur.execute("SELECT * FROM {}".format(tabla))
        for key in cur.description[1:]:
            values = []
            for value in cur.execute("SELECT {} FROM {};".format(key[0],tabla)):
                if value[0]=="":
                    pass
                else:
                    values.append(value[0])
            tipo[key[0]] = values
        tipos[tabla] = tipo
    cur.close()
    con.close()
    return tipos

# crear_producto(obtener_diccionarios())

def mostrar_por_tipo():
    while True:
        opcion = input("""
        1. Alacena
        2. Mesa
        3. Cajonera
        4. Silla
        Opcion: """)
        if opcion == "1":
            rows = Articulos.select().order_by(Articulos.codigo.asc())
            print("\n\tAlacenas: \n")
            for row in rows:
                primer_digito = str(row)
                if primer_digito[0] == "0":
                    print(f"Codigo: {row.codigo} === Tipo: {row.tipo} === Modelo: {row.modelo} === Color: {row.color} === Cantidad: {row.cantidad}")            
                    return
        elif opcion == "2":
            rows = Articulos.select().order_by(Articulos.codigo.asc())
            print("\n\tMesas: \n")
            for row in rows:
                primer_digito = str(row)
                if primer_digito[0] == "1":
                    print(f"Codigo: {row.codigo} === Tipo: {row.tipo} === Modelo: {row.modelo} === Color: {row.color} === Cantidad: {row.cantidad}")            
                    return
        elif opcion == "3":
            rows = Articulos.select().order_by(Articulos.codigo.asc())
            print("\n\tCajoneras: \n")
            for row in rows:
                primer_digito = str(row)
                if primer_digito[0] == "2":
                    print(f"Codigo: {row.codigo} === Tipo: {row.tipo} === Modelo: {row.modelo} === Color: {row.color} === Cantidad: {row.cantidad}")            
                    return
        elif opcion == "4":
            rows = Articulos.select().order_by(Articulos.codigo.asc())
            print("\n\tSillas: \n")
            for row in rows:
                primer_digito = str(row)
                if primer_digito[0] == "3":
                    print(f"Codigo: {row.codigo} === Tipo: {row.tipo} === Modelo: {row.modelo} === Color: {row.color} === Cantidad: {row.cantidad}")            
                    return
        else:
            print("Opcion incorrecta, reintentar.")

def mostrar_por_codigo():
    while True:
        codigo = input("\nIngrese el codigo: ")
        if len(codigo) == 3:
            codigo_a_buscar = codigo[0]+"-"+codigo[1]+"-"+codigo[2]
            break
        else:
            print("Reintentar, recuerde que el codigo es de 3 digitos")
    rows = Articulos.select().order_by(Articulos.codigo.asc())
    for row in rows:
        row_cod = str(row)
        if row_cod == codigo_a_buscar:
            print(f"\nCodigo: {row.codigo} === Tipo: {row.tipo} === Modelo: {row.modelo} === Color: {row.color} === Cantidad: {row.cantidad}")
            return
    print("Codigo no registrado en el sistema")

def modificar_stock():
    while True:
        opcion = input("""
        1. Agregar cantidad de articulo
        2. Restar cantidad de articulo
        Opcion: """)
        if opcion == "1" or opcion == "2":
            break
        else:
            print("Opcion incorrecta, reintentar")
    while True:
        codigo = input("\nIngrese el codigo: ")
        if len(codigo) == 3:
            codigo_a_buscar = codigo[0]+"-"+codigo[1]+"-"+codigo[2]
            break
        else:
            print("Reintentar, recuerde que el codigo es de 3 digitos")
    rows = Articulos.select().order_by(Articulos.codigo.asc())
    flag = 0
    for row in rows:
        row_cod = str(row)
        if row_cod == codigo_a_buscar:
            flag += 1
        else:
            flag += 0
    if flag == 0:
        print("El articulo no existe")
        return
    elif opcion == "1":
        while True:
            try:
                stock_a_agregar = int(input("Ingrese la cantidad a agregar: "))
                if stock_a_agregar > 0:
                    query = Articulos.select(Articulos.cantidad).where(Articulos.codigo == codigo_a_buscar)
                    for articulo in query:
                        stock = articulo.cantidad + stock_a_agregar
                    Articulos.update(cantidad=stock).where(Articulos.codigo == codigo_a_buscar).execute()
                    break
                else:
                    print("Error, el valor a ingresar debe ser mayor a 0")
            except:
                print("Valor invalido, recuerde que el stock es numerico")
    elif opcion == "2":
        while True:
            try:
                if obtener_stock(codigo_a_buscar) == 0:
                    print("El stock es cero, no puede restar unidades al stock")
                    return
                else:
                    stock_a_restar = int(input("Ingrese la cantidad a restar: "))
                    if stock_a_restar > 0 and obtener_stock(codigo_a_buscar) >= stock_a_restar:
                        query = Articulos.select(Articulos.cantidad).where(Articulos.codigo == codigo_a_buscar)
                        for articulo in query:
                            stock = articulo.cantidad - stock_a_restar
                        Articulos.update(cantidad=stock).where(Articulos.codigo == codigo_a_buscar).execute()
                        break
                    else:
                        print("Error, el valor a ingresar debe ser mayor a 0 y menor o igual a la cantidad actual de stock")
            except:
                print("Valor invalido, recuerde que el stock es numerico")
    print("\nStock modificado con exito!!!")

def borrar_articulo():
    while True:
        codigo = input("\nIngrese el codigo del producto a eliminar: ")
        if len(codigo) == 3:
            codigo_a_buscar = codigo[0]+"-"+codigo[1]+"-"+codigo[2]
            break
        else:
            print("Reintentar, recuerde que el codigo es de 3 digitos")
    rows = Articulos.select().order_by(Articulos.codigo.asc())
    flag = 0
    for row in rows:
        row_cod = str(row)
        if row_cod == codigo_a_buscar:
            flag += 1
        else:
            flag += 0
    if flag == 0:
        print("El articulo no existe")
        return
    Articulos.delete().where(Articulos.codigo == codigo_a_buscar).execute()
    print("\nArticulo borrado del sistema con exito!!!")

def menu():
    while True:
        opcion = input("""\nIngrese una opcion
        1. Agregar articulo
        2. Modificar stock
        3. Eliminar articulo
        4. Mostrar articulos por codigo
        5. Mostrar articulos por tipo
        6. Obtener stock de un producto
        7. Salir
        Opcion: """)
        if opcion == "1":
            crear_producto(obtener_diccionarios())
        elif opcion == "2":
            modificar_stock()
        elif opcion == "3":
            borrar_articulo()
        elif opcion == "4":
            mostrar_por_codigo()
        elif opcion == "5":
            mostrar_por_tipo()
        elif opcion == "6":
            obtener_stock_por_codigo()
        elif opcion == "7":
            break
        else:
            print("Opcion incorrecta, reintentar")

menu()