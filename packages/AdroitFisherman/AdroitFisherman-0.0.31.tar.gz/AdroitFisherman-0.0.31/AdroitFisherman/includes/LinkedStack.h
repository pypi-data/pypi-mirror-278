#ifndef LINKEDSTACK_H
#define LINKEDSTACK_H
typedef PyObject* ElemType;
typedef struct Node
{
    PyObject_HEAD
        ElemType elem;
    struct Node* next;
}StackNode;
typedef struct {
    PyObject_HEAD
    StackNode* instance;
    int length;
}LinkedStack;
static void StackNode_destroy(StackNode* self)
{
    Py_DECREF(self->elem);
    Py_DECREF(self->next);
    Py_TYPE(self)->tp_free(self);
}
static PyObject* StackNode_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    StackNode* node = (StackNode*)type->tp_alloc(type, 0);
    if (node == NULL)
    {
        Py_RETURN_NONE;
    }
    else
    {
        node->elem = NULL;
        node->next = NULL;
        Py_INCREF(node);
        return (PyObject*)node;
    }
}
static int StackNode_init(StackNode* self, PyObject* args, PyObject* kwds)
{
    return 0;
}
static PyMemberDef StackNode_members[] = {
    {"elem",T_OBJECT,offsetof(StackNode,elem),0,""},
    {"next",T_OBJECT,offsetof(StackNode,next),0,""},
    {NULL}
};
static void LinkedStack_destroy(LinkedStack* self)
{
    Py_DECREF(self->instance);
    Py_TYPE(self)->tp_free(self);
}
static PyObject* LinkedStack_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    LinkedStack* stack = type->tp_alloc(type, 0);
    if (stack == NULL)
    {
        Py_RETURN_NONE;
    }
    else
    {
        stack->instance = NULL;
        stack->length = 0;
        Py_INCREF(stack);
        return (PyObject*)stack;
    }
}
static int LinkedStack_init(LinkedStack* self, PyObject* args, PyObject* kwds)
{
    return 0;
}
static PyMemberDef LinkedStack_members[] = {
    {"instance",T_OBJECT,offsetof(LinkedStack,instance),0,""},
    {"length",T_INT,offsetof(LinkedStack,length),0,""},
    {NULL}
};
static PyObject* InitStack(LinkedStack* self, PyObject* args)
{
    int length;
    if (PyArg_ParseTuple(args, "i", &length) < 0)
    {
        Py_RETURN_FALSE;
    }
    else
    {
        self->instance = (StackNode*)malloc(sizeof(StackNode));
        if (self->instance == NULL)
        {
            Py_RETURN_FALSE;
        }
        else
        {
            self->instance->next = NULL;
            self->length = length;
            Py_RETURN_TRUE;
        }
    }
}
static PyObject* DestroyStack(LinkedStack* self)
{
    StackNode* p = self->instance;
    while (self->instance != NULL)
    {
        p = self->instance;
        self->instance = p->next;
        free(p);
        p = NULL;
    }
    self->length = 0;
    Py_RETURN_TRUE;
}
static PyObject* ClearStack(LinkedStack* self)
{
    StackNode* p = self->instance->next;
    while (self->instance->next != NULL)
    {
        p = self->instance->next;
        self->instance->next = p->next;
        free(p);
        p = NULL;
    }
    Py_RETURN_TRUE;
}
static PyObject* StackEmpty(LinkedStack* self)
{
    if (self->instance->next == NULL)
    {
        Py_RETURN_TRUE;
    }
    else
    {
        Py_RETURN_FALSE;
    }
}
static PyObject* StackLength(LinkedStack* self)
{
    StackNode* p = self->instance;
    int counter = 0;
    while (counter < self->length && p->next != NULL)
    {
        counter++;
        p = p->next;
    }
    PyObject* result = Py_BuildValue("i", counter);
    Py_INCREF(result);
    return result;
}
static PyObject* GetTop(LinkedStack* self)
{
    if (self->instance->next != NULL)
    {
        Py_INCREF(self->instance->next->elem);
        return self->instance->next->elem;
    }
    else
    {
        Py_RETURN_NONE;
    }
}
static PyObject* Push(LinkedStack* self, PyObject* args)
{
    if (StackLength(self) == self->length)
    {
        Py_RETURN_FALSE;
    }
    else {
        PyObject* elem;
        if (PyArg_ParseTuple(args, "O", &elem) < 0)
        {
            Py_RETURN_FALSE;
        }
        else
        {
            StackNode* summon = (StackNode*)malloc(sizeof(StackNode));
            if (summon == NULL)
            {
                Py_RETURN_FALSE;
            }
            else
            {
                Py_INCREF(elem);
                summon->elem = elem;
                summon->next = self->instance->next;
                self->instance->next = summon;
                Py_RETURN_TRUE;
            }
        }
    }
}
static PyObject* Pop(LinkedStack* self)
{
    if (self->instance->next == NULL)
    {
        Py_RETURN_NONE;
    }
    else {
        StackNode* p = self->instance->next;
        self->instance->next = p->next;
        ElemType tmp = p->elem;
        free(p);
        p = NULL;
        Py_INCREF(tmp);
        return tmp;
    }
}
static PyObject* StackTraverse(LinkedStack* self)
{
    StackNode* p = self->instance->next;
    while (p != NULL)
    {
        PyObject_Print(p->elem, stdout, 0);
        p = p->next;
    }
    printf("\n");
    Py_RETURN_NONE;
}
static PyMethodDef methods[] = {
    {"init_stack",InitStack,METH_VARARGS,""},
    {"destroy_stack",DestroyStack,METH_NOARGS,""},
    {"clear_stack",ClearStack,METH_NOARGS,""},
    {"stack_empty",StackEmpty,METH_NOARGS,""},
    {"stack_length",StackLength,METH_NOARGS,""},
    {"get_top",GetTop,METH_NOARGS,""},
    {"push",Push,METH_VARARGS,""},
    {"pop",Pop,METH_NOARGS,""},
    {"traverse",StackTraverse,METH_NOARGS,""},
    {NULL}
};
static PyTypeObject StackNode_object = {
    PyVarObject_HEAD_INIT(NULL,0)
    .tp_name = "LinkedStack.Node",
    .tp_new = StackNode_new,
    .tp_init = (initproc)StackNode_init,
    .tp_dealloc = (destructor)StackNode_destroy,
    .tp_basicsize = sizeof(StackNode),
    .tp_itemsize = 0,
    .tp_members = StackNode_members,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE
};
static PyTypeObject LinkedStack_object = {
    PyVarObject_HEAD_INIT(NULL,0)
    .tp_name = "LinkedStack.Stack",
    .tp_new = LinkedStack_new,
    .tp_init = (initproc)LinkedStack_init,
    .tp_dealloc = (destructor)LinkedStack_destroy,
    .tp_basicsize = sizeof(LinkedStack),
    .tp_itemsize = 0,
    .tp_members = LinkedStack_members,
    .tp_methods = methods,
    .tp_flags = Py_TPFLAGS_BASETYPE | Py_TPFLAGS_DEFAULT
};
#endif // !LINKEDSTACK_H
