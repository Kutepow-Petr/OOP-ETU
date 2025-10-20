package Utils;

import Structures.Floors;
import Structures.Houses;
import Structures.Streets;

import java.util.Collections;
import java.util.Map;

public class CitiesUtils {
    public void findDuplicateAddresses(Map<String, Streets> citiesMap) {
        System.out.println("\n\u001B[47m\u001B[30mПОВТОРЯЮЩИЕСЯ АДРЕСА\u001B[0m");

        citiesMap.forEach((cityName, streets) -> {
            streets.getStreetsMap().forEach((streetName, houses) -> {
                houses.getHousesMap().forEach((houseNumber, floors) -> {
                    floors.getFloorsMap().forEach((floorNumber, repeats) -> {
                        if (repeats > 1) {
                            System.out.printf("Адрес: %s, %s, дом %d, этаж %d; Повторений: %d\n",
                                    cityName, streetName, houseNumber, floorNumber, repeats);
                        }
                    });
                });
            });
        });
    }

    public void printNumberOfStoreyBuildings(Map<String, Streets> citiesMap) {
        System.out.println("\n\u001B[47m\u001B[30mКОЛИЧЕСТВО 1, 2, 3, 4 И 5-ти ЭТАЖНЫХ ЗДАНИЙ\u001B[0m");

        citiesMap.forEach((cityName, streets) -> {
            int[] numberOfHouses = new int[6];

            for (Houses houses : streets.getStreetsMap().values()) {
                for (Floors floors : houses.getHousesMap().values()) {

                    int maxFloor = Collections.max(floors.getFloorsMap().keySet());
                    if (maxFloor >= 1 && maxFloor <= 5) {
                        numberOfHouses[maxFloor]++;
                    }
                }
            }
            System.out.printf("%s:\n\t1-этажных = %d\n\t2-этажных = %d\n\t3-этажных = %d\n\t4-этажных = %d\n\t5-этажных = %d\n",
                    cityName, numberOfHouses[1], numberOfHouses[2], numberOfHouses[3], numberOfHouses[4], numberOfHouses[5]);
        });
    }
}
