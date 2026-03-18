package io.jenkins.plugins.chatbot;

import hudson.Extension;
import jenkins.model.GlobalConfiguration;

@Extension
public class ChatbotPlugin extends GlobalConfiguration {
    public ChatbotPlugin() {
        load();
    }
}
