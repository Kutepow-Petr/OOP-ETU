import java.awt.*;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class WikipediaSearcher {
    public static List<Article> searchWikipedia(String query) throws IOException {
        System.out.printf("Поиск...\n");
        String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8);
        String apiUrl = "https://ru.wikipedia.org/w/api.php?action=query&list=search&utf8=&format=json&srsearch=\"" + encodedQuery + "\"";

        URL url = new URL(apiUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.setRequestProperty("User-Agent",
                "WikipediaSearch");

        String response = new String(connection.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        String jsonResponse = response.toString();
        List<Article> articles = new ArrayList<>();
        extractArticlesFromJson(jsonResponse, articles);

        return articles;
    }

    private static void extractArticlesFromJson(String json, List<Article> articles) {
        Pattern titlePattern = Pattern.compile("\"title\"\\s*:\\s*\"([^\"]+)\"");
        Pattern idPattern = Pattern.compile("\"pageid\"\\s*:\\s*(\\d+)");

        Matcher titleMatcher = titlePattern.matcher(json);
        Matcher idMatcher = idPattern.matcher(json);

        while (titleMatcher.find() && idMatcher.find()) {
            articles.add(new Article(titleMatcher.group(1), Integer.parseInt(idMatcher.group(1))));
        }
    }

    public static void openArticleInBrowser(Article article) throws Exception {
        String articleUrl = "https://ru.wikipedia.org/w/index.php?curid=" + article.getId();
        URI uri = URI.create(articleUrl);
        Desktop desktop = Desktop.getDesktop();
        System.out.printf("Статья открывается...\n");
        desktop.browse(uri);
    }
}