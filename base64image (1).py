import base64
image = open('whatis.this', 'rb')
image_read = image.read()
image_64_decode = base64.b64decode(image_read) 
image_result = open('decode.png', 'wb') # create a writable image and write the decoding result
image_result.write(image_64_decode)
