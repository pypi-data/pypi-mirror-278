import io
import math
from PIL import Image
from uuid import uuid4

_8_bit_mask = 0b11111111
_24_bit_mask = 0b111111111111111111111111

_encrypted_image_buffer = io.BytesIO()


def _load_image(filename: str):
    ''' Загружает изображение в массив пикселей
    '''
    im = Image.open(filename)
    width, height = im.size
    pixel_array = im.load()
    return (pixel_array, width, height, im)


def str_to_bytes(msg):
    return ' '.join(format(ord(x), 'b') for x in msg)


def _insert_msg(pixel_array_tuple, msg, q_const):
    ''' Вставляет переданное сообщение в изображение
    '''
    pixel_array, width, height, im = pixel_array_tuple
    msg_index = 0
    msg_len = len(msg)
    for i in range(0, height):
        for k in range(0, width):
            r, g, b = pixel_array[k, i]
            if ord(msg[msg_index]) == 0:
                pixel_array[k, i] = (
                    r, g, b + math.ceil(q_const * (0.299 * r + 0.587 * b + 0.114 * b)))
            else:
                pixel_array[k, i] = (
                    r, g, b - math.ceil(q_const * (0.299 * r + 0.587 * b + 0.114 * b)))
            msg_index += 1
            if msg_index == msg_len:
                im.save(_encrypted_image_buffer, 'JPG')
                _encrypted_image_buffer.seek(0)
                return


def _gen_key():
    ''' Генерация ключа для шифрования с помощью сети Фейстеля
    '''
    u = uuid4()
    return (
        ((u.node & _24_bit_mask) << 40)
        + ((u.clock_seq_hi_variant & _8_bit_mask) << 32)
        + ((u.clock_seq_low & _8_bit_mask) << 24)
        + ((u.time_hi_version & _8_bit_mask) << 16)
        + ((u.time_mid & _8_bit_mask) << 8)
        + u.time_low
    )


def _feistel_cipher(block, key, n):
    ''' Применение функции шифрования блока сообщения
    '''
    L = block[:4]
    R = block[4:]

    for _ in range(n):
        new_R = bytes([L[j] ^ key[j] for j in range(4)])
        L, R = R, new_R

    return R + L


def _encrypt_image(data, filename_out, key, n):
    ''' Шифрование изображения с помощью сети Фейстеля
    '''
    encrypted_data = b''
    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        if len(block) < 8:
            block += b'\0' * (8 - len(block))
        encrypted_block = _feistel_cipher(block, key, n)
        encrypted_data += encrypted_block

    with open(filename_out, 'wb') as f:
        f.write(encrypted_data)


def save_encrypted_image(filepath: str):
    '''Сохранить зашифрованное изображение в файловой системе
    '''
    img = Image.open(_encrypted_image_buffer)
    img.save(filepath)


def encrypt_data_in_image(data_buf,
                          image_filename,
                          encrypted_filename,
                          q_const,
                          n_iterations) -> int:
    ''' Зашифровать сообщение в изображении и обработать файл с помощью сети Фейстеля
    Параметры:
        - data_buf: данные для шифрования в битах
        - image_filename: название файла с изображением, в которое будет производиться вставка
        - encrypted_filename: название зашифрованного выходного файла
        - q_const: константа для установки степени влияния зашифрованного бита на оттенок пикселя
        - n_iterations: количество раундов сети Фейстеля

    Возвращает:
        - сгенерированный 64-битный ключ для сети Фейстеля
    '''
    image_info = _load_image(image_filename)
    _insert_msg(image_info, data_buf, q_const)
    key = _gen_key()
    _encrypt_image(_encrypted_image_buffer.read(), encrypted_filename, key, n_iterations)
    return key
