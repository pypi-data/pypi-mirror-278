use pyo3::prelude::pyfunction;
use pyo3::{exceptions::PyKeyError, PyErr};

pub use crate::blacklist::{PIPELINE_BLACKLIST, SSGTM_BLACKLIST};

#[pyfunction]
pub fn is_blacklisted(name: &str, filter_type: &str) -> Result<bool, PyErr> {
    match filter_type {
        "PIPELINE" => {
            Ok(PIPELINE_BLACKLIST.contains_key(name))
        }
        "SSGTM" => {
            Ok(SSGTM_BLACKLIST.contains_key(name))
        }
        _ => Err(PyErr::new::<PyKeyError, _>("This FilterType is not implemented")),
    }
}
