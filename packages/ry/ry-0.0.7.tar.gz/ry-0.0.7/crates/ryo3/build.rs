use chrono::Local;
use chrono::SecondsFormat;

fn main() {
    println!(
        "cargo:rustc-env=PROFILE={}",
        std::env::var("PROFILE").unwrap()
    );

    // build timestamp
    println!(
        "cargo:rustc-env=BUILD_TIMESTAMP={}",
        Local::now().to_rfc3339_opts(SecondsFormat::Secs, true)
    );
}
