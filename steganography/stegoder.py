from PIL import Image
from bitarray import bitarray
import os

file_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

class ImgTooSmallException(Exception):
    pass

def str_to_bits(msg: str):
    ba = bitarray()
    ba.frombytes(msg.encode('utf-8'))
    ba = ba.to01()
    return ba

def bits_to_str(msg_bits):
    ba = bitarray(msg_bits).tostring()
    return ba

def get_img_capacity(img_size):
    return (img_size[0] * img_size[1]) * 3

def check_length(img_size: tuple, msg_bits):
    img_capacity = get_img_capacity(img_size)
    return img_capacity > len(msg_bits)

def pad_msg(msg_bits, img_size):
    msg = bits_to_str(msg_bits)

    img_capacity = get_img_capacity(img_size)
    available_bytes = img_capacity // 8
    
    while len(msg) != available_bytes:
        msg += "."
    msg_bits = str_to_bits(msg)
    return msg_bits 

def rgb_dec_to_bits(rgb_dec: tuple):
    return [bin(val) for val in rgb_dec]

def rgb_bits_to_dec(rgb_bits: list):
    return tuple(int(val, 2) for val in rgb_bits)

def hide(msg_bits: str, source_img: str):
    i = 0

    try:
        with Image.open(file_dir + source_img) as img:
            width, height = img.size

            if not check_length(img.size, msg_bits):
                raise ImgTooSmallException()
            else:
                msg_bits = pad_msg(msg_bits, img.size)
            
            rgb_img = img.convert('RGB')
            pixels = rgb_img.load()

            valid = True
            while valid:
                for y in range(height):
                    if not valid:
                        break

                    for x in range(width):
                        if not valid:
                            break

                        new_rgb = []
                        pixels_bits = rgb_dec_to_bits(pixels[x, y])
                        # for ea val in rgb binary values
                        for val in pixels_bits:

                            # whole msg not hidden yet
                            if i < len(msg_bits):
                                val = val[:-1] + msg_bits[i]
                                new_rgb.append(val)
                                i += 1
                            else:
                                if len(new_rgb) < 3:
                                    for i in range(3 - len(new_rgb)):
                                        new_rgb.extend(pixels_bits[len(new_rgb):])
                                elif len(new_rgb) == 3:
                                    pixels[x, y] = rgb_bits_to_dec(new_rgb)
                                valid = False
                                break
                        
                        pixels[x, y] = rgb_bits_to_dec(new_rgb)

            rgb_img.save(file_dir + "final_lsb_" + source_img)
            print(f"Message hidden!\nImage saved to <final_lsb_{source_img}>.\n")
            stegoder_menu()

    except FileNotFoundError:
        print("Image given is not found. Please try another.\n")
        stegoder_menu()
    except ImgTooSmallException:
        print("Image provided is not big enough to hide the message.\n")
        stegoder_menu()

def find(source_img):
    msg_bits = []
    try:
        with Image.open(file_dir + source_img) as img:
            width, height = img.size

            i = get_img_capacity(img.size)
            
            rgb_img = img.convert('RGB')
            pixels = rgb_img.load()

            valid = True
            for y in range(height):
                if not valid:
                    break
                for x in range(width):
                    if not valid:
                        break

                    pixel_bits = rgb_dec_to_bits(pixels[x, y])
                    for val in pixel_bits:
                        if i > 0:
                            msg_bits.append(val[-1])
                            i -= 1
                        else:
                            valid = False
                            break
            
            result_bits = "".join(msg_bits)
            result: str = bits_to_str(result_bits)
            result = result.replace(".", "")
            return result

    except FileNotFoundError:
        print("Image not found. Try again.\n")
        stegoder_menu()


def stegoder_menu():
    action = input('''Welcome to Stecoder!
What would you like to do today?
1. Hide message
2. Find message
3. Exit
>>> ''')
    while True:
        if action in ["1", "2", "3"]:
            if action == "1":
                msg = input("Enter message to hide: ")
                src_img = input("Enter source image to use: ")

                msg_bits = str_to_bits(msg)

                hide(msg_bits, src_img)
                    
            elif action == "2":
                steg_img = input("Enter image to uncover: ")

                result = find(steg_img)

                print("Message found!")
                print(f"Uncovered Message: {result}\n")
                stegoder_menu()
            elif action == "3":
                print("Exiting...")
                os._exit(1)
        else:
            print("Please input a valid action.")


def main():
    print('''
      .-')    .-') _     ('-.                          _ .-') _     ('-.  _  .-')   
 ( OO ). (  OO) )  _(  OO)                        ( (  OO) )  _(  OO)( \( -O )  
(_)---\_)/     '._(,------. ,----.     .-'),-----. \     .'_ (,------.,------.  
/    _ | |'--...__)|  .---''  .-./-') ( OO'  .-.  ',`'--..._) |  .---'|   /`. ' 
\  :` `. '--.  .--'|  |    |  |_( O- )/   |  | |  ||  |  \  ' |  |    |  /  | | 
 '..`''.)   |  |  (|  '--. |  | .--, \\_) |  |\|  ||  |   ' |(|  '--. |  |_.' | 
.-._)   \   |  |   |  .--'(|  | '. (_/  \ |  | |  ||  |   / : |  .--' |  .  '.' 
\       /   |  |   |  `---.|  '--'  |    `'  '-'  '|  '--'  / |  `---.|  |\  \  
 `-----'    `--'   `------' `------'       `-----' `-------'  `------'`--' '--' 
    ''')

    stegoder_menu()
   

if __name__ == '__main__':
    main()