import getopt, sys
import cv2

def is_rgb(im1, im2):
    return im1.shape[2] == 3 and im2.shape[2] == 3

def dim_bg(im):
    im[..., 0] = im[..., 0] - im[..., 0].min()
    im[..., 1] = im[..., 1] - im[..., 1].min()
    im[..., 2] = im[..., 2] - im[..., 2].min()
    return im

def downscale_large_image(im1, im2):
    if im1.shape[0] > im2.shape[0]:
        return downscale_large_image(im2, im1)
    dim = (im1.shape[0], im1.shape[1])
    im2 = cv2.resize(im2, dim, interpolation = cv2.INTER_AREA)
    return (im1, im2)

def photowithcode(photo_path, code_path, should_dim_bg):
    photo = cv2.imread(photo_path, cv2.IMREAD_COLOR)
    if photo is None:
        print(f'error: couldn\'t read {photo_path}')
        return
    code = cv2.imread(code_path, cv2.IMREAD_COLOR)
    if code is None:
        print(f'error: couldn\'t read {code_path}')
        return

    if is_rgb(photo, code):
        if should_dim_bg:
            print('dimming the background...')
            code = dim_bg(code)
        print('downscaling the larger image...')
        im1, im2 = downscale_large_image(photo, code)

        print('composing the image...')
        out = cv2.add(im1, im2)

        print('saving the output...')
        cv2.imwrite('photowithcode.png', out)
    else:
        print('error: both images should be rgb')

if __name__ == '__main__':
    # set default values
    photo_path = 'sample_photo.jpg'
    code_path = 'sample_code.png'
    should_dim_bg = False

    # read arguments to override
    argument_list = sys.argv[1:]
    options = 'p:c:d:'
    long_options = ['Photo=', 'Code=', 'Dim=']

    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for arg, val in arguments:
            if arg in ('-p', '--Photo'):
                photo_path = val
            elif arg in ('-c', '--Code'):
                code_path = val
            elif arg in ('-d', '--Dim'):
                should_dim_bg = bool(int(val))
                
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
    
    print('running the script with following parameters:')
    print(f'   photo_path={photo_path}')
    print(f'   code_path={code_path}')
    print(f'   should_dim_bg={should_dim_bg}')
    print('starting processing...')
    photowithcode(photo_path, code_path, should_dim_bg)