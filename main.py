import cv2
import tkinter, os
from PIL import Image, ImageTk, ImageDraw
import json
import calendar, time, threading, numpy

cam = cv2.VideoCapture(1)

cv2.namedWindow("lol sexy will")

thresh_on = (0x7a, 0xc6, 0xa0)
thresh_low = 70
thresh_high = 90

f = True


current_milli_time = lambda: int(round(time.time() * 1000))

c = 250
cf = current_milli_time() + c

def proc_img():
    imf = Image.open('inp.png')
    try:
        imfa = imf.load()
        print('Image loaded')
        for x in range(imf.width):
                for y in range(imf.height):
                    c_pixel = imfa[x, y]
                    pass_r = c_pixel[0] > thresh_low
                    pass_g = c_pixel[1] > thresh_high
                    pass_b = c_pixel[2] > thresh_low
                    if pass_r and pass_g and pass_b:
                        ret_pix = (255, 255, 255, 255)
                    else:
                        ret_pix = (0, 0, 0, 255)
                    imfa[x, y] = ret_pix
        imf.save('final.png')
    except OSError:
        print('OS Error')
    except ValueError:
        print('Value Error')
    except SyntaxError:
        print('PNG error. its fine fam')
    try:
        imf = imf
        imf.thumbnail((int(imf.width / 8), int(imf.height / 8)))
        imf.save('thumb.png')
        print('Thumbnail created')
        px = imf.load()
        imgpickup = []
        for x in range(imf.width):
            for y in range(imf.height):
                #print(px[x, y])
                if px[x, y] == (255, 255, 255):
                    #print('Pixel on')
                    # Pixel on
                    cont_l = True
                    cont_l_val = [0, 0]
                                # Point, offset

                    cont_r = True
                    cont_r_val = [0, 0]

                    cont_u = True
                    cont_u_val = [0, 0]

                    cont_d = True
                    cont_d_val = [0, 0]
                    #print('Scanning image')
                    while cont_l or cont_r or cont_u or cont_d:
                        if cont_l:
                            try:
                                cont_l_val[1] += 1
                                px_l = px[x - cont_l_val[1], y]
                                #print('cont l finish')
                            except IndexError:
                                cont_l = False
                        if cont_r:
                            try:
                                cont_r_val[1] += 1
                                px_r = px[x + cont_r_val[1], y]
                                #print('cont r finish')
                            except IndexError:
                                cont_r = False
                        if cont_u:
                            try:
                                cont_u_val[1] += 1
                                px_u = px[x, y - cont_u_val[1]]
                                #print('cont u finish')
                            except IndexError:
                                cont_u = False
                        if cont_d:
                            try:
                                cont_d_val[1] += 1
                                px_d = px[x, y + cont_d_val[1]]
                                #print('cont d finish')
                            except IndexError:
                                cont_d = False
                        
                        #print(px_l, px_r, px_d, px_u)

                        if px_l != (255, 255, 255):
                            cont_l_val[0] = cont_l_val[0] + 1
                            #print("px_l_+")
                            if cont_l_val[0] == 10:
                                cont_l = False
                                #print('cont l finish')
                        
                        if px_r != (255, 255, 255):
                            cont_r_val[0] = cont_r_val[0] + 1
                            #print("px_r_+")
                            if cont_r_val[0] == 10:
                                cont_r = False
                                #print('cont r finish')
                        
                        if px_u != (255, 255, 255):
                            cont_u_val[0] = cont_u_val[0] + 1
                            #print("px_u_+")
                            if cont_u_val[0] == 10:
                                cont_u = False
                                #print('cont u finish')
                        
                        if px_d != (255, 255, 255):
                            cont_d_val[0] = cont_d_val[0] + 1
                            #print("px_d_+")
                            if cont_d_val[0] == 10:
                                cont_d = False
                                #print('cont d finish')
                    imgpickup.append([
                        [x, y], 
                        [-cont_l_val[1], cont_r_val[1], -cont_u_val[1], -cont_d_val[1]]
                        ])
    except:
        pass
                
                #print('Pixel scan complete')
    try:
        print(imgpickup)
        json.dump(imgpickup, open('sqr.json', 'w'))
    except:
        pass

f = []
b = Image.new('RGB', (60, 60), color = 'blue').save('blue.png')
b = Image.open('blue.png')

while True:
    frame = numpy.array(b)
    im = Image.fromarray(frame)
    j = json.load(open('settings.json'))
    if j['auto']:
        # Auto detect background
        fp = im.load()
        print('Detecting background...')
        avg_r = 0
        avg_g = 0
        avg_b = 0
        for x in range(im.width):
            for y in range(im.height):
                px = fp[x, y]
                avg_r += px[0]
                avg_g += px[1]
                avg_b += px[2]
        avg_r = avg_r / im.width * im.height
        avg_g = avg_g / im.width * im.height
        avg_b = avg_b / im.width * im.height
        thresh_on = (avg_r, avg_g, avg_b)
        print(thresh_on)
        j['auto'] = False
        json.dump(j, open('settings.json', 'w'))
    if j['camera-on']:
        if j['mask'] == False:
            ret, frame = cam.read()
            im = Image.fromarray(frame)
        else:
            im = Image.open('final.png')
    else:
        pass
    try:
        f = json.load(open('sqr.json'))
    except:
        pass
    
    dr = ImageDraw.Draw(im)
    dr.text((10, 10), "VR-Bust Motion Tracking")
    for bf in f:
        x, y = bf[0]
        offset = bf[1]
        rect = [(x * 8) + (offset[0] * 8), (y * 8) + (offset[2] * 8), (x * 8) + (offset[1] * 8), (y * 8) + (offset[3] * 8)] # upscale values by downscale
        dr.rectangle(rect, outline="yellow")
    im.save("temp.png")
    
    frame = numpy.array(im)
    cv2.imshow("test", frame)
    
    
    k = cv2.waitKey(1)

    if json.load(open('settings.json'))['active']:

    #print(c, cf, calendar.timegm(time.gmtime()))

        if current_milli_time() > cf:
            cf = current_milli_time() + c
            print('Processing...')
            img_name = "inp.png"
            cv2.imwrite(img_name, frame)
            threading.Thread(target=proc_img).start()