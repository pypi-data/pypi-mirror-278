#ifndef SINGLELINKEDLISTWITHOUTHEADNODE_H_INCLUDED
#define SINGLELINKEDLISTWITHOUTHEADNODE_H_INCLUDED
typedef PyObject* ElemType;
typedef struct Node
{
    PyObject_HEAD
        ElemType elem;
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
    {NULL}
};
static PyMemberDef List_members[] = {
    {"instance",T_OBJECT,offsetof(List,instance),0,""},
    {NULL}
};
static PyObject* InitList(List* self, PyObject* args)
{
    self->instance = NULL;
    Py_RETURN_TRUE;
}
static PyObject* DestroyList(List* self, PyObject* args)
{
    LNode* p = self->instance;
    while (p != NULL)
    {
        p = self->instance;
        self->instance = p->next;
        PyMem_FREE(p);
        p = NULL;
    }
    self->instance = NULL;
    Py_RETURN_TRUE;
}
static PyObject* ClearList(List* self, PyObject* args)
{
    LNode* p = self->instance;
    while (p != NULL)
    {
        p = self->instance;
        self->instance = p->next;
        PyMem_FREE(p);
        p = NULL;
    }
    self->instance = NULL;
    Py_RETURN_TRUE;
}
static PyObject* ListEmpty(List* self, PyObject* args)
{
    if (self->instance == NULL)
    {
        Py_RETURN_TRUE;
    }
    else {
        Py_RETURN_FALSE;
    }
}
static PyObject* ListLength(List* self, PyObject* args)
{
    int i = 0;
    LNode* p = self->instance;
    while (p != NULL)
    {
        p = p->next;
        i++;
    }
    PyObject* result = Py_BuildValue("i", i);
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
    else
    {
        if (index < 0 || index >= ListLength(self, args))
        {
            Py_RETURN_NONE;
        }
        else
        {
            LNode* temp = self->instance;
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
    else
    {
        LNode* summon = (LNode*)PyMem_MALLOC(sizeof(LNode));
        if (summon == NULL)
        {
            Py_RETURN_FALSE;
        }
        else
        {
            Py_XINCREF(elem);
            summon->elem = elem;
            summon->next = self->instance;
            self->instance = summon;
            Py_RETURN_TRUE;
        }
    }
}
static PyObject* AddAfter(List* self, PyObject* args)
{
    PyObject* elem;
    if (PyArg_ParseTuple(args, "O", &elem) < 0)
    {
        Py_RETURN_FALSE;
    }
    else
    {
        LNode* summon = (LNode*)PyMem_MALLOC(sizeof(LNode));
        LNode* p = self->instance;
        if (summon == NULL)
        {
            Py_RETURN_FALSE;
        }
        else
        {
            Py_XINCREF(elem);
            if (self->instance==NULL)
            {
                summon->elem=elem;
                summon->next=NULL;
                self->instance = summon;
                Py_RETURN_TRUE;
            }
            while (p->next != NULL)
            {
                p = p->next;
            }
            summon->elem = elem;
            summon->next = p->next;
            p->next = summon;
            Py_RETURN_TRUE;
        }
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
    else
    {
        if (index<0 || index>ListLength(self, NULL))
        {
            Py_RETURN_FALSE;
        }
        else
        {
            int counter = 0;
            if (index == 0)
            {
                LNode* summon = (LNode*)PyMem_MALLOC(sizeof(LNode));
                if (summon == NULL)
                {
                    Py_RETURN_FALSE;
                }
                else
                {
                    Py_XINCREF(elem);
                    summon->elem = elem;
                    summon->next = self->instance;
                    self->instance = summon;
                    Py_RETURN_TRUE;
                }
            }
            LNode* p = self->instance;
            LNode* summon = (LNode*)PyMem_MALLOC(sizeof(LNode));
            if (summon == NULL)
            {
                Py_RETURN_FALSE;
            }
            else {
                Py_XINCREF(elem);
                summon->elem = elem;
                int counter = 1;
                while (counter < index)
                {
                    p = p->next;
                    counter++;
                }
                summon->next = p->next;
                p->next = summon;
                Py_RETURN_TRUE;
            }
        }
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
        else
        {
            if (index == 0)
            {
                LNode* temp = self->instance;
                self->instance = temp->next;
                PyMem_FREE(temp);
                temp = NULL;
                Py_RETURN_TRUE;
            }
            LNode* p = self->instance, * del;
            int i = 1;
            while (i < index)
            {
                p = p->next;
                i++;
            }
            del = p->next;
            p->next = del->next;
            PyMem_FREE(del);
            del = NULL;
            Py_RETURN_TRUE;
        }
    }
}
static PyObject* TraverseList(List*self,PyObject*args)
{
    LNode *p=self->instance;
    while(p!=NULL)
    {
        PyObject_Print(p->elem, stdout, 0);
        p=p->next;
    }
    printf("\n");
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
    {NULL}
};
static PyTypeObject LNodeObject = {
    PyVarObject_HEAD_INIT(NULL,0)
    .tp_name = "SingleLinkedListWithoutHeadNode.LNode",
    .tp_new = LNode_new,
    .tp_init = (initproc)LNode_init,
    .tp_dealloc = (destructor)LNode_destroy,
    .tp_basicsize = sizeof(LNode),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_members = LNode_members
};
static PyTypeObject SingleLinkedListWithoutHeadNodeObject = {
    PyVarObject_HEAD_INIT(NULL,0)
    .tp_name = "SingleLinkedListWithoutHeadNode.List",
    .tp_new = List_new,
    .tp_init = (initproc)List_init,
    .tp_dealloc = (destructor)List_destroy,
    .tp_basicsize = sizeof(List),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_BASETYPE | Py_TPFLAGS_DEFAULT,
    .tp_members = List_members,
    .tp_methods = List_methods
};
#endif // SINGLELINKEDLISTWITHOUTHEADNODE_H_INCLUDED