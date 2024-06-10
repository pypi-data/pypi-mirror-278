use clap::Parser;
use pdf_extract::extract_text;
use std::fs::File;
use std::io::Write;

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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Cli::parse();

    // 讀取 PDF 文件並提取文本
    let text = extract_text(&args.input)?;

    // 將提取的文本寫入 TXT 文件
    let mut output_file = File::create(&args.output)?;
    output_file.write_all(text.as_bytes())?;

    println!("PDF 轉換成 TXT 完成！");
    Ok(())
}
