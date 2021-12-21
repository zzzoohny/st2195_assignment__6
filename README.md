# st2195_assignment__6

list
1. Load and merge the datasets keeping all information available for the dates in which there is a measurement in 'fx.csv'.
2. Handle missing observations for the exchange rate, if any. This should be done replacing any missing exchange rate with latest information available. Whenever this cannot be done, the relevant entry should be removed entirely from the dataset.
3. Calculate the exchange rate return. Extend original dataset with the following variables: 'good_news' (equal to 1 when the exchange rate return is larger than 0.5%, 0 otherwise) and 'bad_news'(equal to 1 when the exchange rate return is lower than -0.5%, 0 otherwise).
4. Remove the entries for which contents has NA values. Generate and store in the csv the following tables: 
a. 'good_indicators' - with the 20 most common words (excluding articles, prepositions and similar connectors) associated with entries wherein 'good_news' is equal to 1;
b. 'bad_indicators' - with the 20 most common words (excluding articles, prepositions and similar connectors) associated with entries wherein 'bad_news' is equal to 1;
Any observation from the common words found above?

*Note that the original data should not be included in the GitHub repository, but only appropriately described and linked in the readme file. 
