from AdroitFisherman.SHAUtility import SHABlock


class SHA512Encoder:
    def __init__(self):
        self.__sha = SHABlock()

    def __del__(self):
        self.__sha.destroy_sha512()

    def sha512_encode(self, source, encode='utf-8'):
        return self.__sha.update(bytes(source, encoding=encode)).decode(encode)

    def clear(self):
        self.__sha.destroy_sha512()

    def get_data(self, encode='utf-8'):
        return self.__sha.get_data().decode(encode)
