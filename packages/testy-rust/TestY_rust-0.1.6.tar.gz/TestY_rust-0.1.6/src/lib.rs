use pyo3::prelude::*;

mod serialization;
mod sql;
#[pymodule]
fn rusty(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(serialization::serialize_tree, m)?)?;
    m.add_function(wrap_pyfunction!(sql::cases_search, m)?)?;
    Ok(())
}
