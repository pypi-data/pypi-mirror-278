#define PY_SIZE_T_CLEAN
#include <python.h>
#include <structmember.h>
#include "SeqList.h"
static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name="SequentialList",
    .m_size = -1
};
PyMODINIT_FUNC PyInit_SequentialList()
{
    PyObject* m;
    if (PyType_Ready(&SeqListObject)<0)
    {
        return NULL;
    }
    m = PyModule_Create(&module);
    if (m==NULL)
    {
        return NULL;
    }
    Py_INCREF(&SeqListObject);
    if (PyModule_AddObject(m,"SeqList",(PyObject*)&SeqListObject)<0)
    {
        PyErr_SetString(PyExc_Exception, "list object added failure!");
        Py_DECREF(&SeqListObject);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}