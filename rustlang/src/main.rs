extern crate chrono;
extern crate futures;
extern crate futures_cpupool;
extern crate num_cpus;
extern crate postgres;
extern crate r2d2;
extern crate r2d2_postgres;
extern crate serde_json;
#[macro_use]
extern crate serde_derive;
extern crate tokio_minihttp;
extern crate tokio_proto;
extern crate tokio_service;

use dotenv;
use std::io;

use chrono::{DateTime, SecondsFormat, Utc};
use futures::future::{self, Either};
use futures::Future;
use futures_cpupool::{CpuFuture, CpuPool};
use r2d2_postgres::{PostgresConnectionManager, TlsMode};

use tokio_minihttp::{Http, Request, Response};
use tokio_proto::TcpServer;
use tokio_service::Service;

struct Techempower {
    thread_pool: CpuPool,
    db_pool: r2d2::Pool<r2d2_postgres::PostgresConnectionManager>,
}

#[derive(Serialize)]
struct SecurityData {
    isin: String,
    data: serde_json::Value,
    last_updated: String,
}

impl Service for Techempower {
    type Request = Request;
    type Response = Response;
    type Error = std::io::Error;
    type Future =
        Either<future::Ok<Response, io::Error>, Box<dyn Future<Item = Response, Error = io::Error>>>;

    fn call(&self, req: Request) -> Self::Future {
        // Bare-bones router
        match req.path() {
            p if p.starts_with("/securities") => Either::B(self.securities(&req)),
            _ => {
                let mut resp = Response::new();
                resp.status_code(404, "Not Found");
                Either::A(future::ok(resp))
            }
        }
    }
}

impl Techempower {
    fn securities(&self, req: &Request) -> Box<dyn Future<Item = Response, Error = io::Error>> {
        let path = req.path();

        let request_url_parts: Vec<&str> = path.split("/").collect();

        if request_url_parts.len() < 3 {
            let mut resp = Response::new();
            resp.status_code(400, "Bad Request");
            return Box::new(future::ok(resp));
        }

        let request_isin = request_url_parts[2].to_string();

        let row = self.get_db_row(request_isin);

        return Box::new(row.map(|row| {
            let mut resp = Response::new();
            resp.header("Content-Type", "application/json")
                .body(&serde_json::to_string(&row).unwrap());
            return resp;
        }));
    }

    fn get_db_row(&self, isin: String) -> CpuFuture<SecurityData, io::Error> {
        let db = self.db_pool.clone();
        self.thread_pool.spawn_fn(move || {
            let conn = db
                .get()
                .map_err(|e| io::Error::new(io::ErrorKind::Other, format!("timeout: {}", e)))?;

            let stmt = conn
                .prepare_cached("select isin, data, last_updated from securities where isin=$1")?;
            let rows = stmt.query(&[&isin])?;

            let row = rows.get(0);

            let isin: String = row.get(0);
            let data: serde_json::Value = row.get(1);
            let last_updated = DateTime::<Utc>::from_utc(row.get(2), Utc);

            Ok(SecurityData {
                isin: isin,
                data: data,
                last_updated: last_updated.to_rfc3339_opts(SecondsFormat::Micros, true),
            })
        })
    }
}

fn main() {
    let addr = "0.0.0.0:8002".parse().unwrap();
    let thread_pool = CpuPool::new(10);

    dotenv::dotenv().ok();

    let postgres_host = match dotenv::var("DB_HOST") {
        Ok(value) => value,
        Err(error) => panic!("Error reading {} env variable: {:?}", "DB_HOST", error),
    };

    let postgres_port = match dotenv::var("DB_PORT") {
        Ok(value) => value,
        Err(error) => panic!("Error reading {} env variable: {:?}", "DB_PORT", error),
    };

    let postgres_user = match dotenv::var("DB_USER") {
        Ok(value) => value,
        Err(error) => panic!("Error reading {} env variable: {:?}", "DB_USER", error),
    };

    let postgres_password = match dotenv::var("DB_PASSWORD") {
        Ok(value) => value,
        Err(error) => panic!("Error reading {} env variable: {:?}", "DB_PASSWORD", error),
    };

    let postgres_db_name = match dotenv::var("DB_NAME") {
        Ok(value) => value,
        Err(error) => panic!("Error reading {} env variable: {:?}", "DB_NAME", error),
    };

    let postgres_uri = std::format!(
        "postgres://{}:{}@{}:{}/{}",
        postgres_user,
        postgres_password,
        postgres_host,
        postgres_port,
        postgres_db_name,
    );

    let db_config = r2d2::Config::default();
    let db_manager = PostgresConnectionManager::new(&postgres_uri[..], TlsMode::None).unwrap();
    let db_pool = r2d2::Pool::new(db_config, db_manager).unwrap();

    let mut srv = TcpServer::new(Http, addr);
    srv.threads(num_cpus::get());
    srv.serve(move || {
        Ok(Techempower {
            thread_pool: thread_pool.clone(),
            db_pool: db_pool.clone(),
        })
    })
}
