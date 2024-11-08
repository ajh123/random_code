package me.ajh123.os_simulator;

import imgui.ImGui;
import imgui.ImGuiIO;
import imgui.ImVec2;
import imgui.app.Application;
import imgui.app.Configuration;
import imgui.flag.ImGuiConfigFlags;
import imgui.flag.ImGuiWindowFlags;
import org.pf4j.JarPluginManager;
import org.pf4j.PluginManager;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Main extends Application {
    private final PluginManager pluginManager = new JarPluginManager();
    private final Map<String, ImVec2> buttonPositions = new HashMap<>();
    private List<App> apps;
    private final List<App> openApps = new ArrayList<>();

    @Override
    protected void configure(Configuration config) {
        config.setTitle("OS Simulator");
    }

    @Override
    protected void initImGui(Configuration config) {
        super.initImGui(config);
        final ImGuiIO io = ImGui.getIO();
        io.setIniFilename(null);                                // We don't want to save .ini file
        io.addConfigFlags(ImGuiConfigFlags.NavEnableKeyboard);  // Enable Keyboard Controls
        io.addConfigFlags(ImGuiConfigFlags.DockingEnable);      // Enable Docking
        io.addConfigFlags(ImGuiConfigFlags.ViewportsEnable);    // Enable Multi-Viewport / Platform Windows
        io.setConfigViewportsNoTaskBarIcon(true);

        pluginManager.loadPlugins();
        pluginManager.startPlugins();

        apps = pluginManager.getExtensions(App.class);
    }

    @Override
    public void process() {
        // Set the main window's dimensions to fill the OS window
        float width = ImGui.getWindowViewport().getSizeX();
        float height = ImGui.getWindowViewport().getSizeY();
        float x = ImGui.getWindowViewport().getPosX();
        float y = ImGui.getWindowViewport().getPosY();

        // Set flags for a transparent, borderless ImGui window
        int windowFlags = ImGuiWindowFlags.NoTitleBar | ImGuiWindowFlags.NoResize | ImGuiWindowFlags.NoMove |
                ImGuiWindowFlags.NoBackground | ImGuiWindowFlags.NoDocking | ImGuiWindowFlags.NoBringToFrontOnFocus;

        // Begin the window, set its position and size to cover the main window
        ImGui.setNextWindowPos(x, y);
        ImGui.setNextWindowSize(width, height);
        ImGui.begin("Desktop", windowFlags);

        float buttonSize = 100.0f; // Adjust button size as needed
        float buttonSpacing = 20.0f; // Adjust spacing between buttons
        int buttonsPerRow = 5; // Number of buttons per row in the grid

        for (int i = 0; i < apps.size(); i++) {
            App app = apps.get(i);
            String appName = app.getName(); // Assuming App class has a getName() method

            // Calculate grid position based on index
            int row = i / buttonsPerRow;
            int col = i % buttonsPerRow;
            float initialX = 10.0f + col * (buttonSize + buttonSpacing);
            float initialY = 10.0f + row * (buttonSize + buttonSpacing);

            // Set the initial position for the button if it hasn't been moved
            buttonPositions.putIfAbsent(appName, new ImVec2(initialX, initialY));

            // Retrieve and set the current position
            ImVec2 pos = buttonPositions.get(appName);
            ImGui.setCursorPos(pos.x, pos.y);

            if (ImGui.button(appName, buttonSize, buttonSize)) {
                openApp(app);
            }

            // Make the button draggable
            if (ImGui.isItemActive()) {
                pos.x += ImGui.getIO().getMouseDeltaX();
                pos.y += ImGui.getIO().getMouseDeltaY();
                buttonPositions.put(appName, pos); // Update the stored position
            }
        }

        // End the window
        ImGui.end();

        for (App app : openApps) {
            app.run();
        }

        openApps.removeIf(app -> !app.isRunning());
    }

    @Override
    protected void dispose() {
        super.dispose();
        pluginManager.stopPlugins();
        pluginManager.unloadPlugins();
    }

    protected void openApp(App app) {
        app.init();
        openApps.add(app);
    }

    public static void main(String[] args) {
        launch(new Main());
    }
}