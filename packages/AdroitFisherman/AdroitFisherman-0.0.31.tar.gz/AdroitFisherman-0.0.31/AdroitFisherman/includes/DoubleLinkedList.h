#ifndef DOUBLELINKEDLIST_CHAR_H_INCLUDED
#define DOUBLELINKEDLIST_CHAR_H_INCLUDED
#define TRUE 1
#define FALSE -1
typedef PyObject* ElemType;
typedef struct Node
{
    PyObject_HEAD
    ElemType elem;
    struct Node* prior;
    struct Node* next;
}LNode;
typedef struct {
    PyObject_HEAD
    LNode* instance;
}List;
static void LNode_destroy(LNode* self)
{
    Py_DECREF(self->elem);
    Py_DECREF(self->next);
    Py_DECREF(self->prior);
    Py_TYPE(self)->tp_free(self);
}
static void List_destroy(List* self)
{
    Py_DECREF(self->instance);
    Py_TYPE(self)->tp_free(self);
}
static PyObject* LNode_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    LNode* self;
    self = (LNode*)type->tp_alloc(type, 0);
    if (self == NULL)
    {
        PyErr_SetString(PyExc_Exception, "list node object created failure!");
        return NULL;
    }
    else
    {
        self->elem = NULL;
        self->next = NULL;
        self->prior = NULL;
        Py_INCREF(self);
        return (PyObject*)self;
    }
}
static PyObject* List_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    List* self;
    self = (List*)type->tp_alloc(type, 0);
    if (self == NULL)
    {
        PyErr_SetString(PyExc_Exception, "list object created failure!");
        return NULL;
    }
    else {
        self->instance = NULL;
        Py_INCREF(self);
        return (PyObject*)self;
    }
}
static int LNode_init(LNode* self, PyObject* args, PyObject* kwds)
{
    return 0;
}
static int List_init(List* self, PyObject* args, PyObject* kwds)
{
    return 0;
}
static PyMemberDef LNode_members[] = {
    {"elem",T_OBJECT,offsetof(LNode,elem),0,""},
    {"next",T_OBJECT,offsetof(LNode,next),0,""},
    {"prior",T_OBJECT,offsetof(LNode,prior),0,""},
    {NULL}
};
static PyMemberDef List_members[] = {
    {"instance",T_OBJECT,offsetof(List,instance),0,""},
    {NULL}
};
static PyObject* InitList(List*self,PyObject*args)
{
    self->instance = (LNode*)PyMem_MALLOC(sizeof(LNode));
    if (self->instance!=NULL)
    {
        self->instance->next = NULL;
        self->instance->prior = NULL;
        Py_RETURN_TRUE;
    }
    else
    {
        Py_RETURN_FALSE;
    }
}
static PyObject* DestroyList(List*self,PyObject*args)
{
    LNode* temp = self->instance;
    while (temp != NULL)
    {
        temp = self->instance;
        self->instance = temp->next;
        PyMem_FREE(temp);
        temp = NULL;
    }
    Py_RETURN_TRUE;
}
static PyObject* ClearList(List* self, PyObject* args) {
    LNode* temp = self->instance;
    while (self->instance->next != NULL)
    {
        temp = self->instance->next;
        self->instance->next = temp->next;
        PyMem_FREE(temp);
        temp = NULL;
    }
    Py_RETURN_TRUE;
}
static PyObject* ListEmpty(List* self, PyObject* args)
{
    LNode* temp = self->instance;
    if (temp->next != NULL)
    {
        Py_RETURN_FALSE;
    }
    else
    {
        Py_RETURN_TRUE;
    }
}
static PyObject* ListLength(List* self, PyObject* args)
{
    LNode* temp = self->instance;
    int counter = 0;
    while (temp->next != NULL)
    {
        counter++;
        temp = temp->next;
    }
    PyObject* result = Py_BuildValue("i", counter);
    Py_INCREF(result);
    return result;
}
static PyObject* GetElem(List* self, PyObject* args)
{
    int index;
    PyObject* result;
    if (PyArg_ParseTuple(args, "i", &index) < 0)
    {
        PyErr_SetString(PyExc_Exception, "Args parsed failure!");
        Py_RETURN_NONE;
    }
    else {
        if (index < 0 || index >= ListLength(self, NULL))
        {
            Py_RETURN_NONE;
        }
        else
        {
            LNode* temp = self->instance->next;
            int counter = 0;
            while (counter < index)
            {
                temp = temp->next;
                counter++;
            }
            result = temp->elem;
            Py_XINCREF(result);
            return result;
        }
    }
}
static PyObject* AddFirst(List* self, PyObject* args)
{
    PyObject* elem;
    if (PyArg_ParseTuple(args, "O", &elem) < 0)
    {
        Py_RETURN_FALSE;
    }
    LNode* summon = (LNode*)PyMem_MALLOC(sizeof(LNode));
    if (summon == NULL)
    {
        Py_RETURN_FALSE;
    }
    else
    {
        Py_XINCREF(elem);
        summon->elem = elem;
        summon->next = self->instance->next;
        self->instance->next = summon;
        summon->prior = self->instance;
        if (summon->next!=NULL)
        {
            summon->next->prior = summon;
        }
        Py_RETURN_TRUE;
    }
}static PyObject* AddAfter(List* self, PyObject* args)
{
    PyObject* elem;
    if (PyArg_ParseTuple(args, "O", &elem) < 0)
    {
        Py_RETURN_FALSE;
    }
    LNode* summon = (LNode*)PyMem_MALLOC(sizeof(LNode));
    if (summon == NULL)
    {
        Py_RETURN_FALSE;
    }
    else
    {
        LNode* temp = self->instance;
        while (temp->next != NULL)
        {
            temp = temp->next;
        }
        Py_XINCREF(elem);
        summon->elem = elem;
        summon->next = temp->next;
        summon->prior = temp;
        temp->next = summon;
        Py_RETURN_TRUE;
    }
}
static PyObject* ListInsert(List* self, PyObject* args)
{
    int index;
    PyObject* elem;
    if (PyArg_ParseTuple(args, "iO", &index, &elem) < 0)
    {
        PyErr_SetString(PyExc_Exception, "Args parsed failure!");
        Py_RETURN_FALSE;
    }
    else if (index==0)
    {
        PyTupleObject* arguments = Py_BuildValue("(O)",elem);
        Py_INCREF(arguments);
        return AddFirst(self,arguments);
    }
    else
    {
        LNode* p = self->instance;
        LNode* summon = (LNode*)PyMem_MALLOC(sizeof(LNode));
        int i = 0;
        while (i < index)
        {
            p = p->next;
            i++;
        }
        summon = (LNode*)malloc(sizeof(LNode));
        if (summon==NULL)
        {
            Py_RETURN_FALSE;
        }
        summon->elem = elem;
        summon->next = p->next;
        summon->prior = p;
        p->next = summon;
        if (summon->next != NULL)
        {
            summon->next->prior = summon;
        }
        Py_RETURN_TRUE;
    }
}
static PyObject* ListDelete(List* self, PyObject* args)
{
    int index;
    if (PyArg_ParseTuple(args, "i", &index) < 0)
    {
        PyErr_SetString(PyExc_Exception, "Args parsed failure!");
        Py_RETURN_FALSE;
    }
    else
    {
        if (index < 0 || index >= ListLength(self, NULL))
        {
            Py_RETURN_FALSE;
        }
        else if (index==ListLength(self,NULL)-1)
        {
            LNode* p = self->instance, * del;
            int i = 0;
            while (i < index)
            {
                p = p->next;
                i++;
            }
            del = p->next;
            del->prior->next = NULL;
            del->prior = NULL;
            free(del);
            del = NULL;
            Py_RETURN_TRUE;
        }
        else
        {
            LNode* temp = self->instance;
            LNode* del;
            int counter = 0;
            while (counter < index)
            {
                temp = temp->next;
                counter++;
            }
            del = temp->next;
            del->prior->next = del->next;
            del->next->prior = del->prior;
            PyMem_FREE(del);
            del = NULL;
            Py_RETURN_TRUE;
        }
    }
}
static PyObject* TraverseList(List*self,PyObject*args)
{
    LNode* p = self->instance->next;
    while (p != NULL)
    {
        PyObject_Print(p->elem,stdout,0);
        p = p->next;
    }
    printf("\n");
    Py_RETURN_NONE;
}
static PyObject* TraverseListByReverseOrder(List* self, PyObject* args)
{
    if (self->instance->next==NULL)
    {
        printf("\n");
    }
    else
    {
        LNode* p = self->instance->next;
        while (p->next != NULL)
        {
            p = p->next;
        }
        while (p->prior != NULL)
        {
            PyObject_Print(p->elem, stdout, 0);
            p = p->prior;
        }
        printf("\n");
    }
    Py_RETURN_NONE;
}
static PyMethodDef List_methods[] = {
    {"init_list",InitList,METH_VARARGS,""},
    {"destroy_list",DestroyList,METH_VARARGS,""},
    {"clear_list",ClearList,METH_VARARGS,""},
    {"list_empty",ListEmpty,METH_VARARGS,""},
    {"list_length",ListLength,METH_VARARGS,""},
    {"get_elem",GetElem,METH_VARARGS,""},
    {"add_first",AddFirst,METH_VARARGS,""},
    {"add_after",AddAfter,METH_VARARGS,""},
    {"list_insert",ListInsert,METH_VARARGS,""},
    {"list_delete",ListDelete,METH_VARARGS,""},
    {"traverse_list",TraverseList,METH_VARARGS,""},
    {"reverse_list",TraverseListByReverseOrder,METH_VARARGS,""},
    {NULL}
};
static PyTypeObject LNodeObject = {
    PyVarObject_HEAD_INIT(NULL,0)
    .tp_name = "DoubleLinkedList.LNode",
    .tp_new = LNode_new,
    .tp_init = (initproc)LNode_init,
    .tp_dealloc = (destructor)LNode_destroy,
    .tp_basicsize = sizeof(LNode),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_members = LNode_members
};
static PyTypeObject DoubleLinkedListObject = {
    PyVarObject_HEAD_INIT(NULL,0)
    .tp_name = "DoubleLinkedList.List",
    .tp_new = List_new,
    .tp_init = (initproc)List_init,
    .tp_dealloc = (destructor)List_destroy,
    .tp_basicsize = sizeof(List),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_BASETYPE | Py_TPFLAGS_DEFAULT,
    .tp_members = List_members,
    .tp_methods = List_methods
};
#endif // DOUBLELINKEDLIST_CHAR_H_INCLUDED