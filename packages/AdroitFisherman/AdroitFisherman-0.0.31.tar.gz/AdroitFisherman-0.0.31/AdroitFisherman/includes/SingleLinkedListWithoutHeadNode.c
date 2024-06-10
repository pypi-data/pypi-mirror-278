#define PY_SIZE_T_CLEAN
#include <python.h>
#include <structmember.h>
#include "SingleLinkedListWithoutHeadNode.h"
static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name="SingleLinkedListWithoutHeadNode",
    .m_size = -1
};
PyMODINIT_FUNC PyInit_SingleLinkedListWithoutHeadNode()
{
    PyObject* m;
    if (PyType_Ready(&SingleLinkedListWithoutHeadNodeObject)<0)
    {
        return NULL;
    }
    m = PyModule_Create(&module);
    if (m==NULL)
    {
        return NULL;
    }
    Py_INCREF(&SingleLinkedListWithoutHeadNodeObject);
    if (PyModule_AddObject(m,"SingleLinkedList",(PyObject*)&SingleLinkedListWithoutHeadNodeObject)<0)
    {
        PyErr_SetString(PyExc_Exception, "list object added failure!");
        Py_DECREF(&SingleLinkedListWithoutHeadNodeObject);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}