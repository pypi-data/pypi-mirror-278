#include <Python.h>
#include <structmember.h>
#include "Base64Util.h"
static PyModuleDef Base64_module = {
	PyModuleDef_HEAD_INIT,
	.m_name = "Base64Utility",
	.m_size = -1
};
PyMODINIT_FUNC PyInit_Base64Utility()
{
	PyObject* m;
	if (PyType_Ready(&Base64block_object)<0)
	{
		return NULL;
	}
	m = PyModule_Create(&Base64_module);
	if (m==NULL)
	{
		return NULL;
	}
	Py_XINCREF(&Base64block_object);
	if (PyModule_AddObject(m,"Base64Block",(PyObject*) & Base64block_object)<0)
	{
		Py_DECREF(&Base64block_object);
		Py_DECREF(m);
		return NULL;
	}
	return m;
}