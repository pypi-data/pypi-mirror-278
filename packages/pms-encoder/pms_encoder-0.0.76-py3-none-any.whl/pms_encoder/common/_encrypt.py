class Encrypt:
    def __init__(self):
        self.BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def base62_encode(self, plain_text):
        number = int.from_bytes(plain_text.encode('utf-8'), 'big')
        result = ""
        while number > 0:
            number, remainder = divmod(number, len(self.BASE62))
            result = self.BASE62[remainder] + result
        return result

    def base62_decoding(self, encoded_text):
        result = 0
        for char in encoded_text:
            result = result * len(self.BASE62) + self.BASE62.find(char)
        return result.to_bytes((result.bit_length() + 7) // 8, 'big').decode('utf-8')