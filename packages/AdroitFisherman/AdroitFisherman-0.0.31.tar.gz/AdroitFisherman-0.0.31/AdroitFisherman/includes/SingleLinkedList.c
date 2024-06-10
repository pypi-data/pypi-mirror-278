#define PY_SIZE_T_CLEAN
#include <python.h>
#include <structmember.h>
#include "SingleLinkedList.h"
static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name="SingleLinkedList",
    .m_size = -1
};
PyMODINIT_FUNC PyInit_SingleLinkedList()
{
    PyObject* m;
    if (PyType_Ready(&LNodeObject)<0)
    {
        return NULL;
    }
    if (PyType_Ready(&SingleLinkedListObject)<0)
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
    Py_INCREF(&SingleLinkedListObject);
    if (PyModule_AddObject(m,"List",(PyObject*)&SingleLinkedListObject)<0)
    {
        PyErr_SetString(PyExc_Exception, "list object added failure!");
        Py_DECREF(&SingleLinkedListObject);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}