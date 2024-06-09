use pyo3::prelude::*;
use pyo3::types::PyDict;
use serde_json::Value;
use std::collections::HashMap;
use pyo3::exceptions;


pub struct PyJsonValue(pub Value);

impl ToPyObject for PyJsonValue {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        value_to_object(&self.0, py)
    }
}
pub fn value_to_object(val: &Value, py: Python<'_>) -> PyObject {
    match val {
        Value::Null => py.None(),
        Value::Bool(b) => b.to_object(py),
        Value::Number(n) => {
            let oi64 = n.as_i64().map(|i| i.to_object(py));
            let ou64 = n.as_u64().map(|i| i.to_object(py));
            let of64 = n.as_f64().map(|i| i.to_object(py));
            oi64.or(ou64).or(of64).expect("number too large")
        },
        Value::String(s) => s.to_object(py),
        Value::Array(v) => {
            let inner: Vec<_> = v.iter().map(|x| value_to_object(x, py)).collect();
            inner.to_object(py)
        },
        Value::Object(m) => {
            let inner: HashMap<_, _> =
                m.iter().map(|(k, v)| (k, value_to_object(v, py))).collect();
            inner.to_object(py)
        },
    }
}

pub fn parse_value(value: &str) -> Result<Value, serde_json::Error> {
    let parsed_value: Value = serde_json::from_str(value)?;

    // Check if the parsed value is an array
    if let Value::Array(arr) = &parsed_value {
        // If the array has elements, return the first one
        if let Some(first_elem) = arr.get(0) {
            return Ok(first_elem.clone());
        }
    }

    Ok(parsed_value)
}

#[pyfunction]
pub fn parse_attributes(py: Python, attributes: HashMap<String, String>, _py: Python) -> PyResult<PyObject> {
    let parsed_attributes = PyDict::new(_py);

    for (key, value) in attributes {
        if ["type", "Product", "Content-Type"].contains(&&*key) {
            parsed_attributes.set_item(key, value)?;
        } else {
            let parsed_value = match parse_value(&value) {
                Ok(val) => val,
                Err(_) => Value::String(value),
            };
            let parsed_json_pyobj = PyJsonValue(parsed_value).to_object(py);
            parsed_attributes.set_item(
                key.split("\\").last().unwrap_or(&key).to_string(),
                parsed_json_pyobj,
            )?;
        }
    }

    Ok(parsed_attributes.into())
}

#[pyfunction]
pub fn parse_binary_json(py: Python, data: &PyAny) -> PyResult<PyObject> {
    // Extract binary data
    let bytes_data = data.extract::<&[u8]>()?;

    // Decode binary data into a UTF-8 string
    let json_str = std::str::from_utf8(bytes_data)
        .map_err(|e| PyErr::new::<exceptions::PyUnicodeDecodeError, _>(format!("{}", e)))?;

    // Parse UTF-8 string as JSON
    let parsed_json: Value = serde_json::from_str(json_str)
        .map_err(|e| PyErr::new::<exceptions::PyValueError, _>(format!("Failed to parse JSON: {}", e)))?;

    // Convert the parsed JSON to a Python object
    let parsed_json_pyobj = PyJsonValue(parsed_json).to_object(py);

    Ok(parsed_json_pyobj)
}
