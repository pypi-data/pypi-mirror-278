use pyo3::prelude::*;
use pyo3::types::PyDict;
use serde_json::Value;
use std::collections::HashMap;
use pyo3::exceptions;
use url::Url;

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

#[pyfunction]
pub fn old_cookie_parser(py: Python, cookie: &str) -> PyResult<PyObject> {
    let domains = vec![
        "360.cn", "alice.com", "alltheweb.com", "altavista.com", ".aol.", "ask.com", "search.auone.jp",
        "isearch.avg.com", "search.babylon.com", "baidu.com", "biglobe.ne.jp", "bing.com", "search.centrum.cz",
        "search.comcast.net", "search.conduit.com", "www.cnn.com/search", "daum.net", "duckduckgo.com",
        "ecosia.org", "ekolay.net", "eniro.se", "globo.com/busca", "go.mail.ru", "google", "goo.ne.jp",
        "haosou.com/s", "search.incredimail.com", "kvasir.no", "bing.com", "lycos.com", "search.lycos",
        "mamma.com", "msn.com", "mynet.com", "najdi.si", "naver.com", "search.netscape.com",
        "szukaj.onet.pl", "ozu.es", "rakuten.co.jp", "rambler.ru", "search-results.com",
        "search.smt.docomo.ne.jp", "sesam.no", "seznam.cz", "so.com/s", "sogou.com", "startsiden.no/sok",
        "szukacz.pl", "buscador.terra.com.br", "search.tut.by", "search.ukr.net", "search.virgilio.it",
        "voila.fr", "wp.pl", "yahoo", "yandex", "yam.com", "google.com",
    ];

    let mut domain = None;
    let mut domain_name = false;
    let mut cookie_data = HashMap::new();

    let first_int_cookie = cookie.split(',');

    for element in first_int_cookie {
        let split_element: Vec<&str> = element.split(':').collect();
        if split_element.len() < 2 {
            continue;
        }
        let key = split_element[0].trim();
        cookie_data.insert(key.to_string(), split_element[1..].join(":").trim().to_string());

        if key == "landing_page" {
            if let Ok(landing_page_parsed) = Url::parse(&cookie_data[key]) {
                cookie_data.insert(
                    "landing_page_cleaned".to_string(),
                    format!(
                        "{}://{}{}",
                        landing_page_parsed.scheme(),
                        landing_page_parsed.host_str().unwrap_or(""),
                        landing_page_parsed.path()
                    ),
                );

                if let Some(query) = landing_page_parsed.query() {
                    for (qs_key, qs_value) in url::form_urlencoded::parse(query.as_bytes()) {
                        cookie_data.insert(qs_key.into_owned(), qs_value.into_owned());
                    }
                }
            }
        }

        if key == "landing_date" {
            if let Ok(landing_date) = cookie_data[key].parse::<i64>() {
                let landing_date_secs = ((landing_date as f64) / 1000.0).ceil() as i64;
                cookie_data.insert("landing_date".to_string(), landing_date_secs.to_string());
            }
        }
    }

    if let Some(http_referer) = cookie_data.get("http_referer") {
        if let Ok(referer_parsed) = Url::parse(http_referer) {
            domain = referer_parsed.host_str().map(|host| host.replace("www.", ""));
            domain_name = domain.as_deref().map(|d| domains.contains(&d)).unwrap_or(false);
        }
    }

    if !cookie.contains("utm_medium") {
        if domain_name || domain.as_deref().map(|d| domains.contains(&d)).unwrap_or(false) {
            cookie_data.insert("utm_medium".to_string(), "organic".to_string());
            if let Some(d) = domain.clone() {
                cookie_data.insert("utm_source".to_string(), d);
            }
        } else {
            cookie_data.insert("utm_medium".to_string(), "referral".to_string());
            if let Some(d) = domain.clone() {
                cookie_data.insert("utm_source".to_string(), d);
            }
        }

        if !cookie.contains("http_referer") {
            cookie_data.insert("utm_medium".to_string(), "(none)".to_string());
            cookie_data.insert("utm_source".to_string(), "direct".to_string());
        }
    }

    let py_dict = PyDict::new(py);
    for (key, value) in cookie_data {
        if key == "landing_date" {
            if let Ok(landing_date) = value.parse::<i64>() {
                py_dict.set_item(key, landing_date)?;
            } else {
                py_dict.set_item(key, value)?;
            }
        } else {
            py_dict.set_item(key, value)?;
        }
    }

    Ok(py_dict.into())
}
