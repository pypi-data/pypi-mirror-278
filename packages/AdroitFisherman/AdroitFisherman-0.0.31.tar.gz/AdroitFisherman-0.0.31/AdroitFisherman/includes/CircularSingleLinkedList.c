#define PY_SIZE_T_CLEAN
#include <python.h>
#include <structmember.h>
#include "CircularSingleLinkedList.h"
static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name="CircularSingleLinkedList",
    .m_size = -1
};
PyMODINIT_FUNC PyInit_CircularSingleLinkedList()
{
    PyObject* m;
    if (PyType_Ready(&CircularSingleLinkedListObject)<0)
    {
        return NULL;
    }
    m = PyModule_Create(&module);
    if (m==NULL)
    {
        return NULL;
    }
    Py_INCREF(&CircularSingleLinkedListObject);
    if (PyModule_AddObject(m,"SingleLinkedList",(PyObject*)&CircularSingleLinkedListObject)<0)
    {
        PyErr_SetString(PyExc_Exception, "list object added failure!");
        Py_DECREF(&CircularSingleLinkedListObject);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}