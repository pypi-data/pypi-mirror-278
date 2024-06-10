// clang-format off
#include <Python.h>
// clang-format on
#include "emulator.h"
#include "memory.h"

static struct PyModuleDef fast_emulator;
static PyTypeObject FastEmulatorType;
static PyTypeObject FastEmulatorType;

typedef struct {
    PyObject_HEAD emulator_s *emulator;
} FastEmulatorObject;

static int FastEmulator_init(FastEmulatorObject *self, PyObject *args);
static void FastEmulator_dealloc(FastEmulatorObject *self);
static PyObject *FastEmulator_step(FastEmulatorObject *self,
                                   PyObject *Py_UNUSED(ignored));
static PyObject *FastEmulator_cycle(FastEmulatorObject *self,
                                    PyObject *Py_UNUSED(ignored));
static PyObject *FastEmulator_cycle_until_halt(FastEmulatorObject *self,
                                               PyObject *Py_UNUSED(ignored));
static PyObject *FastEmulator_dump(FastEmulatorObject *self,
                                   PyObject *Py_UNUSED(ignored));
static PyObject *_create_byte(PyObject *byte_class, int value);

PyMODINIT_FUNC PyInit_fast_emulator(void) {
    PyObject *m;
    if (PyType_Ready(&FastEmulatorType) < 0) {
        return NULL;
    }

    m = PyModule_Create(&fast_emulator);
    if (m == NULL) {
        return NULL;
    }

    Py_INCREF(&FastEmulatorType);
    if (PyModule_AddObject(m, "FastEmulator", (PyObject *)&FastEmulatorType) <
        0) {
        Py_DECREF(&FastEmulatorType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}

static struct PyModuleDef fast_emulator = {
    PyModuleDef_HEAD_INIT,
    .m_name = "fast_emulator",
    .m_size = -1,
};

static PyMethodDef FastEmulator_methods[] = {
    {"step", (PyCFunction)FastEmulator_step, METH_NOARGS, ""},
    {"cycle", (PyCFunction)FastEmulator_cycle, METH_NOARGS, ""},
    {"cycle_until_halt", (PyCFunction)FastEmulator_cycle_until_halt,
     METH_NOARGS, ""},
    {"dump", (PyCFunction)FastEmulator_dump, METH_NOARGS, ""},
    {NULL, NULL, METH_NOARGS, ""} /* Sentinel */
};

static PyTypeObject FastEmulatorType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "fast_emulator.FastEmulator",
    .tp_basicsize = sizeof(FastEmulatorObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)FastEmulator_init,
    .tp_dealloc = (destructor)FastEmulator_dealloc,
    .tp_methods = FastEmulator_methods,
};

static int FastEmulator_init(FastEmulatorObject *self, PyObject *args) {
    PyObject *byte_array = NULL;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &byte_array)) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a list of bytes.");
        return -1;
    }

    if (byte_array == NULL) {
        PyErr_SetString(PyExc_AttributeError, "Memory bytes is not set.");
        return -1;
    }

    memory_s *memory = create_memory();
    if (memory == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory.");
        return -1;
    }

    Py_ssize_t size = PyList_Size(byte_array);
    for (Py_ssize_t i = 0; i < size; i++) {
        PyObject *byte = PyList_GetItem(byte_array, i); // Borrowed reference

        if (byte == NULL) {
            PyErr_SetString(PyExc_TypeError, "List item is not a byte.");
            free_memory(memory);
            return -1;
        }

        PyObject *value_attr = PyObject_GetAttrString(byte, "value");
        if (value_attr == NULL) {
            PyErr_SetString(PyExc_AttributeError,
                            "Could not get value from byte object.");
            free_memory(memory);
            return -1;
        }

        if (!PyLong_Check(value_attr)) {
            PyErr_SetString(PyExc_TypeError,
                            "Value attribute is not an integer.");
            Py_DECREF(value_attr);
            free_memory(memory);
            return -1;
        }

        memory->memory[i] = (int)PyLong_AsLong(value_attr);
        Py_DECREF(value_attr);
    }

    emulator_s *emulator = create_emulator(memory);
    if (emulator == NULL) {
        PyErr_SetString(PyExc_MemoryError,
                        "Not enough memory to initialize emulator.");
        free_memory(memory);
        return -1;
    }

    self->emulator = emulator;
    return 0;
}

