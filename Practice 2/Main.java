import Structures.Cities;
import Utils.CitiesUtils;
import Utils.CsvXmlFileReader;

import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        while (true) {
            Scanner consoleInput = new Scanner(System.in);
            System.out.print("Введите путь до справочника или напишите \"exit\", чтобы выйти_");

            try {
                String userResponse = consoleInput.nextLine();
                long totalTime = System.currentTimeMillis(), separateTime = System.currentTimeMillis();
                if (userResponse.equals("exit")) {
                    return;
                } else {
                    CsvXmlFileReader reader = new CsvXmlFileReader();
                    reader.checkingFileExists(userResponse);

                    Cities listOfCities;
                    if (userResponse.matches(".*\\.csv$")) {
                        listOfCities = reader.readCsvFile(userResponse);
                    } else if (userResponse.matches(".*\\.xml$")) {
                        listOfCities = reader.readXmlFile(userResponse);
                    } else {
                        throw new IOException("Неизвестный формат файла.");
                    }

                    System.out.printf("\u001B[34mФайл прочитан за %dмс\u001B[0m\n", System.currentTimeMillis() - separateTime);
                    separateTime = System.currentTimeMillis();

                    CitiesUtils handlerForCitiesMap = new CitiesUtils();

                    handlerForCitiesMap.findDuplicateAddresses(listOfCities.getCitiesMap());

                    System.out.printf("\u001B[34mДубликаты найдены за %dмс\u001B[0m\n", System.currentTimeMillis() - separateTime);
                    separateTime = System.currentTimeMillis();

                    handlerForCitiesMap.printNumberOfStoreyBuildings(listOfCities.getCitiesMap());

                    System.out.printf("\u001B[34mКоличество домов найдено за %dмс\u001B[0m\n", System.currentTimeMillis() - separateTime);
                    System.out.printf("\u001B[34m\nОбщее время обработки файла = %dмс\u001B[0m\n", System.currentTimeMillis() - totalTime);
                }
            } catch (Exception error) {
                System.err.println("\nОшибка: " + error.getMessage());
            }
        }
    }
}
