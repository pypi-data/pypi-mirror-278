from AdroitFisherman.Base64Utility import Base64Block


class Base64Encoder:
    def __init__(self):
        self.__base64utility = Base64Block()

    def __del__(self):
        self.__base64utility.destroy_base64()

    def base64_encode(self, source, encode='utf-8'):
        return self.__base64utility.Base64Encryptor(bytes(source, encoding=encode)).decode(encode)

    def clear(self):
        self.__base64utility.destroy_base64()


class Base64Decoder:
    def __init__(self):
        self.__base64utility = Base64Block()

    def __del__(self):
        self.__base64utility.destroy_base64()

    def base64_decode(self, source, encode='utf-8'):
        return self.__base64utility.Base64Decryptor(bytes(source, encoding=encode)).decode(encode)

    def clear(self):
        self.__base64utility.destroy_base64()