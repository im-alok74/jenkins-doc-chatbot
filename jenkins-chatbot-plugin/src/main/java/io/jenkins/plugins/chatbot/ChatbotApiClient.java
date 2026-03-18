package io.jenkins.plugins.chatbot;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class ChatbotApiClient {
    private final String backendUrl;
    private final String apiKey;

    public ChatbotApiClient(String backendUrl, String apiKey) {
        this.backendUrl = backendUrl;
        this.apiKey = apiKey;
    }

    public String sendMessage(String query, String context) throws IOException {
        String endpoint = backendUrl + "/api/chat";
        String payload = String.format("{\"query\":\"%s\",\"context\":%s,\"conversation_history\":[]}", query, context);
        return postJson(endpoint, payload);
    }

    public String analyzeLogs(String consoleLog) throws IOException {
        String endpoint = backendUrl + "/api/logs/analyze";
        String payload = String.format("{\"console_log\":\"%s\"}", consoleLog);
        return postJson(endpoint, payload);
    }

    private String postJson(String endpoint, String payload) throws IOException {
        URL url = new URL(endpoint);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setRequestProperty("Authorization", "Bearer " + apiKey);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(30000);
        conn.setDoOutput(true);
        conn.getOutputStream().write(payload.getBytes());
        Scanner scanner = new Scanner(conn.getInputStream()).useDelimiter("\A");
        String response = scanner.hasNext() ? scanner.next() : "";
        scanner.close();
        conn.disconnect();
        return response;
    }
}
