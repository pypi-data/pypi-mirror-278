#define PY_SIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include "LinkedStack.h"
static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "LinkedStack",
    .m_size = -1
};
PyMODINIT_FUNC PyInit_LinkedStack()
{
    PyObject* m;
    if (PyType_Ready(&LinkedStack_object) < 0)
    {
        return NULL;
    }
    m = PyModule_Create(&module);
    if (m == NULL)
    {
        return NULL;
    }
    Py_INCREF(&LinkedStack_object);
    if (PyModule_AddObject(m, "Stack", (PyObject*)&LinkedStack_object) < 0)
    {
        PyErr_SetString(PyExc_Exception, "stack object added failure!");
        Py_DECREF(&LinkedStack_object);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}