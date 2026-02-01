#include <cstring>
#include <algorithm>

extern "C" {
    struct Img { unsigned char* d; int w, h; };

    Img* filter(unsigned char* img, int w, int h) {
        Img* r = new Img{new unsigned char[w*h], w, h};
        memset(r->d, 0, w*h);
        int k[3][3] = {{1,1,1},{1,-8,1},{1,1,1}};
        
        for(int y=1; y<h-1; y++) for(int x=1; x<w-1; x++) {
            int s=0;
            for(int ky=-1; ky<=1; ky++) for(int kx=-1; kx<=1; kx++)
                s += img[(y+ky)*w+x+kx]*k[ky+1][kx+1];
            r->d[y*w+x] = std::min(255, std::abs(s));
        }
        return r;
    }

    void free_img(Img* i) { delete[] i->d; delete i; }
    unsigned char* data(Img* i) { return i->d; }
    int width(Img* i) { return i->w; }
    int height(Img* i) { return i->h; }
}