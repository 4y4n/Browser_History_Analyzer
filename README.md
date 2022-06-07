# Browser_History_Analyzer

This program uses python's built-in module SQLite3 to display each website you have accessed and the amount of times you have accessed it. The program uses simple SQL select queries to retrieve the information of each website you have visited from the database. It then parses the data, scans for duplicates and counts how many times each website was accessed. Finally, it displays the data in an the console or it plots the data using the matplotlib library. 

There are many possibilities when it comes to the SQL browser tables including date and time accessed and the origin of the visit. 

Future advancements of the program could include OOP integration to store the entire table for each website. Please let me know if you have any suggestions :)

Note: the default database it is using is for chrome, for different broswers, locate the data folder on your machine and replace the dataPath variable with its path.
