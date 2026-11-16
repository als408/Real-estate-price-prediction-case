# Raport z eksperymentów PricePred

## Cel i dane

Przewidujemy cenę ofertową mieszkania na rynku wtórnym na podstawie cech tabelarycznych, tytułu i opisu. To nie jest prognoza ceny transakcyjnej. Dane źródłowe zawierają 13 745 ogłoszeń; analizowany rynek wtórny obejmuje 5954 oferty.

Wspólny podział czasowy: 4758 ofert treningowych i 1196 testowych. Granica testu: 24 maja 2020 r. Podział odbywa się po pierwszej publikacji, z zachowaniem całego dnia i deduplikacją ID. Oba notebooki importują tę samą funkcję podziału.

## Przygotowanie danych

- Imputacja, skalowanie, kategorie, TF-IDF i SVD są dopasowywane wyłącznie na danych uczących danego folda, a przy refit na całym treningu.
- `params` parsujemy przed czyszczeniem HTML. Pola ceny i ceny/m² nie trafiają do cech.
- Maskujemy kwoty z walutą, dekodujemy encje i usuwamy HTML. Kwoty bez waluty lub zapisane słownie nadal wymagają kontroli.
- Powierzchnia 267 000 m² pozostaje w audycie, a jako cecha modelu staje się brakiem. Nie ustalamy nieznanej prawidłowej wartości. Jawny przedział wiarygodności to 5–2000 m².
- Połączono 13 cech GPT z pliku `llm_features_new.csv` po unikalnym ID, bez zmiany liczebności ani kolejności treningu/testu.
- Wykryto 44 ofert testowych z identycznym długim oczyszczonym opisem w treningu. To kandydaci do weryfikacji, nie potwierdzone duplikaty nieruchomości; wspólny szablon agencji także może dawać taki wynik.

## Reprezentacje i modele

1. Mediana treningowa oraz liniowe modele cech strukturalnych.
2. Ridge + jawne cechy NLP: długości tekstu, liczba cyfr, wzmianki o remoncie, balkonie, komunikacji i zieleni.
3. Ridge TF-IDF oraz Ridge łączący tekst ze strukturą, a następnie z GPT.
4. Random Forest, Extra Trees i HistGradientBoosting na identycznych cechach bez GPT i z GPT.
5. Extra Trees na strukturze, GPT i 48 składowych SVD reprezentacji TF-IDF tytułu i opisu.
6. Temporal stacking: trzy gałęzie (Ridge tekstowy, Extra Trees struktura/GPT, Extra Trees SVD/GPT) i meta-model Ridge. Cechy meta-modelu to wyłącznie predykcje OOF z wcześniejszych modeli, z góry ustalonych niezależnie od późniejszych etykiet walidacyjnych.
7. TabPFN 10.0.0 wykonano lokalnie po akceptacji licencji przez użytkownika: `TabPFNRegressor()` z domyślnymi ustawieniami, bez strojenia. Osiągnął MAE 36 409,79 PLN, RMSE 64 273,97 PLN i R² 0,794.

## Walidacja

W treningu wydzielono trzy kolejne okna czasowe: około 55–70%, 70–85% i 85–100% danych treningowych. Modele uczą się wyłącznie na wcześniejszych wierszach. Konfiguracje wybieramy według średniego MAE walidacji. Ridge wybiera alpha spośród 1 i 10. Zespoły mają po dwie konfiguracje.

Gałęzie stackingu mają stałe hiperparametry, aby uniknąć wykorzystania późniejszych wyników walidacji do konstrukcji wcześniejszych predykcji OOF. Diagnostyka meta-modelu na ostatnim oknie używa meta-modelu dopasowanego tylko na dwóch wcześniejszych oknach. Końcowy refit używa całego treningu, bez dopasowania do testowych etykiet.

## Wyniki eksploracyjne na wspólnym teście

