package Utils;

import Structures.Cities;
import Structures.Floors;
import Structures.Houses;
import Structures.Streets;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamReader;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class CsvXmlFileReader {
    public Cities readCsvFile(String filePath) throws IOException {
        Cities listOfCities = new Cities();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line = reader.readLine();

            while ((line = reader.readLine()) != null) {
                line = line.replaceAll("\"", "");
                String[] values = line.split(";");

                if (values.length == 4) {
                    String city = values[0];
                    String street = values[1];
                    int house = Integer.parseInt(values[2]);
                    short floor = Short.parseShort(values[3]);

                    Streets listOfStreets = listOfCities.getOrCreateStreets(city);
                    Houses listOfHouses = listOfStreets.getOrCreateHouses(street);
                    Floors listOfFloors = listOfHouses.getOrCreateFloors(house);
                    listOfFloors.incrementFloor(floor);
                }
            }
        }
        return listOfCities;
    }

    public Cities readXmlFile(String filePath) throws Exception {
        Cities listOfCities = new Cities();
        XMLInputFactory factory = XMLInputFactory.newInstance();

        try (FileReader fileReader = new FileReader(filePath)) {
            XMLStreamReader reader = factory.createXMLStreamReader(fileReader);

            while (reader.hasNext()) {
                int event = reader.next();

                if (event == XMLStreamReader.START_ELEMENT && "item".equals(reader.getLocalName())) {

                    String city = reader.getAttributeValue(null, "city");
                    String street = reader.getAttributeValue(null, "street");
                    int house = Integer.parseInt(reader.getAttributeValue(null, "house"));
                    short floor = Short.parseShort(reader.getAttributeValue(null, "floor"));

                    Streets listOfStreets = listOfCities.getOrCreateStreets(city);
                    Houses listOfHouses = listOfStreets.getOrCreateHouses(street);
                    Floors listOfFloors = listOfHouses.getOrCreateFloors(house);
                    listOfFloors.incrementFloor(floor);
                }
            }
            reader.close();
        }
        return listOfCities;
    }

    public void checkingFileExists(String filePath) throws IOException {
        File fileToOpen = new File(filePath);

        if (!fileToOpen.exists()) {
            throw new IOException("Файл не найден.");
        }
    }
}