use dotenv::dotenv;
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::env;
use tokio::time::{sleep, Duration};

#[derive(Debug, Deserialize)]
struct Signal {
    id: i64,
    tick_id: i64,
    #[serde(rename = "type")]
    signal_type: String,
    strength: Option<f64>,
}

#[derive(Debug, Serialize)]
struct Trade {
    signal_id: i64,
    side: String,
    qty: i32,
    price: f64,
    sl: f64,
    tp: f64,
    status: String,
    pnl: Option<f64>,
}

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    dotenv().ok();

    let supabase_url = env::var("SUPABASE_URL").expect("SUPABASE_URL not set");
    let supabase_key = env::var("SUPABASE_SERVICE_KEY").expect("SUPABASE_SERVICE_KEY not set");

    let client = Client::new();

    loop {
        println!("Polling for new signals...");

        let res = client
            .get(format!("{supabase_url}/rest/v1/signals?select=*"))
            .header("apikey", &supabase_key)
            .header("Authorization", format!("Bearer {}", &supabase_key))
            .send()
            .await?;

        let signals: Vec<Signal> = res.json().await.unwrap_or(vec![]);

        if signals.is_empty() {
            println!("No new signals...");
        } else {
            for signal in signals {
                println!("Executing signal: {signal:?}");

                let trade = Trade {
                    signal_id: signal.id,
                    side: signal.signal_type.clone(),
                    qty: 10,
                    price: 57000.0,
                    sl: 56700.0,
                    tp: 57500.0,
                    status: "sent".to_string(),
                    pnl: None,
                };

                let trade_res = client
                    .post(format!("{supabase_url}/rest/v1/trades"))
                    .header("apikey", &supabase_key)
                    .header("Authorization", format!("Bearer {}", &supabase_key))
                    .header("Content-Type", "application/json")
                    .json(&trade)
                    .send()
                    .await?;

                if trade_res.status().is_success() {
                    println!("Trade executed: {trade:?}");
                } else {
                    println!("Failed to insert trade: {:?}", trade_res.status());
                }
            }
        }

        sleep(Duration::from_secs(2)).await;
    }
}
