/**
 * (C) 2010 Brandon Gilmore <brandon@mg2.org>
 * See LICENSE for details
 */
 
#include "Python.h"
#include "byteorder.h"

PyDoc_STRVAR(py_read_string_docstr, "deserializes a unicode string from a Hessian input stream");
PyObject * py_read_string(PyObject *self, PyObject *args)
{
	PyObject *stream, *shim, *result;
	PyObject *read   = NULL,
			 *buffer = NULL,
			 *excess = NULL,
			 *chunk  = NULL,
			 *chunks = NULL;
	Py_ssize_t consumed;
	uint16_t remaining;

	if (! PyArg_UnpackTuple(args, "read_string", 1, 1, &stream))
		return NULL;

	read = PyObject_GetAttrString(stream, "read");
	if (! PyCallable_Check(read)) {
		PyErr_SetString(PyExc_RuntimeError, "the stream argument to read_string must have a 'read' method");
		return NULL;
	}

	/* we need the first two bytes to determine overall character count (NOT byte count) */
	buffer = PyObject_CallFunction(read, "i", 2);

	/* this is our first chance to make sure stream.read returns raw strs */
	if (! PyString_Check(buffer)) {
		PyErr_SetString(PyExc_TypeError, "the stream argument to read_string must return str objects");
		goto err;
	}

	if (PyString_Size(buffer) != 2) {
		PyErr_SetString(PyExc_EOFError, "encountered unexpected end of stream");
		goto err;
	}

	remaining = SWAB16(*((uint16_t *) PyString_AS_STRING(buffer)));
	Py_DECREF(buffer);

	/* trapdoor */
	if (remaining == 0) {
		return Py_BuildValue("u", "");
	}

	chunks = PyList_New(0);

	while (remaining > 0) {
		/* read minimum viable chunk */
		buffer = PyObject_CallFunction(read, "i", remaining);
		if (PyString_Size(buffer) != remaining) {
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

		chunk = PyUnicode_DecodeUTF8Stateful(PyString_AS_STRING(buffer), remaining, "strict", &consumed);
		if (chunk == NULL)
			goto err;

		if (PyList_Append(chunks, chunk) != 0)
			goto err;

		/* check if we need to stash leftover bytes for the next round */
		if (consumed < remaining) {
			excess = PyString_FromStringAndSize(PyString_AS_STRING(buffer) + consumed, remaining - consumed);
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

