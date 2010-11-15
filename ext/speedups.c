/**
 * (C) 2010 Brandon Gilmore <brandon@mg2.org>
 * See LICENSE for details
 */
 
#include "Python.h"

PyDoc_STRVAR(py_read_string_docstr, "deserializes a unicode string from a Hessian input stream");
PyObject * py_read_string(PyObject *self, PyObject *args)
{
	PyObject *stream, *count;   /* arguments */
	PyObject *shim, *result;    /* safe refs */
	PyObject *read   = NULL,
	         *buffer = NULL,
	         *excess = NULL,
	         *chunk  = NULL,
	         *chunks = NULL;
	Py_ssize_t consumed;
	long remaining, needed;

	if (! PyArg_UnpackTuple(args, "read_string", 2, 2, &stream, &count))
		return NULL;

	remaining = PyInt_AsLong(count);
	if ((remaining == -1) && (PyErr_Occurred()))
		return NULL;

	/* trap door */
	if (remaining <= 0)
		return Py_BuildValue("u", "");

	read = PyObject_GetAttrString(stream, "read");
	if (! PyCallable_Check(read))
		goto err;

	chunks = PyList_New(0);
	if (chunks == NULL)
		goto err;

	while (remaining > 0) {
		if (excess != NULL)
			needed = remaining - PyString_GET_SIZE(excess);
		else
			needed = remaining;

		/* read minimum viable chunk */
		buffer = PyObject_CallFunction(read, "i", needed);
		if (PyString_Size(buffer) != needed) {
			PyErr_SetString(PyExc_EOFError, "encountered unexpected end of stream");
			goto err;
		}

		/* prepend overflow bytes from previous rounds if necessary */
		if (excess != NULL) {
			PyString_ConcatAndDel(&excess, buffer);
			if (excess == NULL)
				goto err;

			buffer = excess;
			excess = NULL;
		}

		/* decode the buffer and store the resulting chunk */
		chunk = PyUnicode_DecodeUTF8Stateful(PyString_AS_STRING(buffer), remaining, "strict", &consumed);
		if (chunk == NULL)
			goto err;

		if (PyList_Append(chunks, chunk) != 0)
			goto err;

		/* check if we need to stash leftover bytes for the next round */
		if (consumed < PyString_GET_SIZE(buffer)) {
			excess = PyString_FromStringAndSize(PyString_AS_STRING(buffer) + consumed, PyString_GET_SIZE(buffer) - consumed);
		}

		remaining -= PyUnicode_GET_SIZE(chunk);

		Py_DECREF(chunk);
		Py_DECREF(buffer);
	}


	Py_DECREF(read);

	shim   = PyUnicode_FromWideChar((const wchar_t *) "", 0);
	result = PyUnicode_Join(shim, chunks);

	Py_DECREF(shim);
	Py_DECREF(chunks);

	return result;

err:
	Py_XDECREF(read);
	Py_XDECREF(buffer);
	Py_XDECREF(excess);
	Py_XDECREF(chunk);
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
	Py_InitModule3("_speedups", speedups_methods, module_doc);
}

/* vim:set noexpandtab shiftwidth=4 tabstop=4 textwidth=118 */