static void FastEmulator_dealloc(FastEmulatorObject *self) {
    if (self->emulator->control_unit->memory) {
        free_memory(self->emulator->control_unit->memory);
    }
    if (self->emulator) {
        free_emulator(self->emulator);
    }
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *FastEmulator_step(FastEmulatorObject *self,
                                   PyObject *Py_UNUSED(ignored)) {
    if (!self->emulator) {
        PyErr_SetString(PyExc_AttributeError,
                        "Emulator is not set. Init has failed.");
        return NULL;
    }

    self->emulator->step(self->emulator);

    Py_RETURN_NONE;
}

static PyObject *FastEmulator_cycle(FastEmulatorObject *self,
                                    PyObject *Py_UNUSED(ignored)) {
    if (!self->emulator) {
        PyErr_SetString(PyExc_AttributeError,
                        "Emulator is not set. Init has failed.");
        return NULL;
    }

    self->emulator->cycle(self->emulator);

    Py_RETURN_NONE;
}

static PyObject *FastEmulator_cycle_until_halt(FastEmulatorObject *self,
                                               PyObject *Py_UNUSED(ignored)) {
    if (!self->emulator) {
        PyErr_SetString(PyExc_AttributeError,
                        "Emulator is not set. Init has failed.");
        return NULL;
    }

    self->emulator->cycle_until_halt(self->emulator);

    Py_RETURN_NONE;
}

static PyObject *FastEmulator_dump(FastEmulatorObject *self,
                                   PyObject *Py_UNUSED(ignored)) {
    if (!self->emulator) {
        PyErr_SetString(PyExc_AttributeError,
                        "Emulator is not set. Init has failed.");
        return NULL;
    }

    state_s *state = self->emulator->dump(self->emulator);
    if (!state) {
        PyErr_SetString(PyExc_RuntimeError,
                        "Failed to dump the emulator state.");
        return NULL;
    }

    PyObject *module_name = PyUnicode_FromString("bytecorefast.state");
    if (!module_name) {
        free(state);
        return NULL;
    }

    PyObject *module = PyImport_Import(module_name);
    Py_DECREF(module_name);
    if (!module) {
        free(state);
        return NULL;
    }

    PyObject *state_class = PyObject_GetAttrString(module, "State");
    Py_DECREF(module);
    if (!state_class) {
        free(state);
        return NULL;
    }

    PyObject *from_raw_method = PyObject_GetAttrString(state_class, "from_raw");
    Py_DECREF(state_class);
    if (!from_raw_method || !PyCallable_Check(from_raw_method)) {
        if (from_raw_method) {
            Py_DECREF(from_raw_method);
        }
        free(state);
        PyErr_SetString(PyExc_AttributeError,
                        "State class has no from_raw method.");
        return NULL;
    }

    PyObject *byte_module_name = PyUnicode_FromString("bytecore.byte");
    if (!byte_module_name) {
        Py_DECREF(from_raw_method);
        free(state);
        return NULL;
    }

    PyObject *byte_module = PyImport_Import(byte_module_name);
    Py_DECREF(byte_module_name);
    if (!byte_module) {
        Py_DECREF(from_raw_method);
        free(state);
        return NULL;
    }

    PyObject *byte_class = PyObject_GetAttrString(byte_module, "Byte");
    Py_DECREF(byte_module);
    if (!byte_class) {
        Py_DECREF(from_raw_method);
        free(state);
        return NULL;
    }

    PyObject *memory_list = PyList_New(state->memory_size);
    if (!memory_list) {
        Py_DECREF(from_raw_method);
        Py_DECREF(byte_class);
        free(state);
        return NULL;
    }

    for (size_t i = 0; i < state->memory_size; i++) {
        PyObject *byte_value = _create_byte(byte_class, state->memory[i]);

        if (!byte_value) {
            Py_DECREF(memory_list);
            Py_DECREF(from_raw_method);
            Py_DECREF(byte_class);
            free(state);
            return NULL;
        }

        PyList_SetItem(memory_list, i,
                       byte_value); // Steals reference to byte_value
    }

    PyObject *accumulator = _create_byte(byte_class, state->accumulator);
    PyObject *pc_msb_register =
        _create_byte(byte_class, state->pc_msb_register);
    PyObject *pc_lsb_register =
        _create_byte(byte_class, state->pc_lsb_register);
    PyObject *temp_register = _create_byte(byte_class, state->temp_register);
    PyObject *mar_msb_register =
        _create_byte(byte_class, state->mar_msb_register);
    PyObject *mar_lsb_register =
        _create_byte(byte_class, state->mar_lsb_register);
    PyObject *opcode = _create_byte(byte_class, state->opcode);
    PyObject *cycle_step = _create_byte(byte_class, state->cycle_step);
    PyObject *is_halt = _create_byte(byte_class, state->is_halt);

    Py_DECREF(byte_class);
    free(state);

    if (!accumulator || !pc_msb_register || !pc_lsb_register ||
        !temp_register || !mar_msb_register || !mar_lsb_register || !opcode ||
        !cycle_step || !is_halt) {
        Py_XDECREF(memory_list);
        Py_XDECREF(accumulator);
        Py_XDECREF(pc_msb_register);
        Py_XDECREF(pc_lsb_register);
        Py_XDECREF(temp_register);
        Py_XDECREF(mar_msb_register);
        Py_XDECREF(mar_lsb_register);
        Py_XDECREF(opcode);
        Py_XDECREF(cycle_step);
        Py_XDECREF(is_halt);
        Py_DECREF(from_raw_method);
        return NULL;
    }

    PyObject *args =
        Py_BuildValue("(OOOOOOOOOO)", memory_list, accumulator, pc_msb_register,
                      pc_lsb_register, temp_register, mar_msb_register,
                      mar_lsb_register, opcode, cycle_step, is_halt);

    Py_DECREF(memory_list);
    Py_DECREF(accumulator);
    Py_DECREF(pc_msb_register);
    Py_DECREF(pc_lsb_register);
    Py_DECREF(temp_register);
    Py_DECREF(mar_msb_register);
    Py_DECREF(mar_lsb_register);
    Py_DECREF(opcode);
    Py_DECREF(cycle_step);
    Py_DECREF(is_halt);

    if (!args) {
        Py_DECREF(from_raw_method);
        return NULL;
    }

    PyObject *result = PyObject_CallObject(from_raw_method, args);
    Py_DECREF(from_raw_method);
    Py_DECREF(args);

    if (!result) {
        return NULL;
    }

    return result;
}

static PyObject *_create_byte(PyObject *byte_class, int value) {
    PyObject *args = Py_BuildValue("(i)", value);
    if (!args) {
        return NULL;
    }
    PyObject *byte_obj = PyObject_CallObject(byte_class, args);
    Py_DECREF(args);
    return byte_obj;
}
