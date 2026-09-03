import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class Main {
    public static void main(String[] args) throws IOException {
        int port = 8082;
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 0);

        String response = "<!DOCTYPE html>\n" +
                "<html lang=\"en\">\n" +
                "<head>\n" +
                "  <meta charset=\"UTF-8\">\n" +
                "  <title>Java App - Assignment 06</title>\n" +
                "  <style>\n" +
                "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #0f172a; color: #f8fafc; }\n" +
                "    .card { background: #1e293b; padding: 2.5rem 3.5rem; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; }\n" +
                "    h1 { color: #f87171; margin-bottom: 0.5rem; }\n" +
                "    p { color: #94a3b8; font-size: 1.1rem; }\n" +
                "    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; background: #991b1b; color: #fee2e2; font-size: 0.875rem; font-weight: 600; margin-top: 1rem; }\n" +
                "  </style>\n" +
                "</head>\n" +
                "<body>\n" +
                "  <div class=\"card\">\n" +
                "    <h1>Java Application Deployed</h1>\n" +
                "    <p>Running inside Docker container on port 8082</p>\n" +
                "    <span class=\"badge\">Task 3: Docker Application Deployment</span>\n" +
                "  </div>\n" +
                "</body>\n" +
                "</html>";

        server.createContext("/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                byte[] bytes = response.getBytes("UTF-8");
                exchange.getResponseHeaders().set("Content-Type", "text/html; charset=utf-8");
                exchange.sendResponseHeaders(200, bytes.length);
                OutputStream os = exchange.getResponseBody();
                os.write(bytes);
                os.close();
            }
        });

        server.setExecutor(null);
        System.out.println("Java server running on port " + port);
        server.start();
    }
}
