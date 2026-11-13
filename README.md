# PricePred — predykcja cen nieruchomości

Eksperymenty i EDA znajdują się w notebooku `projekt2.ipynb`.

## Zrobione

- [x] Wczytanie danych i wybór ogłoszeń z rynku wtórnego.
- [x] Jeden wspólny podział czasowy dla wszystkich modeli: 4758 ofert treningowych i 1196 testowych.
- [x] Dopasowywanie imputacji, kodowania kategorii, skalowania i TF-IDF wyłącznie na treningu.
- [x] Usunięcie `price_per_m` z cech modeli i pól cenowych z `params`.
- [x] EDA: braki, duplikaty, rozkłady, wartości odstające, korelacje, tekst i ceny w czasie.
- [x] Baseline przewidujący medianę ceny z treningu.
- [x] Regresja liniowa, wariant z liczbą pokoi i regresja Ridge z TF-IDF.
- [x] Drzewo regresyjne i porównanie modeli na tych samych ofertach testowych.
- [x] Globalne i lokalne wyjaśnienia SHAP oraz lokalne wyjaśnienie LIME z oceną jego wiarygodności.
- [x] Uporządkowanie notebooka i krótkie opisy w Markdownzie.

## Do zrobienia

- [ ] Mocniejsze modele, np. Random Forest, Extra Trees i boosting, oraz połączenie cech liczbowych i tekstowych.
- [ ] Strojenie modeli na walidacji czasowej wewnątrz treningu, bez dobierania parametrów na teście.
- [ ] Lepsze przetwarzanie tekstu: czyszczenie HTML, parsowanie `params`, kontrola cen w opisach i tytułach oraz porównanie TF-IDF z embeddingami.
- [ ] Przygotowanie zapytania/promptu do GPT do ekstrakcji cech z opisów i sprawdzenie jakości odpowiedzi na przykładach treningowych.
- [ ] Weryfikacja podejrzanych wartości, szczególnie powierzchni 267 000 m², i duplikatów nieruchomości pod różnymi ID.
- [ ] Sprawdzenie stabilności wyjaśnień i poprawa wiarygodności LIME — obecne lokalne R² wynosi około 0,137.
- [ ] Prezentacja: cel, dane, metodologia, porównanie modeli, wyjaśnienia i wnioski.
- [ ] Raport: opis przygotowania danych, podziału, eksperymentów, wyników i ograniczeń.

Jeśli zmiany modelu wynikają z analizy obecnego testu, końcowa ocena wymaga nowego, niezależnego zbioru testowego.
