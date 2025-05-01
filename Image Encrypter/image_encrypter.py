from PIL import Image
import random

def encrypt(file1,file2):
    """encrypts the image. file1 is the file to be encrypted. file2 is the name of the new encrypted file"""
    
    if (file2[-4:] == ".jpg"):
        file2 = file2[0:len(file2)-4]+".png"
        print("WARNING:")
        print(".jpgs are not able to be encrypted since they lose important pixel information.")
        print("your encrypted file extension has been replaced with a .png extension.")
    elif(file2[-5:] == ".jpeg"):
        file2 = file2[0:len(file2)-5]+".png"
        print("WARNING:")
        print(".jpgs are not able to be encrypted since they lose important pixel information.")
        print("your encrypted file extension has been replaced with a .png extension.")

    img = Image.open(file1).convert('RGB') 
    random.seed(1234) 

    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            pixel = (pixel[0]+random.randint(0,255))%256,(pixel[1]+random.randint(0,255))%256,(pixel[2]+random.randint(0,255))%256
            img.putpixel((x,y),pixel)
    img.show()
    img.save(file2)

def decrypt(file1,file2):
    """decrypts the image. file1 is the name of the file to be decrypted. file2 is the new name of the decrypted file"""
    img = Image.open(file1).convert('RGB') 
    random.seed(1234)

    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            R,G,B = (pixel[0]-random.randint(0,255))%256 ,(pixel[1]-random.randint(0,255))%256,(pixel[2]-random.randint(0,255))%256
            pixel = R,G,B
            img.putpixel((x,y),pixel)
    img.show()
    img.save(file2)

encrypt('brock_before.jpg',"brock_after.jpg")
decrypt("brock_after.png",'brock_before.jpg')