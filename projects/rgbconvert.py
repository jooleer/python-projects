def rgb(r, g, b):
    if r or g or b < 0:
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
    
    if r or g or b > 255:
        if r > 255:
            r = 255
        if g > 255:
            g = 255
        if b > 255:
            b = 255
            
    hr, hg, hb = hex(r), hex(g), hex(b)
    hr, hg, hb = hr.split("x"), hg.split("x"), hb.split("x")
    hr, hg, hb = hr[1], hg[1], hb[1]

    if len(hr) < 2:
        hr = "0" + str(hr)
    if len(hg) < 2:
        hg = "0" + str(hg)
    if len(hb) < 2:
        hb = "0" + str(hb)

    return (hr+hg+hb).upper()

def main():
    # tests
    print(rgb(1, 1, 1))
    print(rgb(255,255,255))
    print(rgb(-20, 275, 125))
    print(rgb(34, 168, 14))
    print(rgb(212, 10, -64))

if __name__ == '__main__':
    main()
