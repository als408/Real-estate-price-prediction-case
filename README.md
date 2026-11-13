# PricePred — predykcja cen nieruchomości

## Pliki projektu

- `projekt2.ipynb` — wspólny podział czasowy, EDA, modele ceny oraz SHAP i LIME.
- `OpenAI_API_real_estate_ads.ipynb` — prompt do GPT, schemat cech, porównanie modeli i ekstrakcja informacji z opisów.
- `llm_features.csv` — 5954 oferty z ID i 12 cechami wyodrębnionymi przez LLM; część wartości jest brakująca.
- `real_estate_with_llm_features.csv` — dane źródłowe połączone z cechami LLM po ID (5954 wiersze, 27 kolumn).

## Zrobione

- [x] Wczytanie danych i wybór ogłoszeń z rynku wtórnego.
- [x] Jeden wspólny podział czasowy dla modeli ceny w `projekt2.ipynb`: 4758 ofert treningowych i 1196 testowych.
- [x] Dopasowywanie imputacji, kodowania kategorii, skalowania i TF-IDF wyłącznie na treningu.
- [x] Usunięcie `price_per_m` z cech modeli i pól cenowych z `params`.
- [x] EDA: braki, duplikaty, rozkłady, wartości odstające, korelacje, tekst i ceny w czasie.
- [x] Baseline przewidujący medianę ceny z treningu.
- [x] Regresja liniowa, wariant z liczbą pokoi i regresja Ridge z TF-IDF.
- [x] Drzewo regresyjne i porównanie modeli na tych samych ofertach testowych.
- [x] Globalne i lokalne wyjaśnienia SHAP oraz lokalne wyjaśnienie LIME z oceną jego wiarygodności.
- [x] Uporządkowanie notebooka: podział i przygotowanie danych → EDA → modele → wyjaśnialność; krótkie opisy w Markdownzie.
- [x] Przygotowanie promptu do GPT oraz schematu Pydantic dla 12 cech, m.in. stanu mieszkania, standardu wykończenia, parkingu, windy i komórki lokatorskiej.
- [x] Czyszczenie opisów przed ekstrakcją LLM: usuwanie HTML, dekodowanie encji i ograniczenie długości tekstu.
- [x] Porównanie odpowiedzi dwóch modeli GPT na próbce 10 ofert treningowych, wraz z analizą zgodności oraz kosztu i czasu.
- [x] Asynchroniczna ekstrakcja cech i zapis wyników dla 5954 ofert rynku wtórnego.
- [x] Połączenie cech LLM z danymi źródłowymi po ID i eksport do CSV.

## Do zrobienia

- [ ] Mocniejsze modele, np. Random Forest, Extra Trees i boosting, oraz połączenie cech liczbowych i tekstowych.
- [ ] Strojenie modeli na walidacji czasowej wewnątrz treningu, bez dobierania parametrów na teście.
- [ ] Lepsze przetwarzanie tekstu w modelach ceny: przeniesienie czyszczenia HTML do pipeline TF-IDF, parsowanie `params`, kontrola cen w opisach i tytułach oraz porównanie TF-IDF z embeddingami.
- [ ] Ręczna ocena poprawności ekstrakcji na przykładach treningowych — zgodność dwóch modeli nie jest miarą zgodności z prawdą; analiza braków i doprecyzowanie definicji cech.
- [ ] Dołączenie cech LLM do modeli ceny i porównanie wariantów z tymi cechami i bez nich na tych samych ofertach.
- [ ] Ujednolicenie podziału w obu notebookach: notebook GPT obecnie tworzy własny podział losowy, a `projekt2.ipynb` używa czasowego. Przed oceną cech LLM sprawdzić, czy przykłady użyte do wyboru promptu i schematu nie należą do końcowego testu.
- [ ] Zapewnienie odtwarzalności notebooka GPT: dodanie brakującego modułu `openai_call_metrics`, zależności oraz obsługi klucza poza Google Colab; ujednolicenie ścieżek danych i domyślne wyłączenie pełnej ekstrakcji (`RUN_FULL = False`).
- [ ] Weryfikacja podejrzanych wartości, szczególnie powierzchni 267 000 m², i duplikatów nieruchomości pod różnymi ID.
- [ ] Sprawdzenie stabilności wyjaśnień i poprawa wiarygodności LIME — obecne lokalne R² wynosi około 0,137.
- [ ] Prezentacja: cel, dane, metodologia, porównanie modeli, wyjaśnienia i wnioski.
- [ ] Raport: opis przygotowania danych, podziału, eksperymentów, wyników i ograniczeń.

Jeśli zmiany modelu wynikają z analizy obecnego testu, końcowa ocena wymaga nowego, niezależnego zbioru testowego.
