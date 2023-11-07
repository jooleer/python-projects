# converts rgb 0-255, 0-255, 0-255 to hex ######

def limit_value(number):
    if number < 0:
        return 0
    if number > 255:
        return 255
    return number

def rgb(r, g, b):
    r, g, b = limit_value(r), limit_value(g), limit_value(b)
            
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
