package Structures;

import java.util.HashMap;
import java.util.Map;

public class Houses {
    private Map<Integer, Floors> housesMap; // номер дома, список этажей в нём

    public Houses() {
        housesMap = new HashMap<>();
    }

    public Map<Integer, Floors> getHousesMap() {
        return housesMap;
    }

    public Floors getOrCreateFloors(int houseNumber) {
        return housesMap.computeIfAbsent(houseNumber, key -> new Floors());
    }
}