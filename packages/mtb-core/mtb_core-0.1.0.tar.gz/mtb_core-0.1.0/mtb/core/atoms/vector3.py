import numbers
from dataclasses import dataclass

import numpy as np


def operate_on_vec3(a, b, operation):
    if isinstance(b, (numbers.Number, np.ndarray)):
        return vec3(operation(a.x, b), operation(a.y, b), operation(a.z, b))
    if isinstance(b, vec3):
        return vec3(operation(a.x, b.x), operation(a.y, b.y), operation(a.z, b.z))
    return NotImplemented


def extract(cond, x):
    return x if isinstance(x, numbers.Number) else np.extract(cond, x)


@dataclass
class vec3:
    x: float
    y: float
    z: float

    def __add__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a + b)

    def __sub__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a - b)

    def __mul__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a * b)

    def __truediv__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a / b)

    def __str__(self):
        # Used for debugging. This method is called when you print an instance
        return f"({str(self.x)}, {str(self.y)}, {str(self.z)})"

    def __add__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a + b)

    def __radd__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a + b)

    def __sub__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a - b)

    def __rsub__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a - b)

    def __mul__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a * b)

    def __rmul__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a * b)

    def __truediv__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a / b)

    def __rtruediv__(self, v):
        return operate_on_vec3(self, v, lambda a, b: a / b)

    def __abs__(self):
        return vec3(np.abs(self.x), np.abs(self.y), np.abs(self.z))

    def real(self):
        return vec3(np.real(self.x), np.real(self.y), np.real(self.z))

    def imag(self):
        return vec3(np.imag(self.x), np.imag(self.y), np.imag(self.z))

    def yzx(self):
        return vec3(self.y, self.z, self.x)

    def xyz(self):
        return vec3(self.x, self.y, self.z)

    def zxy(self):
        return vec3(self.z, self.x, self.y)

    def average(self):
        return (self.x + self.y + self.z) / 3

    # def matmul(self, matrix):
    #     if isinstance(self.x, numbers.Number):
    #         return array_to_vec3(np.dot(matrix, self.to_array()))
    #     elif isinstance(self.x, np.ndarray):
    #         return array_to_vec3(np.tensordot(matrix, self.to_array(), axes=([1, 0])))

    def matmul(self, matrix):
        return vec3(*np.dot(self.to_array(), np.array(matrix)))

    def change_basis(self, new_basis):
        new_basis_matrix = np.array([b.to_array() for b in new_basis]).T
        return vec3(*np.dot(np.linalg.inv(new_basis_matrix), self.to_array()))

    def __pow__(self, a):
        return vec3(self.x**a, self.y**a, self.z**a)

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def exp(self):
        return vec3(np.exp(self.x), np.exp(self.y), np.exp(self.z))

    def sqrt(self):
        return vec3(np.sqrt(self.x), np.sqrt(self.y), np.sqrt(self.z))

    def to_array(self):
        return np.array([self.x, self.y, self.z])

    def cross(self, v):
        return vec3(
            self.y * v.z - self.z * v.y,
            -self.x * v.z + self.z * v.x,
            self.x * v.y - self.y * v.x,
        )

    def length(self):
        return np.sqrt(self.dot(self))

    def square_length(self):
        return self.dot(self)

    def normalize(self):
        mag = self.length()
        return self * (1.0 / np.where(mag == 0, 1, mag))

    def components(self):
        return (self.x, self.y, self.z)

    def extract(self, cond):
        if isinstance(cond, np.ndarray) and cond.shape == (3,):
            return vec3(
                self.x if cond[0] else 0, self.y if cond[1] else 0, self.z if cond[2] else 0
            )
        else:
            return vec3(self.x if cond else 0, self.y if cond else 0, self.z if cond else 0)

    def repeat(self, n):
        return vec3(
            np.repeat(self.x, n).tolist(),
            np.repeat(self.y, n).tolist(),
            np.repeat(self.z, n).tolist(),
        )

    def where(self, out_true, out_false):
        return vec3(
            np.where(self.x > 0, out_true.x, out_false.x).item(),
            np.where(self.y > 0, out_true.y, out_false.y).item(),
            np.where(self.z > 0, out_true.z, out_false.z).item(),
        )

    def select(self, out_list):
        out_list_x = [i.x for i in out_list]
        out_list_y = [i.y for i in out_list]
        out_list_z = [i.z for i in out_list]

        return vec3(
            np.select(self, out_list_x),
            np.select(self, out_list_y),
            np.select(self, out_list_z),
        )

    def clip(self, min, max):
        return vec3(
            np.clip(self.x, min, max),
            np.clip(self.y, min, max),
            np.clip(self.z, min, max),
        )

    def place(self, cond):
        r = vec3(np.zeros(cond.shape), np.zeros(cond.shape), np.zeros(cond.shape))
        np.place(r.x, cond, self.x)
        np.place(r.y, cond, self.y)
        np.place(r.z, cond, self.z)
        return r

    def reshape(self, *newshape):
        return vec3(
            self.x.reshape(*newshape),
            self.y.reshape(*newshape),
            self.z.reshape(*newshape),
        )

    def shape(self, *newshape):
        if isinstance(self.x, numbers.Number):
            return 1
        elif isinstance(self.x, np.ndarray):
            return self.x.shape

    def mean(self, axis):
        return vec3(
            np.mean(self.x, axis=axis),
            np.mean(self.y, axis=axis),
            np.mean(self.z, axis=axis),
        )

    def __eq__(self, other):
        return (self.x == other.x) & (self.y == other.y) & (self.z == other.z)


def array_to_vec3(array):
    return vec3(array[0], array[1], array[2])


global rgb
rgb = vec3
