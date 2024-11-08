package me.ajh123.os_simulator.apps;

import me.ajh123.os_simulator.App;
import org.pf4j.Extension;

@Extension
public class Calculator implements App {
    @Override
    public void init() {
        System.out.println("AAAA");
    }

    @Override
    public void ImGUIProcess() {

    }

    @Override
    public String getName() {
        return "Calculator";
    }
}
