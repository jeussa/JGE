import numpy as np



# ===========
# = Matrix4 =
# ===========
class Matrix4:

    # = Add =
    def add(left, right):
        return left + right


    # = Create =
    def create():
        return np.identity(4)
    

    # = Multiply =
    def multiply(left, right):
        return left * right
    

    # = Rotate =    TODO: improve this method
    def rotate(matrix, angle, x, y, z):
        c=np.cos(angle)
        s=np.sin(angle)
        oneminusc=1-c
        xy=x*y
        yz=y*z
        xz=x*z
        xs=x*s
        ys=y*s
        zs=z*s
        
        f00=x*x*oneminusc+c
        f01=xy*oneminusc+zs
        f02=xz*oneminusc-ys
        
        f10=xy*oneminusc-zs
        f11=y*y*oneminusc+c
        f12=yz*oneminusc+xs
        
        f20=xz*oneminusc+ys
        f21=yz*oneminusc-xs
        f22=z*z*oneminusc+c
        
        t00=matrix[0][0]*f00+matrix[1][0]*f01+matrix[2][0]*f02
        t01=matrix[0][1]*f00+matrix[1][1]*f01+matrix[2][1]*f02
        t02=matrix[0][2]*f00+matrix[1][2]*f01+matrix[2][2]*f02
        t03=matrix[0][3]*f00+matrix[1][3]*f01+matrix[2][3]*f02
        t10=matrix[0][0]*f10+matrix[1][0]*f11+matrix[2][0]*f12
        t11=matrix[0][1]*f10+matrix[1][1]*f11+matrix[2][1]*f12
        t12=matrix[0][2]*f10+matrix[1][2]*f11+matrix[2][2]*f12
        t13=matrix[0][3]*f10+matrix[1][3]*f11+matrix[2][3]*f12
        
        matrix[2][0]=matrix[0][0]*f20+matrix[1][0]*f21+matrix[2][0]*f22
        matrix[2][1]=matrix[0][1]*f20+matrix[1][1]*f21+matrix[2][1]*f22
        matrix[2][2]=matrix[0][2]*f20+matrix[1][2]*f21+matrix[2][2]*f22
        matrix[2][3]=matrix[0][3]*f20+matrix[1][3]*f21+matrix[2][3]*f22
        matrix[0][0]=t00
        matrix[0][1]=t01
        matrix[0][2]=t02
        matrix[0][3]=t03
        matrix[1][0]=t10
        matrix[1][1]=t11
        matrix[1][2]=t12
        matrix[1][3]=t13

        return matrix
    
    # = Scale =
    def scale(matrix, x, y, z, w = 1):
        return matrix * np.array([x, y, z, w])
    
    # = Subtract =
    def sub(left, right):
        return left - right
    
    # = Translate =
    def translate(matrix, x, y, z, w = 1):
        matrix[3] = x*matrix[0] + y*matrix[1] + z*matrix[2] + w*matrix[3]
        return matrix
