/**
 * (C) 2010 Brandon Gilmore <brandon@mg2.org>
 * See LICENSE for details
 */
 
#include "Python.h"

static PyObject *PyUnicode_NIL;


/**
 * _speedups.read_string(<obj:stream>, <int:count>)
 */

PyDoc_STRVAR(py_read_string_docstr, "deserializes a unicode string from a Hessian input stream");
PyObject * py_read_string(PyObject *self, PyObject *args)
{
	PyObject *stream, *count;   /* arguments */
	PyObject *read   = NULL,
	         *buffer = NULL,
	         *excess = NULL,
	         *chunk  = NULL,
	         *chunks = NULL,
	         *result = NULL;
	Py_ssize_t consumed, remaining;

	if (! PyArg_UnpackTuple(args, "read_string", 2, 2, &stream, &count))
		return NULL;

	remaining = (long) PyInt_AsLong(count);
	if ((remaining == -1) && (PyErr_Occurred()))
		return NULL;

	/* trap door */
	if (remaining <= 0)
		return PyUnicode_NIL;

	read = PyObject_GetAttrString(stream, "read");
	if (! PyCallable_Check(read))
		goto err;

	chunks = PyList_New(0);
	if (chunks == NULL)
		goto err;

	while (remaining > 0) {
		/* read minimum viable chunk */
		buffer = PyObject_CallFunction(read, "i", remaining);
		if (PyString_Size(buffer) != remaining) {
			PyErr_SetString(PyExc_EOFError, "encountered unexpected end of stream");
			goto err;
		}

		/* pull in excess bytes from the last iteration */
		if (excess != NULL) {
			PyString_ConcatAndDel(&excess, buffer);
			if (excess == NULL)
				goto err;

			buffer = excess;
			excess = NULL;
		}

		/* decode the buffer and store the result chunk */
		chunk = PyUnicode_DecodeUTF8Stateful(PyString_AS_STRING(buffer), PyString_GET_SIZE(buffer), "strict", &consumed);
		if (chunk == NULL)
			goto err;

		if (PyList_Append(chunks, chunk) != 0)
			goto err;

		/* stash any remaining undecoded bytes for next iteration */
		if (consumed < PyString_GET_SIZE(buffer)) {
			excess = PyString_FromStringAndSize(PyString_AS_STRING(buffer) + consumed, PyString_GET_SIZE(buffer) - consumed);
			if (excess == NULL)
				goto err;
		}

		remaining -= PyUnicode_GET_SIZE(chunk);
		Py_DECREF(buffer);
		Py_DECREF(chunk);
	}

	Py_DECREF(read);

	result = PyUnicode_Join(PyUnicode_NIL, chunks);
	if (result == NULL)
		goto err;

	Py_DECREF(chunks);

	return result;

err:
	Py_XDECREF(read);
//	Py_XDECREF(buffer); /* unsafe to collect? WHY? */
	Py_XDECREF(excess);
	Py_XDECREF(chunks);
	return NULL;
}


/**
 * module initialization
 */

static PyMethodDef speedups_methods[] = {
	{"read_string", py_read_string, METH_VARARGS, py_read_string_docstr},
	{NULL, NULL},
};

PyDoc_STRVAR(module_doc, "native codec implementations");
PyMODINIT_FUNC init_speedups(void)
{
	PyUnicode_NIL = PyUnicode_FromWideChar((wchar_t *) "", 0);
	if (PyUnicode_NIL == NULL)
		return;

	Py_InitModule3("_speedups", speedups_methods, module_doc);
}

/* vim:set noexpandtab shiftwidth=4 tabstop=4 textwidth=118 */

