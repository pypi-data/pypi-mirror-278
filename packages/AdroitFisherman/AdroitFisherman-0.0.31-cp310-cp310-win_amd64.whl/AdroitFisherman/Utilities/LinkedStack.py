from AdroitFisherman.LinkedStack import Stack


class StackObject:
    def __init__(self, length):
        self.__stack = Stack()
        self.__stack.init_stack(length)

    def destroy(self):
        self.__stack.destroy_stack()

    def clear_stack(self):
        self.__stack.clear_stack()

    def stack_empty(self):
        return self.__stack.stack_empty()

    def stack_length(self):
        return self.__stack.stack_length()

    def get_top(self):
        return self.__stack.get_top()

    def push(self, elem):
        return self.__stack.push(elem)

    def pop(self):
        return self.__stack.pop()

    def __del__(self):
        self.__stack.destroy_stack()

    def __str__(self):
        self.__stack.traverse()
        return "traverse result"
