
** **

# Intelligent Assignment of Data to Dedup Nodes  
## CS6620-Fall21  

** **

## 1.   Vision and Goals Of The Project:

Setup a distributed file storage test bed.   

Collect data on deduplication performance of several configurations of a distributed file storage test bed.   
  - compare algorithms for intelligent assignment of regions to dedup pods   
    (apply algos tried on cluster computing at cloud scale)  
  - compare settings for region size    

Draw conclusions on how to balance computational effort vs storage of duplicate data

## 2. Users/Personas Of The Project:

Enterprise data storage architects need performance data on proposed improvements to data storage techniques.   
Data center operators need to minimize storage of duplicate data to minimize cost. 

** **

## 3.   Scope and Features Of The Project:

Out of scope:
- Data ingestion (segmentation and fingerprinting)
- Creation of fingerprint trace datasets (will use existing data set)

Within scope: 
- Selecting size of regions that group together fingerprints
- Testing algorithms for intelligent assignment of regions to dedup pods


** **

## 4. Solution Concept

Global Architectural Structure Of the Project:

![Conceptual Diagram](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/conceptual-diagram.png)

We will use fingerprint data from https://tracer.filesystems.org/ representing real world storage of files. The fingerprints are hashes representing a unique segment of data and are used to identify duplicate segments. We will not be manipulating the data itself (data ingest is out of scope of the project).   

Fingerprinted segments are grouped into regions. These regions act as a higher level hash that can be checked once to avoid inspecting each segment fingerprint within the region. Finding duplicated regions is more efficient than finding each duplicated segment separately.   

The Dedup pods represent the Deduplication nodes where the region metadata are stored.  
The Key-Value store contains a collection of fingerprints (which are the keys) which points to the actual chunks of data stored.  
  
The algorithms we plan to use will be manipulating the fingerprint segment metadata and the region metadata mapping segments->regions. Algorithms will smartly assign regions to dedup pods, which each contain multiple dedup domains (VMs). It will be necessary to allow some duplication across pods to avoid strictly checking every fingerprint against a single global key store. We will be comparing various algorithms and evaluating the amount of duplication that occurs.  We will also investigate manipulating region size to find the optimal performance. 
## 5. Acceptance criteria

Deliver a repeatable test configuration that can be used for different algorithms. 
- Scalable for testing cloud workload
- Uses containers and kubernetes to scale independent of hardware 

Implement two (stretch goal four) distribution algorithms  
- Collect data on optimal size of regions for each algorithm  
- Collect data on rate of duplication for each algorithm

## 6.  Release Planning:

Detailed user stories and plans are on the Taiga board: https://tree.taiga.io/project/amanbatra-cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes

Release #1(due by Week 5):  
Test bed established and validated to be ready for algorithm testing. 


Release #2:

…

Release #3:

…

Release #4:

…

Release #5:


** **

