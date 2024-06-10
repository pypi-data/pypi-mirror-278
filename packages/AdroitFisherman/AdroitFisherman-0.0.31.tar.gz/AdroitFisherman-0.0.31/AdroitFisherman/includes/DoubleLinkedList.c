#define PY_SIZE_T_CLEAN
#include <python.h>
#include <structmember.h>
#include "DoubleLinkedList.h"
static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name="DoubleLinkedList",
    .m_size = -1
};
PyMODINIT_FUNC PyInit_DoubleLinkedList()
{
    PyObject* m;
    if (PyType_Ready(&LNodeObject)<0)
    {
        return NULL;
    }
    if (PyType_Ready(&DoubleLinkedListObject)<0)
    {
        return NULL;
    }
    m = PyModule_Create(&module);
    if (m==NULL)
    {
        return NULL;
    }
    Py_INCREF(&LNodeObject);
    if (PyModule_AddObject(m,"LNode",(PyObject*)&LNodeObject)<0)
    {
        PyErr_SetString(PyExc_Exception, "list object added failure!");
        Py_DECREF(&LNodeObject);
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&DoubleLinkedListObject);
    if (PyModule_AddObject(m,"List",(PyObject*)&DoubleLinkedListObject)<0)
    {
        PyErr_SetString(PyExc_Exception, "list object added failure!");
        Py_DECREF(&DoubleLinkedListObject);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}