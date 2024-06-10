use clap::Parser;
use pdf_extract::extract_text;
use std::fs::File;
use std::io::Write;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

/// 命令行參數結構
#[derive(Parser)]
struct Cli {
    /// 輸入的 PDF 檔案路徑
    #[clap(short, long)]
    input: String,
    /// 輸出的 TXT 檔案路徑
    #[clap(short, long)]
    output: String,
}

#[pyfunction]
fn extract_text_from_pdf(input: &str, output: &str) -> PyResult<()> {
    let text = extract_text(input).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
    let mut output_file = File::create(output).map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;
    output_file.write_all(text.as_bytes()).map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;
    Ok(())
}

#[pymodule]
fn botrun_pdf_to_text_rust(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(extract_text_from_pdf, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_extract_text_from_pdf() {
        // 測試代碼
    }
}
