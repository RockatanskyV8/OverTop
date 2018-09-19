import math

class Movimento:

    def __init__(self, vertices, norte):
        self.vertices = vertices
        self.norte = norte

    def Vertices(self):
        return self.vertices

    def Norte(self):
        return self.norte

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

    def mover(self, orien, mult):
        xy           = []
        new_vertices = []
        dir          = self.direcao()
        centro       = self.centroid()
        for d in range (0, len(dir)):
            f = dir[orien][d] - centro[d]
            if(f != 0):
                f = f/10 * (mult)
            xy.append(f)
        new_vertices = []
        for coordenada in self.vertices:
            new_vertices.append([ coordenada[0] + xy[0] , coordenada[1] + xy[1] ])
        self.vertices = new_vertices