| Model | MAE [PLN] | RMSE [PLN] | R² |
|---|---:|---:|---:|
| TemporalStack | 29,881 | 68,397 | 0.767 |
| Ridge_text_GPT | 31,646 | 63,162 | 0.801 |
| Ridge_text_struct | 32,260 | 65,147 | 0.788 |
| TabPFN_default | 36,410 | 64,274 | 0.794 |
| ExtraTrees_SVD_GPT | 37,993 | 74,495 | 0.723 |
| ExtraTrees_gpt | 39,276 | 74,045 | 0.727 |
| ExtraTrees_NLP | 40,376 | 81,490 | 0.669 |
| RandomForest_gpt | 40,590 | 79,176 | 0.687 |
| HistGradientBoosting_gpt | 41,109 | 77,588 | 0.700 |
| Ridge_text | 41,566 | 86,228 | 0.629 |
| RandomForest_base | 42,178 | 80,235 | 0.679 |
| ExtraTrees_base | 42,534 | 82,914 | 0.657 |
| HistGradientBoosting_base | 43,681 | 83,962 | 0.649 |
| Ridge_NLP | 51,881 | 86,775 | 0.625 |
| Ridge_struct | 53,665 | 87,770 | 0.616 |
| LinearRegression_base | 53,821 | 87,858 | 0.615 |
| Mediana | 77,662 | 149,649 | -0.116 |

Najniższe MAE ma TemporalStack: około 29,9 tys. PLN. Ridge tekst + struktura + GPT osiąga około 31,6 tys. PLN MAE i niższe RMSE niż stacking (63,2 wobec 68,4 tys. PLN). Nie ma więc zwycięzcy niezależnego od funkcji straty.

Dodanie GPT zmniejszyło MAE o około 3,8% dla Random Forest, 7,7% dla Extra Trees i 5,9% dla HistGradientBoosting. W prostym modelu Ridge dodanie GPT do tekstu i struktury zmniejszyło MAE z około 32,3 do 31,6 tys. PLN. Proste cechy NLP poprawiły Ridge z około 53,7 do 51,9 tys. PLN; Extra Trees na tej samej reprezentacji NLP osiągnął około 40,4 tys. PLN.

## Wyjaśnialność

Do SHAP i LIME wybrano Extra Trees z GPT według walidacji, nie testowego rankingu. SHAP ma 100 przykładów referencyjnych z treningu, a próbka wyjaśniana pochodzi z testu. Największe średnie bezwzględne wkłady mają powierzchnia, parking i liczba pokoi. To opis zachowania modelu względem wybranego tła, nie przyczynowy wpływ cechy na cenę.

LIME analizuje tę samą pierwszą ofertę testową dla trzech ziaren. Lokalny R² wynosi około 0,10–0,12: przybliżenie jest słabe i jego wag nie należy traktować jako wiarygodnego opisu modelu. Same powtórzenia nie naprawiają tej niskiej wierności. Wyjaśnienia dotyczą Extra Trees, a nie stackingu.

## Ograniczenia i dalsze potwierdzenie

- Test był wielokrotnie oglądany w trakcie projektu. Powyższe liczby są eksploracyjne; potrzebny jest nowy, nieoglądany zbiór czasowy do końcowej oceny.
- Istniejący cache GPT nie ma pełnych historycznych logów promptów. Odtworzone ID próbki zapisanej w nowym notebooku API nie przecinają obecnego testu, ale nie dowodzi to pełnej historii eksperymentów.
- Asystent przejrzał teksty pierwszych 5 z 20 przykładów treningowych w `results/llm_review_train.csv`. Zidentyfikowano pomylenie widoku z nasłonecznieniem (ID 6139961), stanu do odświeżenia z czasem remontu (ID 6098869) oraz dwie niejednoznaczności. To przegląd pomocniczy, nie niezależna ocena ekspercka; pozostałych 15 przykładów nie oceniono. Nie raportujemy accuracy ekstrakcji.
- Powtórzenia opisów i podejrzane wartości należy zweryfikować u źródła.
- Nie uruchamiano ponownej płatnej ekstrakcji, BERT/Sentence-BERT ani BERTopic.
- TabPFN jest uruchomiony. Zapisane predykcje są odtwarzane tylko przy zgodnych hashach danych źródłowych, cech GPT i kodu przygotowania; pełny refit wymaga lokalnego dostępu do wag.

## Odtwarzanie

Uruchom `uv sync`, a następnie `projekt2.ipynb` od początku w katalogu projektu. `uv sync --extra tabpfn` dodaje bonus. Główny notebook nie pobiera modeli z sieci przy domyślnych flagach.

Notebook `OpenAI_API_real_estate_ads_new.ipynb` domyślnie kontroluje cache bez wywołań API. Wywołania wymagają osobnych flag, `OPENAI_API_KEY` i świadomego wyboru pliku wyjściowego. Nowy przebieg nie dopisuje do cache o niepotwierdzonym fingerprintcie.
