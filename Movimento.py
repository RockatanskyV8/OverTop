import math

class Movimento:

    def __init__(self, vertices, norte):
        self.vertices = vertices
        self.norte = norte

    def centroid(self):
        x_coords = [x for x,y in self.vertices]
        y_coords = [y for x,y in self.vertices]
        centroid_x = sum(x_coords) / len(x_coords)
        centroid_y = sum(y_coords) / len(y_coords)
        return [centroid_x, centroid_y]

    def direcao(self):
        dx, dy = self.norte
        if (dx < len(self.vertices) and dy < len(self.vertices)):
            anguloF1 = sum( [x for x,y in [self.vertices[dx] , self.vertices[dy]] ]) / len([x for x,y in [self.vertices[dx] , self.vertices[dy]] ])
            anguloF2 = sum( [y for x,y in [self.vertices[dx] , self.vertices[dy]] ]) / len([y for x,y in [self.vertices[dx] , self.vertices[dy]] ])

            anguloL1 = sum( [x for x,y in [self.vertices[dx+1] , self.vertices[dy+1]] ]) / len([x for x,y in [self.vertices[dx+1] , self.vertices[dy+1]] ])
            anguloL2 = sum( [y for x,y in [self.vertices[dx+1] , self.vertices[dy+1]] ]) / len([y for x,y in [self.vertices[dx+1] , self.vertices[dy+1]] ])
            return [[anguloF1 , anguloF2] , [anguloL1 , anguloL2]]
        else:
            print("valores precisam ser menores que o total de pontos")#########

    def rotacao(self, angulo):
        angulo  = math.radians(angulo)
        cos_val = math.cos(angulo)
        sin_val = math.sin(angulo)
        cx, cy  = self.centroid()
        new_points = []
        for x_old, y_old in self.vertices:
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new + cx, y_new + cy])
        self.vertices = new_points

    def mover(self, x, y):
        new_vertices = []
        for coordenada in self.vertices:
            new_vertices.append([ coordenada[0] + x , coordenada[1] + y ])
        self.vertices = new_vertices

    def orientacao(self, orien):
        xy           = []
        new_vertices = []
        dir          = self.direcao()
        centro       = self.centroid()
        for d in range (0, len(dir)):
            f = dir[orien][d] - centro[d]
            if(f != 0):
                f = f/10
            xy.append(f)
        return xy

################################################################################COL_HANDLER

    def referencia_linhas(self):
        self.contorno = []
        for c in range(1, len(self.vertices)):
            self.contorno.append([self.vertices[c-1], self.vertices[c]])
        self.contorno.append([self.vertices[-1], self.vertices[0]])

    def mid_point(self, coordenadas):
        a , b = coordenadas
        mid_x = sum([x for x,y in coordenadas ])/len([x for x,y in coordenadas ])
        mid_y = sum([y for x,y in coordenadas ])/len([y for x,y in coordenadas ])
        return [mid_x, mid_y]

    def exists_intersection(self, line1, line2):

        def ccw(A,B,C):
            return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

        def intersect(line1, line2):
            A,B = line1
            C,D = line2
            bol1 = ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
            bol2 = (A == C or A == D) or (B == C or B == D)
            return bol1 or bol2

        resultado = []

        x1, y1 = line1[0]
        x2, y2 = line1[1]

        x3, y3 = line2[0]
        x4, y4 = line2[1]

        px_a, px_b = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)), ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        py_a, py_b = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)), ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        if ([px_a, px_b] != [0, 0] and [px_b, py_b] != [0, 0]):
            if intersect(line1, line2):
                px, py = px_a/px_b , py_a/py_b
                resultado = [px, py]

        return resultado
