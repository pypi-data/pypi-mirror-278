use pyo3::prelude::*;
mod blacklist;
mod filter;
mod parse;

use filter::is_blacklisted;
use parse::{parse_attributes, parse_binary_json, old_cookie_parser};

#[pymodule]
fn holded_dataflow(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(is_blacklisted, m)?)?;
    m.add_function(wrap_pyfunction!(parse_attributes, m)?)?;
    m.add_function(wrap_pyfunction!(parse_binary_json, m)?)?;
    m.add_function(wrap_pyfunction!(old_cookie_parser, m)?)?;
    Ok(())
}
