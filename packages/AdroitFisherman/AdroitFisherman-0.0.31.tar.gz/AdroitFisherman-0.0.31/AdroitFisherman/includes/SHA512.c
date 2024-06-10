#include <Python.h>
#include <structmember.h>
#include "SHA512.h"
static PyModuleDef SHA_module = {
	PyModuleDef_HEAD_INIT,
	.m_name = "SHAUtility",
	.m_size = -1
};
PyMODINIT_FUNC PyInit_SHAUtility()
{
	PyObject* m;
	if (PyType_Ready(&SHABlock_object) < 0)
	{
		return NULL;
	}
	m = PyModule_Create(&SHA_module);
	if (m == NULL)
	{
		return NULL;
	}
	Py_XINCREF(&SHABlock_object);
	if (PyModule_AddObject(m, "SHABlock", (PyObject*)&SHABlock_object) < 0)
	{
		Py_DECREF(&SHABlock_object);
		Py_DECREF(m);
		return NULL;
	}
	return m;
}