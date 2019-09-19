#[macro_use] extern crate cpython;

use std::{mem, cell, vec};
use cpython::{ToPyObject, PyType, PyList, PyDict, PyObject, ObjectProtocol, PyModule, PyDrop, PyResult, Python};

// add bindings to the generated python module
// N.B: names: "librust2py" must be the name of the `.so` or `.pyd` file
py_module_initializer!(rust2py, initrust2py, PyInit_rust2py, |py, m| {
    m.add(py, "__doc__", "This module is implemented in Rust.")?;
    //m.add(py, "initialize", py_fn!(py, initialize_library( ) ))?;
    m.add(py, "RustChunk", py.get_type::<Chunk>())?;
    Ok(())
});

fn initialize_library(py: Python) -> PyResult<bool> {
    Ok(true)
}

py_class!(class Chunk |py| {
    data block_data: cell::RefCell<vec::Vec< vec::Vec< vec::Vec<u16> > > >; //[[[i32; 16]; 16]; 16]>;
    data x: i32;
    data z: i32;

    def __new__(cls, x:i32, z:i32) -> PyResult<Chunk> {
        //let block_data: cell::RefCell<[[[i32; 16]; 16]; 16]> = cell::RefCell::new([[[0; 16]; 16]; 16]);
        let block_data = cell::RefCell::new(vec![vec![vec![0; 16]; 256]; 16]);
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

    def set_block_id(&self, x: usize, y: usize, z: usize, block_id: u16) -> PyResult<bool> {
        let ref mut tmp_block_data = *(self.block_data(py).borrow_mut());
        tmp_block_data[x][y][z] = block_id;
        self.block_data(py).replace(tmp_block_data.to_vec());
        Ok(true)
    }

    def set_section(&self, section_id: i32, section: PyObject) -> PyResult<bool> {
        //Extract data: section.get_item(py, 0)?.extract::<u16>(py)?

        //Loop through data
        for x in 0..16 {
            for y in 0..16 {
                for z in 0..16 {
                    let idx: u16 = x + y * 16 + z * 16 * 16;
                    let data_result = section.get_item(py, 0);
                    if data_result.is_ok() {
                        let block_id = data_result.unwrap().extract::<u16>(py)?;
                        let ref mut tmp_block_data = *(self.block_data(py).borrow_mut());
                        tmp_block_data[x as usize][z as usize + (section_id as usize) * 16][y as usize] = block_id;
                        self.block_data(py).replace(tmp_block_data.to_vec());
                    }
                }
            }
        }

        Ok(true)
    }

    def get_block_id(&self, x: usize, y: usize, z: usize) -> PyResult<u16> {
        let block_id: u16 = self.block_data(py).borrow()[x][y][z];
        Ok(block_id)
    }

});
