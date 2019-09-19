#[macro_use] extern crate cpython;

use std::{mem, cell, vec};
use cpython::{ToPyObject, PyType, PyList, PyDict, PyObject, ObjectProtocol, PyModule, PyDrop, PyResult, Python};

// add bindings to the generated python module
// N.B: names: "librust2py" must be the name of the `.so` or `.pyd` file
py_module_initializer!(rust2py, initrust2py, PyInit_rust2py, |py, m| {
    m.add(py, "__doc__", "This module is implemented in Rust.")?;
    m.add(py, "sum_as_string", py_fn!(py, sum_as_string_py(a: i64, b:i64)))?; // Only here for testing
    m.add(py, "initialize", py_fn!(py, initialize_library( ) ))?;
    m.add(py, "TestType", py.get_type::<TestType>())?;
    m.add(py, "ClassWithGCSupport", py.get_type::<TestType>())?;
    m.add(py, "RustChunk", py.get_type::<Chunk>())?;
    Ok(())
});

// logic implemented as a normal rust function
fn sum_as_string(a:i64, b:i64) -> String {
    format!("{}", a + b).to_string()
}

// rust-cpython aware function. All of our python interface could be
// declared in a separate module.
// Note that the py_fn!() macro automatically converts the arguments from
// Python objects to Rust values; and the Rust return value back into a Python object.
fn sum_as_string_py(_: Python, a:i64, b:i64) -> PyResult<String> {
    let out = sum_as_string(a, b);
    Ok(out)
}

fn initialize_library(py: Python) -> PyResult<bool> {
    Ok(true)
}

// Trying to create a class
py_class!(class TestType |py| {
    data number: i32;
    def __new__(_cls, arg: i32) -> PyResult<TestType> {
        TestType::create_instance(py, arg)
    }
    def half(&self) -> PyResult<i32> {
        println!("half() was called with self={:?}", self.number(py));
        Ok(self.number(py) / 2)
    }
});

py_class!(class ClassWithGCSupport |py| {
    data obj: cell::RefCell<Option<PyObject>>;

    def __traverse__(&self, visit) {
        if let Some(ref obj) = *self.obj(py).borrow() {
            visit.call(obj)?
        }
        Ok(())
    }

    def __clear__(&self) {
        let old_obj = mem::replace(&mut *self.obj(py).borrow_mut(), None);
        // Release reference only after the mutable borrow has expired,
        // see Caution note below.
        old_obj.release_ref(py);
    }
});

py_class!(class Chunk |py| {
    data block_data: cell::RefCell<vec::Vec< vec::Vec< vec::Vec<u16> > > >; //[[[i32; 16]; 16]; 16]>;
    data x: i32;
    data z: i32;

    def __new__(cls, x:i32, z:i32) -> PyResult<Chunk> {
        //let block_data: cell::RefCell<[[[i32; 16]; 16]; 16]> = cell::RefCell::new([[[0; 16]; 16]; 16]);
        let block_data = cell::RefCell::new(vec![vec![vec![0; 16]; 16]; 16]);
        Chunk::create_instance(py, block_data,x,z)
    }

    def get_x(&self) -> PyResult<i32> {
        Ok(*self.x(py))
    }

    def get_z(&self) -> PyResult<i32> {
        Ok(*self.z(py))
    }

    def get_block_data(&self) -> PyResult<PyList> {
        let block_data = &*self.block_data(py).borrow();
        let py_block_data: PyList = block_data.to_py_object(py);
        Ok(py_block_data)
    }

    def set_block(&self, x: usize, y: usize, z: usize, block_id: u16) -> PyResult<bool> {
        let ref mut tmp_block_data = *(self.block_data(py).borrow_mut());
        tmp_block_data[x][y][z] = block_id;
        self.block_data(py).replace(tmp_block_data.to_vec());
        Ok(true)
    }

    def set_section(&self, section_id: i32, section: PyObject) -> PyResult<bool> {
        // let quarry: PyModule = py.import("quarry")?;
        // let quarry_types: PyObject = quarry.get(py, "types")?.extract<PyModule>(py)?;
        // let quarry_types_chunk: PyObject = quarry_types.get(py, "chunk")?.extract<PyModule>(py)?;
        // let block_array_type: PyType = section.get_type(py);

        //Extract data: section.get_item(py, 0)?.extract::<u16>(py)?

        //Loop through data
        for x in 0..16 {
            for y in 0..16 {
                for z in 0..16 {
                    let idx: u16 = x + y * 16 + z * 16 * 16;
                    let data_result = section.get_item(py, 0);
                    if data_result.is_ok() {
                        let block_id = data_result.unwrap().extract::<u16>(py)?;
                        // Chunk::set_block(self, x as usize, y as usize + (section_id as usize) * 16, z as usize, block_id);
                        let ref mut tmp_block_data = *(self.block_data(py).borrow_mut());
                        tmp_block_data[x as usize][y as usize + (section_id as usize) * 16][z as usize] = block_id;
                        self.block_data(py).replace(tmp_block_data.to_vec());
                    }
                }
            }
        }

        Ok(true)

        //Ok(section.get_type(py).name(py).into_owned())
    }

});
