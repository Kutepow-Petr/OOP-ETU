package Structures;

import java.util.HashMap;
import java.util.Map;

public class Floors {
    private Map<Short, Integer> floorsMap; // номер этажа, количество повторений адреса

    public Floors() {
        floorsMap = new HashMap<>();
    }

    public Map<Short, Integer> getFloorsMap() {
        return floorsMap;
    }

    public void incrementFloor(short floorNumber) {
        floorsMap.merge(floorNumber, 1, Integer::sum);
    }
}