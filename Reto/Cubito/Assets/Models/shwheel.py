"""
Program that creates a wheel in obj format with a given number of vertices.

args: number of edges of the wheel, the radius of the wheel and width of the wheel

"""
import sys
import math


# Function to create the vertices and normals of the wheel with the given number of edges
def createWheel(numEdges, radius, width, outputFile):
    points = []
    normals = []

    for i in range(numEdges):
        angle = 2 * math.pi * i / numEdges
        y = radius * math.cos(angle)
        z = radius * math.sin(angle)
        x = width / 2
        points.append([x, y, z])
        points.append([-x, y, z]) # Add the other side of the wheel


    for i in range(numEdges -1):
        if(numEdges != numEdges -2):
            # Calculate the normal of the first triangle
            vertice1 = [points[i *2 + 1][0] - points[i * 2][0], points[i *2 + 1][1] - points[i * 2][1], points[i *2 + 1][2] - points[i * 2][2]]
            # Calculate the normal of the second triangle
            vertice2 = [points[i *2 + 2][0] - points[i * 2 + 1][0], points[i *2 + 2][1] - points[i * 2 + 1][1], points[i *2 + 2][2] - points[i * 2 + 1][2]]
        else:
            # Calculate the normal of the first triangle
            vertice1 = [points[i *2 + 1][0] - points[i * 2][0], [points[i *2 + 1][1] - points[i * 2][1]], [points[i *2 + 1][2] - points[i * 2][2]]]
            # Calculate the normal of the second triangle
            vertice2 = [points[0][0] - points[i * 2 + 1][0], [points[0][1] - points[i * 2 + 1][1]], [points[0][2] - points[i * 2 + 1][2]]]

        normal = crossProduct(vertice1, vertice2)
        normal = normalize(normal)
        normals.append(normal)

    #Open the file to write the wheel
    with open(file, "w") as outputFile: 
        for point in points:
            outputFile.write("v " + str(point[0]) + " " + str(point[1]) + " " + str(point[2]) + "\n") 
        # write the center points
        outputFile.write("v " + str(width/2) + "  0  0\n")
        outputFile.write("v " + str(-width/2) + "  0  0\n")
        points.append([width/2, 0, 0])
        points.append([-width/2, 0, 0])
        #Write the normals
        for normal in normals:
            outputFile.write("vn " + str(normal[0]) + " " + str(normal[1]) + " " + str(normal[2]) + "\n")
        outputFile.write("vn 1 0 0\n")
        outputFile.write("vn -1 0 0\n")
        normals.append([1, 0, 0])
        normals.append([-1, 0, 0])

        #Write the faces
        for i in range(numEdges):
            if(i == numEdges -1):
                outputFile.write("f " + str(len(points) -3) + "//" + str(i + 1) + " " + str(len(points)-2) + "//" + str(i + 1) + " " + str(1) + "//" + str(i + 1) + "\n")
                outputFile.write("f " + str(len(points) -2 )+ "//" + str(i + 1) + " " + str(2) + "//" + str(i + 1) + " " + str(1) + "//" + str(i + 1) + "\n")

                #write the lateral faces using the length of the points array
                outputFile.write("f " + str(len(points) - 1) + "//" + str(len(normals) - 1) + " " + str(i * 2 + 1) + "//" + str(len(normals) - 1) + " " + str(1) + "//" + str(len(normals) - 1) + "\n")
                outputFile.write("f " + str(len(points)) + "//" + str(len(normals) + 1) + " " + str(2) + "//" + str(len(normals) + 1) + " " + str(i * 2 + 2) + "//" + str(len(normals) + 1) + "\n")

            else:
                outputFile.write("f " + str(i * 2 + 1) + "//" + str(i + 1) + " " + str(i * 2 + 2) + "//" + str(i + 1) + " " + str(i *2 + 3) + "//" + str(i + 1) + "\n")
                outputFile.write("f " + str(i * 2 + 4) + "//" + str(i + 1) + " " + str(i *2 + 3) + "//" + str(i + 1) + " " + str(i *2 + 2) + "//" + str(i + 1) + "\n")

                #write the lateral faces using the length of the points array
                outputFile.write("f " + str(len(points) - 1) + "//" + str(len(normals) - 1) + " " + str(i * 2 + 1) + "//" + str(len(normals) - 1) + " " + str(i * 2 + 3) + "//" + str(len(normals) - 1) + "\n")
                outputFile.write("f " + str(len(points)) + "//" + str(len(normals)) + " " + str(i * 2 + 4) + "//" + str(len(normals)) + " " + str(i * 2 + 2) + "//" + str(len(normals)) + "\n")

         
def crossProduct(vertice1, vertice2):
    normal = [
        vertice1[1] * vertice2[2] - vertice1[2] * vertice2[1],
        vertice1[2] * vertice2[0] - vertice1[0] * vertice2[2],
        vertice1[0] * vertice2[1] - vertice1[1] * vertice2[0]
    ]
    return normal

def normalize(normal):
    magnitude = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
    return [normal[0] / magnitude, normal[1] / magnitude, normal[2] / magnitude]



if __name__ == "__main__":
    # Set default values for numEdges, radius, and width
    numEdges = 8
    radius = 1.0
    width = 0.5

    # Check the number of command-line arguments
    if len(sys.argv) >= 4:
        numEdges = int(sys.argv[1])
        radius = float(sys.argv[2])
        width = float(sys.argv[3])

    # Check if the provided values are valid
    if numEdges < 3:
        numEdges = 3
    if radius < 1.0:
        radius = 1.0
    if width < 0.5:
        width = 0.5

    file = "W.obj"
    createWheel(numEdges, radius, width, file)
