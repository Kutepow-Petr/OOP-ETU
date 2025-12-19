import requests
from Product import Product

class OpenFoodFacts:
    URL = "https://world.openfoodfacts.org/cgi/search.pl"

    PARAMS = {
            'search_terms': "",
            'json': 1,
            'page_size': 20,
            'lc': 'ru',
            'nutriment_proteins': 1,
            'nutriment_fat': 1,
            'nutriment_carbohydrates': 1,
            'sort_by': 'unique_scans_n',
            'fields': 'product_name,brands,nutriments'
        }

    def search(self, product_name: str) -> list:
        self.PARAMS['search_terms'] = product_name

        try:
            response = requests.get(self.URL, params=self.PARAMS, timeout=20)
            response.raise_for_status()

            valid_products = []
            for product in response.json().get('products', []):
                try:
                    parsed_product = self._parse_product(product)
                    if parsed_product:
                        valid_products.append(parsed_product)  
                except:
                    continue

            return valid_products
        except:
            return []
    
    def _parse_product(self, product_data: str) -> Product:
        name = product_data.get('product_name', '').strip()
        if not name or len(name) < 2:
            return None
        
        brand = product_data.get('brands', '').strip()
        if brand and brand.lower() not in name.lower():
            name += f" ({brand})"
        
        nutriments = product_data.get('nutriments', {})
        proteins = round(nutriments.get('proteins_100g', 0), 1)
        fats = round(nutriments.get('fat_100g', 0), 1)
        carbs = round(nutriments.get('carbohydrates_100g', 0), 1)

        if proteins > 100 and fats > 100 and carbs > 100 \
            or proteins <= 0 and fats <= 0 and carbs <= 0:
            return None
        
        calories = round(nutriments.get('energy-kcal_100g'), 1)
        return Product(
            name=name,
            calories=calories,
            proteins=proteins,
            fats=fats,
            carbs=carbs
        )