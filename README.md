Sprint 5 Demo Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_5.mp4)   

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

Fingerprinted segments are grouped into regions. These regions act as a unit of routing to distribute the work of deduplication evenly across multiple processing nodes. Regions can be created in a variety of sizes. Regions can be routed statefully based on past deduplication results, or statelessly based only on the fingerprints inside the region. 

The Key-Value store contains the collection of fingerprints (which are the keys) which points to values addressing the actual chunks of data stored.

The diagram depicts one of each component required for deduplication. To increase data throughput, a dedup system can be replicated as multiple dedup domains. This way the domains evenly share the work of deduplication. Our solution for this is described in [Section 5](#5-solution-concept). 
** **

## 3. Users/Personas Of The Project:

Enterprise data storage architects need to understand how to scale deduplication clusters to handle cloud-sized storage systems.   

Data center operators need to minimize storage of duplicate data to minimize cost. 

- Team users, the files systems shared by a big team will be benefited from this project. If multiple versions of files are existing, and we want to reduce the memory usage on duplicate data. Also, as data is frequently modified, the inline back of the data is necessary with efficient performance. An intelligent assignment of pods will be helpful for such users for improved performance. 
- Virtual Desktop Deployment (VDI), the organization which must manage multiple VDI, this project will be applicable as it will automatically scale the VDIs and their data backups. 
- In virtualized backup applications, such as cloud storage infrastructures, this project will be helpful for such organizations in intelligently backing up the data with better performance. 


** **

## 4.   Scope and Features Of The Project:

Out of scope:
- Data ingestion (segmentation and fingerprinting)
- Creation of fingerprint trace datasets (will use existing data set)
- Rebalancing of domains between pods (future work)

Within scope: 
- Creation of cloud native, scalable, containerized, file storage simulator
- Selecting size of regions that group together fingerprints
- Testing techniques to form regions
- Testing algorithms for intelligent assignment of regions to dedup domains

** **

## 5. Solution Concept

Global Architectural Structure Of the Project:  
![Conceptual Diagram](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/conceptual-diagram.png)

We will use fingerprint data from https://tracer.filesystems.org/ representing real world storage of files.      
Physical size of hashes representing many TBs of logical data...   
2.879 TB : /traces/fslhomes
- 81.860 GB : /traces/fslhomes/2011-8kb-only/   
- 26.645 GB : /traces/fslhomes/2012-8kb-only/	  
- 1.287 TB : /traces/fslhomes/2012/	  
- 373.241 GB : /traces/fslhomes/2013/	  
- 1.120 TB : /traces/fslhomes/2014/	  
- 2.102 GB : /traces/fslhomes/2015/	  

We will create a containerized, parallel version of the system described in [Section 2](#2-background). 

The storage simulator will be made up of client/server modules...  

Frontend (FE) Module
 - assign fingerprints to regions 
 - assign regions to dedup domains
 - gRPC Client code
 - instrument for performance metrics
 - instrument for deduplication and balance metrics

Backend (BE) Module
 - Lookup into FP index (KV store)
 - Insert into FP index (KV store)
 - gRPC server code
 - instrument for performance metrics
 - instrument for deduplication and balance metrics
 
The algorithms we plan to use will be manipulating the fingerprint segment metadata and the region metadata 
mapping segments->regions. Algorithms will smartly assign regions to dedup domains. The domains are distributed across
pods, with many domains per pod.   

It will be necessary to allow some duplication across domains to avoid strictly checking every 
fingerprint against a single global key store. We will be comparing various algorithms and evaluating the amount 
of duplication that occurs.  We will also investigate manipulating region size to find the optimal performance.

## 6. Acceptance criteria

Deliver a repeatable test configuration that can be used for different algorithms. 
- Scalable for testing cloud workload
- Uses containers and kubernetes to scale independent of hardware 

Implement two algorithms for creation of regions. 
 - "Variable length [regions]* are essential for deduplication of the shifted content of backup images"<sup>[1](#bottleneck)</sup>
 - "A well-designed duplication storage system should have the smallest [region]* size possible given the throughput and capacity requirements"<sup>[1](#bottleneck)</sup>  
 
    \*We expect that principles found for segment formation will also apply to region formation.

Implement two distribution algorithms of regions to domains.
- Collect data on optimal size of regions for each algorithm  
- Collect data on rate of duplication for each algorithm. The ideal case of deduplication would be implemented by directing everything to a single dedup domain, so we will compare to this baseline.
- Collect data on how balanced usage of the dedup domains are. Goal is to minimize skew.
- Evaluate the compute efficiency of each algorithm

## 7.  Release Planning:

Detailed user stories and plans are on the Taiga board: https://tree.taiga.io/project/amanbatra-cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes

Week 5: Oct 4 - 8 Sprint 1 Demo  
 - Video: https://youtu.be/l5Yt3aOgk84 or [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_1.mp4)

Week 7: Oct 18 -21 Sprint 2 Demo  
 - Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_2.mp4)

Week 9: Nov 1 - 5 Sprint 3 Demo  
 - Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_3.mp4)

Week 11: Nov 15 - 19 Sprint 4 Demo
 - Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_4.mp4)   

Week 13: Nov 29 - Dec 3 Sprint 5 Demo
- Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_5.mp4)   

Final projects due: Dec 7th



** **

## 8. References
<a name="bottleneck">1</a>: https://www.usenix.org/conference/fast-08/avoiding-disk-bottleneck-data-domain-deduplication-file-system   
<a name="tradeoffs">2</a>: https://www.usenix.org/conference/fast11/tradeoffs-scalable-data-routing-deduplication-clusters  


