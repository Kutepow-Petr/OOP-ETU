package Structures;

import java.util.HashMap;
import java.util.Map;

public class Streets {
    private Map<String, Houses> streetsMap; // название улицы, список домов в ней

    public Streets() {
        streetsMap = new HashMap<>();
    }

    public Map<String, Houses> getStreetsMap() {
        return streetsMap;
    }

    public Houses getOrCreateHouses(String streetName) {
        return streetsMap.computeIfAbsent(streetName, key -> new Houses());
    }
}