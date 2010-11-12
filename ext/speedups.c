/**
 * (C) 2010 Brandon Gilmore <brandon@mg2.org>
 * See LICENSE for details
 */
 
#include "Python.h"
#include "byteorder.h"

#include <stdint.h>


PyDoc_STRVAR(read_string_docstr, "decodes a unicode string from an input stream");
PyObject * read_string(PyObject *self, PyObject *args)
{
	PyObject *stream, *read, *buffer;
	uint16_t remaining;

	if (! PyArg_UnpackTuple(args, "read_string", 1, 1, &stream))
		return NULL;

	read = PyObject_GetAttrString(stream, "read");
	if (! PyCallable_Check(read)) {
		PyErr_SetString(PyExc_RuntimeError, "the stream argument to read_string must have a 'read' method");
		return NULL;
	}

	/* first, read 2 bytes to determine chunk length */
	buffer = PyObject_CallFunction(read, "i", 2);
	if (PyString_Size(buffer) != 2) {
		Py_XDECREF(buffer);
		PyErr_SetString(PyExc_EOFError, "encountered unexpected end of stream");
		return NULL;
	}

	return buffer;
}


/**
 * module initialization
 */

static PyMethodDef speedups_methods[] = {
	{"read_string", read_string, METH_VARARGS, read_string_docstr},
	{NULL, NULL},
};

PyDoc_STRVAR(module_doc, "native codec implementations");
PyMODINIT_FUNC init_speedups(void)
{
	Py_InitModule3("_speedups", speedups_methods, module_doc);
}

/* vim:set noexpandtab shiftwidth=4 tabstop=4 textwidth=118 */

