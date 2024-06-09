import os
from bitarray._bitarray import bitarray
from PIL import Image


def _load_image(filename: str):
    ''' Загружает изображение в массив пикселей
    '''
    im = Image.open(filename)
    width, height = im.size
    pixel_array = im.load()
    return (pixel_array, width, height, im)


def _extract_msg_from_image(pixel_array_tuple, c, msg_len):
    ''' Выделяет биты исходного сообщения
    '''
    pixel_array, width, height, _ = pixel_array_tuple
    msg = bitarray()
    for y in range(0, height):
        for x in range(0, width):
            if msg_len == 0:
                return msg
            _, _, curr_pixel_blue = pixel_array[x, y]

            x_sum = 0
            for i in range(x - c, x + c):
                if i < 0 or i > width - 1:
                    continue
                _, _, b = pixel_array[i, y]
                x_sum += b
            y_sum = 0
            for i in range(y - c, y + c):
                if i < 0 or i > height - 1:
                    continue
                _, _, b = pixel_array[x, i]
                y_sum += b

            b_value = (1 / 4 * c) * (-2 * curr_pixel_blue * x_sum + y_sum)
            b_mean = b_value - curr_pixel_blue
            msg += [b_mean > 0]

    return msg.tobytes().decode('utf8')


def _feistel_decipher(block, key, n):
    ''' Применение функции расшифрования блока сообщения
    '''
    L = block[:4]
    R = block[4:]

    for _ in range(n):
        new_L = bytes([R[j] ^ key[j] for j in range(4)])
        L, R = new_L, L

    return R + L


def _decrypt_file(filename_in, filename_out, key, n):
    ''' Расшифровать файл с помощью переданного ключа и количества раундов
    '''
    with open(filename_in, 'rb') as f:
        data = f.read()

    decrypted_data = b''
    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        decrypted_block = _feistel_decipher(block, key, n)
        decrypted_data += decrypted_block

    with open(filename_out, 'wb') as f:
        f.write(decrypted_data)


def decrypt_data_from_image(
                          encrypted_filename,
                          key,
                          c_const,
                          msg_len,
                          n_iterations) -> int:
    ''' Расшифровать сообщение из изображения, закодированного с помощью сети Фейстеля
    Параметры:
        - encrypted_filename: название зашифрованного входного файла
        - key: 64-битный ключ для сети Фейстеля
        - c_const: константа для установки количества пикселей, в пределах которого будет производиться поиск зашифрованного бита
        - msg_len: длина зашифрованного сообщения
        - n_iterations: количество раундов сети Фейстеля

    Возвращает:
        - расшифрованный буфер данных из файла
    '''
    _decrypt_file(encrypted_filename, 'tmp.jpg', key, n_iterations)
    image_info = _load_image('tmp.jpg')
    data = _extract_msg_from_image(image_info, c_const, msg_len)
    os.remove('tmp.jpg')
    return data
