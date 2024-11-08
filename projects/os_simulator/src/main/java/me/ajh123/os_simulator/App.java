package me.ajh123.os_simulator;

import imgui.ImGui;
import imgui.type.ImBoolean;
import org.pf4j.ExtensionPoint;

public abstract class App implements ExtensionPoint {
    private final ImBoolean isRunning = new ImBoolean(false);

    public void init() {
        isRunning.set(true);
    }

    public void run() {
        ImGui.begin(getName(), isRunning);
        ImGUIProcess();
        ImGui.end();
    }

    public abstract void ImGUIProcess();
    public abstract String getName();

    public boolean isRunning() {
        return isRunning.get();
    }
}
