package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Docker Multi-Stage Build</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #0b0f19; color: #f8fafc; }
    .card { background: #151d2f; padding: 2.5rem 3.5rem; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); text-align: center; border: 1px solid #24324f; max-width: 600px; }
    h1 { color: #38bdf8; margin-bottom: 0.75rem; font-size: 1.8rem; }
    p { color: #94a3b8; font-size: 1.1rem; line-height: 1.6; }
    .badge { display: inline-block; padding: 0.35rem 0.85rem; border-radius: 9999px; background: #0284c7; color: #f0f9ff; font-size: 0.875rem; font-weight: 600; margin-top: 1rem; }
    .tag { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 6px; background: #1e293b; color: #38bdf8; font-family: monospace; font-size: 0.85rem; margin: 0.2rem; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Hello World from Docker multi-stage build</h1>
    <p>This application was compiled inside a builder container and copied into an ultra-lean Alpine runtime container on port 8080.</p>
    <div style="margin-top: 1rem;">
      <span class="tag">Stage 1: golang:1.21-alpine (Builder)</span><br>
      <span class="tag">Stage 2: alpine:latest (Final Runtime)</span>
    </div>
    <span class="badge">DevOps Assignment 06 – Multi-Stage Build</span>
  </div>
</body>
</html>`)
}

func main() {
	http.HandleFunc("/", handler)
	fmt.Println("Multi-stage web server listening on port 8080...")
	http.ListenAndServe(":8080", nil)
}
