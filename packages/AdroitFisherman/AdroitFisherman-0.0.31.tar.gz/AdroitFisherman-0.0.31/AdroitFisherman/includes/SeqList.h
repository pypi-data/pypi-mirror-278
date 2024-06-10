#ifndef SEQUENTIALLIST
#define SEQUENTIALLIST
typedef PyObject* ElemType;
typedef struct
{
    PyObject_HEAD
        ElemType* elem;
    int length;
    int size;
}SeqList;
static void SeqList_destroy(SeqList* self)
{
    Py_DECREF(self->elem);
    printf("DEBUG:[any_thread]-- This object has been released!");
    Py_TYPE(self)->tp_free(self);
}
static PyObject* SeqList_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    SeqList* list;
    list = (SeqList*)type->tp_alloc(type, 0);
    if (list == NULL)
    {
        PyErr_SetString(PyExc_Exception, "list object created failure!");
        return NULL;
    }
    else
    {
        list->elem = NULL;
        list->length = 0;
        list->size = 0;
        Py_INCREF(list);
        return (PyObject*)list;
    }
}
static int SeqList_init(SeqList* self, PyObject* args, PyObject* kwds)
{
    return 0;
}
static PyMemberDef SeqList_members[] = {
    {"elem",T_OBJECT,offsetof(SeqList,elem),0,""},
    {"length",T_INT,offsetof(SeqList,length),0,""},
    {"size",T_INT,offsetof(SeqList,size),0,""},
    {NULL}
};
static PyObject* InitList(SeqList* self, PyObject* args)
{
    int size;
    if (PyArg_ParseTuple(args, "i", &size) < 0)
    {
        Py_RETURN_FALSE;
    }
    else
    {
        self->elem = (ElemType*)PyMem_Calloc(size, sizeof(ElemType));
        if (self->elem == NULL)
        {
            Py_RETURN_FALSE;
        }
        else
        {
            self->size = size;
            self->length = 0;
            Py_RETURN_TRUE;
        }
    }
}
static PyObject* DestroyList(SeqList* self, PyObject* args)
{
    PyMem_FREE(self->elem);
    self->elem = NULL;
    self->length = 0;
    self->size = 0;
    Py_RETURN_TRUE;
}


static PyObject* ClearList(SeqList* self, PyObject* args)
{
    for (int i = 0; i < self->length; i++)
    {
        self->elem[i] = NULL;
    }
    self->length = 0;
    Py_RETURN_TRUE;
}
static PyObject* ListEmpty(SeqList* self, PyObject* args)
{
    if (self->length == 0)
    {
        Py_RETURN_TRUE;
    }
    else
    {
        Py_RETURN_FALSE;
    }
}
static PyObject* ListLength(SeqList* self, PyObject* args)
{
    PyObject* obj = Py_BuildValue("i", self->length);
    Py_INCREF(obj);
    return obj;
}
static PyObject* GetElem(SeqList* self, PyObject* args)
{
    int index;
    PyObject* result;
    if (PyArg_ParseTuple(args, "i", &index) < 0)
    {
        PyErr_SetString(PyExc_Exception, "Args parsed failure!");
        Py_RETURN_NONE;
    }
    else
    {
        if (index<0 || index>self->length)
        {
            Py_RETURN_NONE;
        }
        else
        {
            result = self->elem[index];
            Py_XINCREF(result);
            return result;
        }
    }
}
static PyObject* ListInsert(SeqList* self, PyObject* args)
{
    int index;
    PyObject* elem;
    if (PyArg_ParseTuple(args, "iO", &index, &elem) < 0)
    {
        PyErr_SetString(PyExc_Exception, "Args parsed failure!");
        Py_RETURN_FALSE;
    }
    else
    {
        if (index<0 || index>self->length)
        {
            Py_RETURN_FALSE;
        }
        else
        {
            for (int i = self->length; i >= index; i--)
            {
                self->elem[i + 1] = self->elem[i];
            }
            Py_XINCREF(elem);
            self->elem[index] = elem;
            self->length++;
            Py_RETURN_TRUE;
        }
    }
}
static PyObject* ListDelete(SeqList* self, PyObject* args)
{
    int index;
    if (PyArg_ParseTuple(args, "i", &index) < 0)
    {
        PyErr_SetString(PyExc_Exception, "Args parsed failure!");
        Py_RETURN_FALSE;
    }
    else
    {
        for (int i = index; i < self->length; i++)
        {
            self->elem[i] = self->elem[i + 1];
        }
        self->elem[self->length] = NULL;
        self->length--;
        Py_RETURN_TRUE;
    }
}
static PyObject* TraverseList(SeqList* self, PyObject* args)
{
    int i = 0;
    while (i < self->length)
    {
        PyObject_Print((PyObject*)self->elem[i], stdout, 0);
        i++;
    }
    printf("\n");
    Py_RETURN_NONE;
}
static PyMethodDef SeqList_methods[] = {
    {"init_list",InitList,METH_VARARGS,""},
    {"destroy_list",DestroyList,METH_VARARGS,""},
    {"clear_list",ClearList,METH_VARARGS,""},
    {"list_empty",ListEmpty,METH_VARARGS,""},
    {"list_length",ListLength,METH_VARARGS,""},
    {"get_elem",GetElem,METH_VARARGS,""},
    {"list_insert",ListInsert,METH_VARARGS,""},
    {"list_delete",ListDelete,METH_VARARGS,""},
    {"traverse_list",TraverseList,METH_VARARGS,""},
    {NULL}
};
static PyTypeObject SeqListObject = {
    PyVarObject_HEAD_INIT(NULL,0)
    .tp_name = "SequentialList.SeqList",
    .tp_new = SeqList_new,
    .tp_init = (initproc)SeqList_init,
    .tp_dealloc = (destructor)SeqList_destroy,
    .tp_basicsize = sizeof(SeqList),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_members = SeqList_members,
    .tp_methods = SeqList_methods
};
#endif // !
