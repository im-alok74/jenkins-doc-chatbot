package io.jenkins.plugins.chatbot;

import jenkins.model.GlobalConfiguration;
import org.kohsuke.stapler.DataBoundSetter;

public class ChatbotConfiguration extends GlobalConfiguration {
    private String backendUrl;
    private String apiKey;

    public ChatbotConfiguration() {
        load();
    }

    public String getBackendUrl() {
        return backendUrl;
    }

    @DataBoundSetter
    public void setBackendUrl(String backendUrl) {
        this.backendUrl = backendUrl;
        save();
    }

    public String getApiKey() {
        return apiKey;
    }

    @DataBoundSetter
    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
        save();
    }
}
