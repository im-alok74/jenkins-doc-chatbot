package io.jenkins.plugins.chatbot;

import hudson.model.Action;
import hudson.model.Run;
import jenkins.model.Jenkins;

public class ChatbotAction implements Action {
    private final Run<?, ?> run;

    public ChatbotAction(Run<?, ?> run) {
        this.run = run;
    }

    @Override
    public String getIconFileName() {
        return "plugin/chatbot/images/chatbot.png";
    }

    @Override
    public String getDisplayName() {
        return "AI Assistant";
    }

    @Override
    public String getUrlName() {
        return "chatbot";
    }

    public String getJobName() {
        return run.getParent().getName();
    }

    public String getBuildId() {
        return String.valueOf(run.getNumber());
    }
}
