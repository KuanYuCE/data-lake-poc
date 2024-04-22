## Some reference docs
* [mysql python connector](https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html)
* [Create table](https://www.w3schools.com/mysql/mysql_create_table.asp)
* [mysql-connector-python pip package](https://pypi.org/project/mysql-connector-python/)
---
[系列影片](https://www.youtube.com/watch?v=p24GiqQaA1U&list=PL-gIUf9e9CCskP6wP-NKRU9VhofMHYjcd)


## What is a Data Lake
* A repository of structured and unstructured data
* There are db and dw, but only hold structured data
    * column / row
    * 但並非所有資料都fit這種模式, 例如JSON data
* let's try to have a place where we can put all this data
    * that could be a Hadoop cluster
    * or you could be using cloud stroage like AmazonS3
* either way you are just basically having a lot of files
* but people don't want to interact with files
    * if you have a thousand files that make up a particular dataset
    * everyone has to sit there and say: ok, i'm going to scan these thousand files and they gotta list the files out..what happens if they miss a file so then you have inconsistent versions of the data
* you generally don't want to do that, you would prefer to do it in the way we do it in db, where we use things like SQL or python, and we interact not with fils but with tables
![image](https://hackmd.io/_uploads/SJoOtTqxC.png)

* Tables basically are an abstraction over the files, it can be one files or thousand of files but we just know it as a particular table and that is the purpose of a table format!

## What is a Table Format?
* An abstraction to allow multiple files on the lake to be seen as a single table.
* ![image](https://hackmd.io/_uploads/ryPp3pqgR.png)


## How do table formats work?

![image](https://hackmd.io/_uploads/Bk1Mpp9lC.png)

### Old Way: Hive / Partition Level / Directory Approach
* In the old days  you would use Hive
    * Hive tracked tables by directory
    * in the hive metastore, metadata that Hive would track it would say for table A, all the files all the data for table A is in table A folder
        * any partitions were also tracked in metastore as subfolder
        * ex: partition=1的資料會在同一folder
    * it work fine.. but the only problem is that you are only tracking it in the metadata at the partition level
        * if you want to update one record, you have to update and swap out a whole partition
        * you have to update things at one partition at a time
            * you cannot atomically swap out 2 partitions
    
    * even if we know which partition to scan, the engine would have to figure out what files are in this folder and would have to do a file listing operation and then iterate through the files to do the scanm which can be a lot more time consuming to do
    * this model works but it could be a lot of ways to be improved.


* Modern Way: Hive / Partition Level / File List Approach
    * instead of focusing on folder, it focus on specific files that make up the table where their metadata now track the indivudual files that make up the table in different way.


* Benefits of this approach:
    * time travel: capture snapshots of these metadata
    * schema evolution: oftentime the schema of the table is tracked in the metadata, the engine can then make sure to apply the schema that is in the metadata to the data
    * ACID transactionsL it will be able to consistently write the data across multiple partitions

### What is Apache Iceberg?
* A modern Data Lakehouse Format
    * a spec and libraries (what)
        1. enable the usage of iceberg in open source tool like spark
        2. allow other tools to more easily take advantage of iceberg (Java/Python API)
    * created at Netflix (who)
    * to deal with the challenges with old table formats
* standard rules of how the metadata is written and how it should be read.
* Essential component: catalog
    * to list the table. it knows which metadata file is the newest one
        * because every time the table changes, a new metadata file created.
        * and the catalog is updated with that point to metadata file the table belongs
        * that's how it maintains consistency(ACID transactions).
            * only when a transaction is complete does that update to the catalog happen.

#### Metadata File
the high-level of the table.
* what is a table schema
* what is the table's paritiong scheme
* what are the lists of historicla snapshots of the tables

#### Manifest File
![image](https://hackmd.io/_uploads/SJ7zK09gC.png)
once it reads a metadata file, it's going to determine which snapshot we are going to query. And each snapshot gets one of these maifest list files. At this point of time there's group of files called manifests. one or more manifests can make up a particular snapshot of the table.

metadata tree that apache icerberg uses.


### Apache Iceberg Features
![image](https://hackmd.io/_uploads/rJOo9Rqg0.png) 


* 透過catalog達到ACID transaction/Consistency Guarantees


![image](https://hackmd.io/_uploads/HkvlsCcx0.png)

* Schema Evolutions, 藉由metadata, 我們可以避免rewrite所有舊的data files

![image](https://hackmd.io/_uploads/Bykuo09x0.png)

* 避免file-listing operations並有效的skip data files in the table that don't need to be scanned. (less files sacnned = faster and cheaper query)
    * use metadata to plan the queries

![image](https://hackmd.io/_uploads/Hy0b2C5lA.png)

* Partition Evolution (Unique Feature in Iceberg)

![image](https://hackmd.io/_uploads/HkVtnAcl0.png)

* Hidden Partition (Unique Feature in Iceberg)
