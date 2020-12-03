package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"path"
	"time"

	"github.com/jackc/pgx/v4/pgxpool"
	"github.com/joho/godotenv"
)

var pool *pgxpool.Pool

func main() {

	godotenv.Load("../../.env")

	postgresHost, ok := os.LookupEnv("DB_HOST")
	if !ok {
		fmt.Printf("%s not set\n", "DB_HOST")
		os.Exit(1)
	}
	postgresPort, ok := os.LookupEnv("DB_PORT")
	if !ok {
		fmt.Printf("%s not set\n", "DB_PORT")
		os.Exit(1)
	}
	postgresUser, ok := os.LookupEnv("DB_USER")
	if !ok {
		fmt.Printf("%s not set\n", "DB_USER")
		os.Exit(1)
	}
	postgresPassword, ok := os.LookupEnv("DB_PASSWORD")
	if !ok {
		fmt.Printf("%s not set\n", "DB_PASSWORD")
		os.Exit(1)
	}
	postgresDatabaseName, ok := os.LookupEnv("DB_NAME")
	if !ok {
		fmt.Printf("%s not set\n", "DB_NAME")
		os.Exit(1)
	}

	postgresURI := fmt.Sprintf(
		"postgres://%s:%s@%s:%s/%s",
		postgresUser,
		postgresPassword,
		postgresHost,
		postgresPort,
		postgresDatabaseName,
	)

    var err error
	pool, err = pgxpool.Connect(context.Background(), postgresURI)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer pool.Close()

	handler := http.NewServeMux()
	handler.HandleFunc("/securities/", Securities)
	http.ListenAndServe("0.0.0.0:8001", handler)
}

func Securities(w http.ResponseWriter, r *http.Request) {

	request_isin := path.Base(r.URL.Path)

    var request_currency string
	m, _ := url.ParseQuery(r.URL.RawQuery)
    if len(m["currency"]) != 0 {
        request_currency = m["currency"][0]
    } else {
        request_currency = "SUR"
    }

	var isin string
	var data []byte
	var last_updated time.Time

	err := pool.QueryRow(
		context.Background(),
		"select isin, data, last_updated from securities where isin=$1 and currency=$2",
		request_isin,
		request_currency,
	).Scan(&isin, &data, &last_updated)

	var json_data map[string]interface{}
	if err := json.Unmarshal(data, &json_data); err != nil {
		panic(err)
	}

	result := make(map[string]interface{})
	result["isin"] = isin
	result["data"] = json_data
	result["last_updated"] = last_updated

	out, _ := json.Marshal(result)

	w.Header().Add("Content-Type", "application/json")

	if err != nil {
		w.WriteHeader(404)
		fmt.Fprintf(w, "null")
	} else {
		fmt.Fprintf(w, string(out))
	}
}
