
** **
## CS6620-Fall21 Intelligent Assignment of Data to Dedup Nodes  

** **

## 1.   Vision and Goals Of The Project:

We will create a storage simulator that will run as multiple containers in an orchestration environment. 
The simulator will process a prepared dataset of hashes (data segment fingerprints). The network of containers 
forms a distributed key-value store where checking of fingerprints takes place. It is necessary to trade-off 
leveraging parallelism for throughput of data vs storage of duplicate data. We want to maximize space saving 
while achieving balanced use of the dedup nodes. 

The main output of this project will be collection of performance data. We will collect data on several 
configurations of our file storage simulator. Deduplication space savings will be measured for each node 
and across the cluster and compute efficiency will be considered. Configuration variations:  
 - scale up to ~1,000 dedup domains
 - implement several algorithms<sup>[1](#bottleneck)</sup> for intelligent assignment of regions to pods
 - compare settings for region size (~1MB-8MB)     

We will draw conclusions on how to balance the trade-offs of data deduplication in a cloud environment. 

** **

## 2. Background:  

Data deduplication techniques are crucial for modern cloud-scale storage systems. Key attributes<sup>[2](#tradeoffs)</sup> required include:
- high throughput, typically over 100 MB/sec to complete a backup quickly  
- high compression of data by deduplication to make disk cost equivalent to tape storage  
- use of commodity hardware (cannot store entire dedup index in RAM)

![Conceptual Diagram](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/dedup_system.png)

Fingerprints are hashes representing a unique segment of data and are used for identifying duplicate segments. An incoming data 
stream is checked against a key-value store so that recognized fingerprints do not need to be stored again. 

Fingerprinted segments are grouped into regions. These regions act as a higher level hash that can be checked 
once to avoid inspecting each segment fingerprint within the region. Finding duplicated regions is more efficient 
than finding each duplicated segment separately.   

The Key-Value store contains the collection of fingerprints (which are the keys) which points to the actual chunks of data stored.

To increase data throughput, a dedup system can be sharded into multiple nodes. Our solution for this is described in [Section 5](#5-solution-concept). Each node would contain a portion of file 
metadata and key value store necessary for duplicate checking.

** **

## 3. Users/Personas Of The Project:

Enterprise data storage architects need performance data on proposed improvements to data storage techniques.   

Data center operators need to minimize storage of duplicate data to minimize cost. 

- Team users, the files systems shared by a big team will be benefited from this project. If multiple versions of files are existing, and we want to reduce the memory usage on duplicate data. Also, as data is frequently modified, the inline back of the data is necessary with efficient performance. An intelligent assignment of pods will be helpful for such users for improved performance. 
- Virtual Desktop Deployment (VDI), the organization which must manage multiple VDI, this project will be applicable as it will automatically scale the VDIs and their data backups. 
- In virtualized backup applications, such as cloud storage infrastructures, this project will be helpful for such organizations in intelligently backing up the data with better performance. 


** **

## 4.   Scope and Features Of The Project:

Out of scope:
- Data ingestion (segmentation and fingerprinting)
- Creation of fingerprint trace datasets (will use existing data set)

Within scope: 
- Creation of cloud native, scalable, containerized, file storage simulator
- Selecting size of regions that group together fingerprints
- Testing algorithms for intelligent assignment of regions to dedup pods

** **

## 5. Solution Concept

Global Architectural Structure Of the Project:  
![Conceptual Diagram](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/conceptual-diagram.png)

We will use fingerprint data from https://tracer.filesystems.org/ representing real world storage of files. 

We will create a containerized, parallel version of the system described in [Section 2](#2-background). 

The storage simulator will be made up of client/server modules...  

Frontend (FE) Module
 - assign fingerprints to regions 
 - assign regions to dedup nodes
 - gRPC Client code
 - instrumentation for performance metrics

Backend (BE) Module
 - Lookup into FP index (KV store)
 - Insert into FP index (KV store)
 - gRPC server code
 - instrumentation for performance metrics
 
The algorithms we plan to use will be manipulating the fingerprint segment metadata and the region metadata 
mapping segments->regions. Algorithms will smartly assign regions to dedup pods, which each contain multiple 
dedup domains. It will be necessary to allow some duplication across pods to avoid strictly checking every 
fingerprint against a single global key store. We will be comparing various algorithms and evaluating the amount 
of duplication that occurs.  We will also investigate manipulating region size to find the optimal performance.

## 6. Acceptance criteria

Deliver a repeatable test configuration that can be used for different algorithms. 
- Scalable for testing cloud workload
- Uses containers and kubernetes to scale independent of hardware 

Implement two algorithms for creation of regions. 
 - "Variable length segments are essential for deduplication of the shifted content of backup images"<sup>[1](#bottleneck)</sup>
 - "A well-designed duplication storage system should have the smallest segment size possible given the throughput and capacity requirements"<sup>[1](#bottleneck)</sup>

Implement two distribution algorithms of regions to domains.
- Collect data on optimal size of regions for each algorithm  
- Collect data on rate of duplication for each algorithm. The ideal case of deduplication would be implemented by directing everything to a single dedup domain, so we will compare to this baseline.
- Collect data on how balanced usage of the dedup domains are. Goal is to minimize skew.
- Collect data on compute efficiency for each algorithm

## 7.  Release Planning:

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

## 8. References
<a name="bottleneck">1</a>: https://www.usenix.org/conference/fast-08/avoiding-disk-bottleneck-data-domain-deduplication-file-system   
<a name="tradeoffs">2</a>: https://www.usenix.org/conference/fast11/tradeoffs-scalable-data-routing-deduplication-clusters  


