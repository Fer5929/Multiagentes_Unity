import math

#creación de la rueda
def rueda(esquinas, r, width, name):
    #lista de puntos y normales para la rueda
    puntos = []
    Ns = []
    # uso de funciones lambda para calcular los vectores y normales
    # los vectores se calculan con la resta de los puntos
    # los normales se calculan con el producto cruz de los vectores
    calculate_vector = lambda p1, p2: [p2[i] - p1[i] for i in range(3)]
    calculate_normal = lambda v1, v2: [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]
    for i in range(esquinas):
        #este for calcula los puntos de la rueda que se encuentran en el plano xy
        theta = 2 * math.pi * i / esquinas
        y = r * math.cos(theta) 
        z = r * math.sin(theta)
        x = width / 2 #asi se centra la rueda en el origen
        puntos.extend([[x, y, z], [-x, y, z]]) #.extend sirve para agregar los puntos a la lista y asi tener el punto y su simetrico
    for i in range(esquinas - 1):#se usa -1 porque estamos hablando del ultimo punto
        vertice1 = calculate_vector(puntos[i * 2], puntos[i * 2 + 1]) #se calcula el vector entre el punto y su simetrico
        vertice2 = calculate_vector(puntos[i * 2 + 1], puntos[i * 2 + 2])
        normal = calculate_normal(vertice1, vertice2)#se calcula el vector normal con el producto cruz de los vectores
        Ns.append(normal)
    #creacion del .obj con los datos obtenidos
    with open(name, "w") as file:
        file.write("# Rueda\n")
        file.write("# SFCF\n")
        #describe los puntos a usar en el .obj
        file.write("# Vertex\n")
        for p in puntos:
            file.write("v {} {} {}\n".format(p[0], p[1], p[2]))
        file.write("v {} 0 0\n".format(width/2))
        file.write("v {} 0 0\n".format(-width/2))
        puntos.extend([[width/2, 0, 0], [-width/2, 0, 0]])#nuevamente se usa .extend para agregar los puntos a la lista (puntos centrales)
        # Mismo procedimiento para las normales
        file.write("# Normals\n")
        for normal in Ns:
            file.write("vn {} {} {}\n".format(normal[0], normal[1], normal[2]))
        file.write("vn 1 0 0\n")
        file.write("vn -1 0 0\n")
        Ns.extend([[1, 0, 0], [-1, 0, 0]])
        # Caras
        file.write("# Faces\n")
        for i in range(esquinas):
            #el for asegura la conexión entre los puntos creando las caras
            #el if es para la cara final
            #funcionamiento dentro del if: se toma el punto central, el punto de la cara y el punto de la cara siguiente
            #se hace una cara con esos puntos
            if i == esquinas - 1:
                file.write(f"f {len(puntos) - 3}//{i + 1} {len(puntos) - 2}//{i + 1} 1//{i + 1}\n")
                file.write(f"f {len(puntos) - 2}//{i + 1} 2//{i + 1} 1//{i + 1}\n")
                #se usan las normales de los puntos centrales para las caras finales
                file.write(f"f {len(puntos) - 1}//{len(Ns) - 1} {i * 2 + 1}//{len(Ns) - 1} 1//{len(Ns) - 1}\n")
                file.write(f"f {len(puntos)}//{len(Ns) + 1} 2//{len(Ns) + 1} {i * 2 + 2}//{len(Ns) + 1}\n")
            else:
                #tiene un comportamiento parecido al if pero al no se una cara final, podemos ver que se usan los puntos de la cara siguiente
                file.write(f"f {i * 2 + 1}//{i + 1} {i * 2 + 2}//{i + 1} {i * 2 + 3}//{i + 1}\n")
                file.write(f"f {i * 2 + 4}//{i + 1} {i * 2 + 3}//{i + 1} {i * 2 + 2}//{i + 1}\n")
                file.write(f"f {len(puntos) - 1}//{len(Ns) - 1} {i * 2 + 1}//{len(Ns) - 1} {i * 2 + 3}//{len(Ns) - 1}\n")
                file.write(f"f {len(puntos)}//{len(Ns)} {i * 2 + 4}//{len(Ns)} {i * 2 + 2}//{len(Ns)}\n")
def get_user_input():
    #funcion para obtener los datos del usuario
    use_defaults = input("Usar valores predeterminados (s/n): ").strip().lower()
    if use_defaults == "s":
        esquinas= 8
        r = 1.0
        width = 0.5
    else:
        while True:
            try:
                esquinas = int(input("Esquinas (3 a 360): "))
                if 3 <= esquinas <= 360:
                    break
                else:
                    print("Valor fuera de los parámetros.")
            except ValueError:
                print("Debe ser un número.")

        r = float(input("Radio: "))
        width = float(input("Ancho: "))

    return esquinas, r, width

#funcion main pide primero los datos y después los usa para llamar a rueda, que creará el obj
if __name__ == "__main__":
    esquinas, r, width = get_user_input()
    file = "W.obj"
    rueda(esquinas, r, width,file)


