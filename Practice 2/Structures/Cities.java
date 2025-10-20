package Structures;

import java.util.HashMap;
import java.util.Map;

public class Cities {
    private Map<String, Streets> citiesMap; // название города, список улиц в нём

    public Cities() {
        citiesMap = new HashMap<>();
    }

    public Map<String, Streets> getCitiesMap() {
        return citiesMap;
    }

    public Streets getOrCreateStreets(String cityName) {
        return citiesMap.computeIfAbsent(cityName, key -> new Streets());
    }
}