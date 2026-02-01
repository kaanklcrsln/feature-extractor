import ctypes as c, numpy as np, matplotlib.pyplot as plt, os
from PIL import Image

lib = c.CDLL(os.path.join(os.path.dirname(__file__), 'liblaplacian.dylib'))

class I(c.Structure):
    _fields_ = [("d", c.POINTER(c.c_ubyte)), ("w", c.c_int), ("h", c.c_int)]

f = lib.filter
f.argtypes = [c.POINTER(c.c_ubyte), c.c_int, c.c_int]
f.restype = c.POINTER(I)

lib.data.argtypes = [c.POINTER(I)]
lib.data.restype = c.POINTER(c.c_ubyte)
lib.width.argtypes = [c.POINTER(I)]
lib.width.restype = c.c_int
lib.height.argtypes = [c.POINTER(I)]
lib.height.restype = c.c_int
lib.free_img.argtypes = [c.POINTER(I)]

def laplacian(p):
    img = np.array(Image.open(p).convert('L'), dtype=np.uint8)
    h, w = img.shape
    r = f(img.ctypes.data_as(c.POINTER(c.c_ubyte)), w, h)
    rh = lib.height(r)
    rw = lib.width(r)
    d = np.ctypeslib.as_array(lib.data(r), (rh, rw)).copy()
    lib.free_img(r)
    return img, d

def show(p):
    o, filtered = laplacian(p)
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    ax[0].imshow(o, cmap='gray')
    ax[0].set_title('Orijinal')
    ax[1].imshow(filtered, cmap='gray')
    ax[1].set_title('Laplacian')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    show('image-ex.jpg')
