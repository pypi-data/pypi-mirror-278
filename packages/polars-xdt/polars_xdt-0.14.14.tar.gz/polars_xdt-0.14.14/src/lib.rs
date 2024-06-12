mod arg_previous_greater;
mod business_days;
mod ewma_by_time;
mod expressions;
mod format_localized;
mod is_workday;
mod month_delta;
mod sub;
mod timezone;
mod to_julian;
mod utc_offsets;

use pyo3::types::PyModule;
use pyo3::{pymodule, Bound, PyResult};

#[cfg(target_os = "linux")]
use jemallocator::Jemalloc;

#[global_allocator]
#[cfg(target_os = "linux")]
static ALLOC: Jemalloc = Jemalloc;

#[pymodule]
fn _internal(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
