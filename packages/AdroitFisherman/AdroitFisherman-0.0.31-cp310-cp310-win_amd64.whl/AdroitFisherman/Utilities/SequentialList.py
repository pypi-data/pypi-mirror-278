from AdroitFisherman.SequentialList import SeqList


class ListObject:
    def __init__(self, size):
        self.__list = SeqList()
        self.__list.init_list(size)

    def destroy(self):
        self.__list.destroy_list()

    def clear_list(self):
        self.__list.clear_list()

    def list_empty(self):
        return self.__list.list_empty()

    def list_length(self):
        return self.__list.list_length()

    def get_elem(self, index):
        return self.__list.get_elem(index)

    def list_insert(self, index, elem):
        return self.__list.list_insert(index, elem)

    def list_delete(self, index):
        return self.__list.list_delete(index)

    def __del__(self):
        self.__list.destroy_list()

    def __str__(self):
        self.__list.traverse_list()
        return "traverse result"
