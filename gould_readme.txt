###John Gould Ornithological Collection
##2015-12-04

This project was an attempt to clean up much of the records and relations between images that were the result of the original digitization project in Luna. The contents of this folder include

*2 csv files, one for books and manuscripts (gould_books_20151110.csv,gould_manuscripts_20151110.csv)

*2 python scripts used to make the MODS records (gould_books2MODS.py,gould_manuscripts2mods.py)


 This project made individual MODS records for each of the images. There are two sections of the Gould collection, Books and ManuscriptsBooks are the finished, published plates within the books. Manuscripts are the draft sketches that sometimes lead to the final prints in the books. The general structure of the records are as follows:

BOOKS

Item level plate record
|
|
|
----Host Monograph of plate (Related Item)


MANUSCRIPTS

Item level image record
|
|
|
----Final, published print of image (Related Item)


The records were created using MARC records for the books and a local database that is a relic from the first digitization phase of this project.

Personnel:

Erik Radio, radio@ku.edu - metadata processing
Micki Lubbers, mlubbers@ku.edu - image loading and management
Scott Hanrath, shanrath@ku.edu - System and workflow consulting
Karen Cook, kscook@ku.edu - Project history and special collections consulting
Miloche Kottman, mkottman@ku.edu - Cataloging consulting