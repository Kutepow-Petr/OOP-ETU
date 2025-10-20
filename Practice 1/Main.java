import java.util.Scanner;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        try {
            Scanner input = new Scanner(System.in);
            String searchQuery = "";

            while (true) {
                System.out.printf("\n\u001B[47m\u001B[30mВведите запрос для поиска статей в Wikipedia или напишите \"exit\"/\"выход\", чтобы выйти_\u001B[0m");
                searchQuery = input.nextLine();

                if (searchQuery.equals("exit") || searchQuery.equals("выход")) {
                    break;
                }

                List<Article> articles = WikipediaSearcher.searchWikipedia(searchQuery);

                if (articles.isEmpty()) {
                    System.out.printf("Статьи по запросу \"%s\" не найдены.\n", searchQuery);
                } else {
                    System.out.printf("Найденные статьи:\n");
                    for (int i = 0; i < articles.size(); i++) {
                        System.out.printf("\t%d. %s\n", (i + 1), articles.get(i).getName());
                    }

                    while (true) {
                        System.out.printf("\u001B[47m\u001B[30mВведите номер статьи для открытия в браузере_\u001B[0m");
                        int choice = Integer.parseInt(input.nextLine()) - 1;

                        if (choice >= 0 && choice < articles.size()) {
                            WikipediaSearcher.openArticleInBrowser(articles.get(choice));
                            break;
                        } else {
                            System.out.printf("\u001B[31mНеверный номер статьи.\u001B[0m\n");
                        }
                    }
                }
            }
        } catch (Exception error) {
            System.err.printf("Произошла ошибка: %s\n", error.getMessage());
        }
    }
}