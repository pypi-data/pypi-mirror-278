from AdroitFisherman.CircularSingleLinkedList import SingleLinkedList


class ListObject:
    def __init__(self):
        self.__list = SingleLinkedList()
        self.__list.init_list()

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

    def add_first(self, elem):
        return self.__list.add_first(elem)

    def add_after(self, elem):
        return self.__list.add_after(elem)

    def list_insert(self, index, elem):
        return self.__list.list_insert(index, elem)

    def list_delete(self, index):
        return self.__list.list_delete(index)

    def __del__(self):
        self.__list.destroy_list()

    def __str__(self):
        self.__list.traverse_list()
        return "traverse result"
