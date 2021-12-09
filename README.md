Final Project Demo Video (20 minute summary of project)  
https://www.youtube.com/watch?v=7JytOpo1gUY

For installation and usage directions, see README in [/simulator](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/tree/main/simulator) directory.  

** **
## CS6620-Fall21 Intelligent Assignment of Data to Dedup Nodes  

** **

## 1.   Vision and Goals Of The Project:

To create a storage simulator that will run as multiple containers in an orchestration environment. 
The simulator processes a prepared dataset of hashes (data segment fingerprints). The cluster of containers 
forms a distributed key-value store where checking of fingerprints takes place. The purpose of the simulator is 
to run many algorithms and configurations in order to investigate trade-offs between leveraging parallelism for 
throughput of data vs minimizing storage of duplicate data. We want to maximize space saving 
while achieving balanced use of the dedup nodes. 

The main output of this project is performance data and statistics. Deduplication space savings was measured for 
each domain, each cluster pod, and overall. Configuration variations include:  
 - varying from 1 to 1000+ dedup domains
 - varying from 1MB to 8MB region size (a region is a unit of deduplication work)  
 - several algorithms for intelligent assignment<sup>[1](#bottleneck)</sup> of regions to pods 
 - several algorithms for region creation: fixed-size, content-defined chunking<sup>[2](#content_defined)</sup>, TTTD<sup>[3](#TTTD)</sup>, AE<sup>[4](#ae_regions)</sup>
 

We will draw conclusions on how to balance the trade-offs of data deduplication in a cloud environment. 

** **

## 2. Background:  

Data deduplication techniques are crucial for modern cloud-scale storage systems. Key attributes<sup>[5](#tradeoffs)</sup> required include:
- high throughput, typically over 100 MB/sec to complete a backup quickly  
- high compression of data by deduplication to make disk cost equivalent to tape storage  
- use of commodity hardware (cannot store entire dedup index in RAM)

![Conceptual Diagram](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/dedup_system.png)

Fingerprints are hashes representing a unique segment of data and are used for identifying duplicate segments. An incoming data 
stream is checked against a key-value store so that recognized fingerprints do not need to be stored again. 

Fingerprinted segments are grouped into regions. These regions act as a unit of routing to distribute the work of deduplication evenly across multiple processing nodes. Regions can be created in a variety of sizes. Regions can be routed statefully based on past deduplication results, or statelessly based only on the fingerprints inside the region. 

The Key-Value store contains the collection of fingerprints (which are the keys) which points to values addressing the actual chunks of data stored.

The diagram depicts one of each component required for deduplication. To increase data throughput, multiple such systems can be run in parallel. Our simulator runs one deduplication node per OpenShift pod. Dedup domains are virtual locations used by routing algorithms to evenly distribute the deduplication work. For example a system may have 8 worker pods, 1024 dedup domains, with 128 domains per pod. Our solution for this is described in [Section 5](#5-solution-concept). 



### Region Creation Algorithms
#### What is a region: 
A region is collection of fingerprints and formation of a super chunk. It help in improving deduplication performance by reducing the time to check each chunk in the region when there no change in the chunks of particular section of data. So, we do not need to check each individual chunk when there is no modification.

1. Fixed-Size Region:

   The first and very simple region creation algorithms is to create a fixed size region, where we define a fixed size for the region say 4mb and when the region size reaches the maximum size we create the region. However, the deduplication is not bevery efficient in such regions because it does not take the contents of the chunk into consideration and any change in the overlapping chunk between two regions will replace the whole two regions(known as [bounary shift problem](#BSW)) which might cause inefficient deduplication. 

2. Content-Defined<sup>[2](#content_defined)</sup>

   In this algorithm we take actual content of the chunk into considerationWe. We define a minimum and maximum region size to avoid very small and very large region size. To check the actual content of the finegerprint(hash) of the chunk we set a fixed max value. The we perfom the bitwise operation on the hash code of the chunk with fixed mask and if the result of calculation is equal to the preset(mask) value, the cutoff point(region boundary) is set. Otherwise, we keep adding the chunk to the region until the cut-off points and repeat the process until all the chunks are assigned to the regions. 

3. Two Thresholds Two Divisors (TTTD)<sup>[3](#TTTD)</sup>

   There is a disadvantage of General content defined algorithm, since in that we do bitwise operation on a fixed mask, there might be the cases when there is no match is found with the given mask so in that case  for most of the cases this algorithm will also work like a fixed size region creation algorithm.

   So, the Two Thresholds Two Divisors (TTTD) Algorithm is improvement over Content defined region creation . This algorithm uses four parameters, the maximum threshold, the minimum threshold, the main divisor, and the second divisor, to avoid the problems boundary shift problem of the content defined algorithm and fixed size region creation algorithm.

   The maximum and minimum thresholds are used to eliminate very large-sized and very small-sized chunks in order to control the variations of region-size. The main divisor plays the same role as the content defined algorithm and can be used to make the region-size close to our expected region-size. In usual, the value of the second divisor is half of the main divisor. Due to its higher probability, second divisor assists algorithm to determine a backup breakpoint for chunks in case the algorithm cannot find any breakpoint by main
   divisor. 

4. Asymmetric Extremum algorithm (AE)<sup>[4](#ae_regions)</sup>

    Asymmetric Extremum chunking algorithm (AE), a new content defined algorithm that significantly improves the chunking throughput of the above existing algorithms while providing comparable deduplication efficiency by using the local extreme value in a variablesized asymmetric window to overcome the aforementioned boundaries-shift problem. With a variable-sized asymmetric window, instead of a fix-sized symmetric window. In this algorithms, we don't have a fixed foundry but rather we find the maximum fingerpint hash, and baased on the maximum chunk hash found till now we define the boudary for the region. This ensures that if there is any change in the chunks then the local maximum of the region of a particular region is changed for which there is any modification of chunk or insertion of new chunk. This way it ensures that the regions are replaced only wfor the regions which local maximum is changed.

    Aasymmetric local breakpoint(maxima) means that there is no fixed size boundary defined for the regions and sizes can vary based on the maximum hash value found till now while creating the regions.


#### <a name="BSW">Boundary Shifting Problem in region creation algorithms</a>: 
Region creation algorithms face the boundary shifting problem
due to the data modifications. When users only insert or delete one byte, the whole file chunking will result in two different hash values between the modified chunk and the original chunk, even if most of the data remain unchanged. In same situation, after one-byte modification happens, the fixed-size region creation will generate totally different
results for all the subsequent chunks even though most of the data in the file are unchanged. This problem is called as the boundary shifting problem. 

### Region Assignment to Domain Algorithms
#### Stateless
1. First Fingerprint     
Look at the first fingerprint within a region. Convert the first n bytes of the fingerprint to an integer. Take modulo by number of domains to get assignment.
2. Min / Max Fingerprint    
Scan first m MB of region, convert the first n bytes of each fingerprint to an integer. Take the minimum or maximum fingerprint, modulo by number of domains to get assignment.
#### Stateful
1. Stateless + Reinforcement Learning    
Any stateless algorithm can be augmented with a reinforcement learning algorithm. The algorithm learns a value function based on rewards from the amount of duplication being achieved. The algorithm has a small randomness factor so that it searches other possible region-->pod assignments for higher reward values. Rewards can be scaled to favor balanced pod usage or to favor maximum deduplication.


** **

## 3. Users/Personas Of The Project:

Enterprise data storage architects need to understand how to scale deduplication clusters to handle cloud-sized storage systems.   

Data center operators need to minimize storage of duplicate data to minimize cost. 

- Team users, the files systems shared by a big team will be benefited from this project. If multiple versions of files are existing, and we want to reduce the memory usage on duplicate data. Also, as data is frequently modified, the inline backup of the data is necessary with efficient performance. An intelligent assignment of pods will be helpful for such users for improved performance. 
- Virtual Desktop Deployment (VDI), the organization which must manage multiple VDI, this project will be applicable as it will automatically scale the VDIs and their data backups. 
- In virtualized backup applications, such as cloud storage infrastructures, this project will be helpful for such organizations in intelligently backing up the data with better performance. 


** **

## 4.   Scope and Features Of The Project:

Out of scope:
- Raw file data ingestion (segmentation and fingerprinting already done)
- Creation of fingerprint trace datasets (using existing data set)
- Rebalancing of domains between pods (future work)

Within scope: 
- Creation of cloud native, containerized, file storage simulator
- Selecting size of regions that group together fingerprints
- Testing techniques to form regions
- Testing algorithms for intelligent assignment of regions to dedup domains

** **

## 5. Solution Concept

Global Architectural Structure Of the Project:  
![Conceptual Diagram](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/conceptual-diagram.png)

We will use fingerprint data from https://tracer.filesystems.org/ representing real world storage of files.      
```
Physical size of dataset representing many TBs of logical data...   
2.879 TB : /traces/fslhomes
- 81.860 GB : /traces/fslhomes/2011-8kb-only/   
- 26.645 GB : /traces/fslhomes/2012-8kb-only/	  
- 1.287 TB : /traces/fslhomes/2012/	  
- 373.241 GB : /traces/fslhomes/2013/	  
- 1.120 TB : /traces/fslhomes/2014/	  
- 2.102 GB : /traces/fslhomes/2015/
```

We created a containerized, parallel version of the system described in [Section 2](#2-background). 

The storage simulator is made up of a one frontend client and multiple backend server modules...  

Frontend (FE) Module
 - assign fingerprints to regions 
 - assign regions to dedup domains
 - gRPC Client code
   * send regions to backend pod
   * recieve acknowledgement with performance, deduplication and balance metrics

Backend (BE) Module
 - Lookup into FP index (KV store)
 - Insert into FP index (KV store)
 - gRPC server code
   * recieve regions from frontend pod
   * send acknowledgement with performance, deduplication and balance metrics
 
The algorithms manipulate the fingerprint segment metadata and the region metadata 
mapping segments->regions. The algorithms smartly assign regions to dedup domains. The domains are distributed across
pods, with many domains per pod.   

It is necessary to allow some duplication across domains to avoid strictly checking every 
fingerprint against a single global key store (only 1 dedup domain). We compared various algorithms and evaluated the amount 
of duplication that occured.  We investigated manipulating region size to find the optimal performance.

## 6. Acceptance criteria

**(done)** Deliver a repeatable test configuration that can be used for different algorithms. 
- Scalable for testing cloud workload
- Uses containers and kubernetes to scale independent of hardware 

**(done)** Implement two algorithms for creation of regions. 
 - "Variable length [regions]* are essential for deduplication of the shifted content of backup images"<sup>[1](#bottleneck)</sup>
 - "A well-designed duplication storage system should have the smallest [region]* size possible given the throughput and capacity requirements"<sup>[1](#bottleneck)</sup>  
 
    \*We expect that principles found for segment formation also apply to region formation.

**(done)** Implement two distribution algorithms of regions to domains.
- **(done)** Collect data on optimal size of regions for each algorithm  
- **(done)** Collect data on rate of duplication for each algorithm. The ideal case of deduplication would be implemented by directing everything to a single dedup domain, so we will compare to this baseline.
- **(done)** Collect data on how balanced usage of the dedup domains are. Goal is to minimize skew.
- **(future work)** Evaluate the compute efficiency of each algorithm


## 7.  Results:
All of our collected data is saved in [/simulator/results](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/tree/main/simulator/results). Each experiment has a .csv with a line for each region processed. There is a [combined file](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/simulator/results/summary/combined_summary_stats.csv) with summary statistics. And a directory containing overall results for each dataset at [/simulator/results/summary_plots](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/tree/main/simulator/results/summary_plots)   

##### Findings:
As expected content defined algorithms worked better than the fixed region ones. On Q-learning we found that although the total dedup took a hit, the skew across the pods was better. Listed down are the best performing configs when it came to total deduplication.
- Pods : 8; Domains : 1024 per pod; Region Creation Alogrithm : Content Defined; Average region size : 8MB; max_size : 12MB; min_size : 4; Assignment = Max FingerPrint Total Dedup : 19.8. Good dedup, but distribution unbalanced because of large number of domains.
- Pods : 8; Domains :16/pod; Region Creation Algorithm: TTTD; Average region size : 8MB; min region size : 	4MB; 	max region size : 12MB; Assignment Algorithm : Max Fingerprnt; Total Dedup : 20. Great overall performance and balance of distribution across the pods.
- Pods :8; Domains : 128/pod; Region creation algo : TTTD; Average Region size : 8MB; min region size : 	4MB; 	max region size : 12MB; Assignment Algorithm : Max Fingerprnt; Total Dedup : 19.8. Great overall performance and balance of distribution across the pods.
- Pods : 8; Domains : 16/pod; Region creation algorithm : CONTENT-DEFINED; Average region size : 8MB; 	min region size : 	4MB; 	max region size : 12MB; Assignment Algo : MAX_FINGERPRINT; Total dedup : 20.2. Great overall performance and balance of distribution across the pods, with a few hotspots where the data is routed to.


## 8.  Releases:

Detailed user stories and plans are on the [Taiga board](https://tree.taiga.io/project/amanbatra-cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes):

Week 5: Oct 4 - 8 Sprint 1 Demo  
 - Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_1.mp4)
 - met with project mentors to understand the problem and read relevant papers   
 - got familiar with project technologies (OpenShift, gRPC, etc)    
 - learned how to read the trace files dataset    

Week 7: Oct 18 -21 Sprint 2 Demo  
 - Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_2.mp4)
 - implemented fixed region formation    
 - implemented first fingerprint routing    
 - got a gRPC demo working    

Week 9: Nov 1 - 5 Sprint 3 Demo  
 - Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_3.mp4)
 - ran code on OpenShift for first time   
 - connected frontend and backend apps with gRPC    
 - replaced in-memory KV store with RocksDB   

Week 11: Nov 15 - 19 Sprint 4 Demo
 - Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_4.mp4)
 - decided on statistics and data to be collected   
 - added use of persistent storage on OpenShift for trace files & logs    
 - added support for running multiple backend pods
 - added reinforcement learning routing algorithm   
 - added TTTD region creation algorithm 

Week 13: Nov 29 - Dec 3 Sprint 5 Demo
- Video: [download MP4](https://github.com/yrrah/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes/blob/main/report_5.mp4)  
- added AE region creation algorithm
- added min/max fingerprint routing algorithms
- collected experiment results

Week 14: Dec 8th Final Demo
- Video: https://www.youtube.com/watch?v=7JytOpo1gUY

** **


## 9. References
<a name="bottleneck">1</a>: [Benjamin Zhu, Kai Li, and Hugo Patterson. 2008. Avoiding the disk bottleneck in the data domain deduplication file system. In Proceedings of the 6th USENIX Conference on File and Storage Technologies (FAST'08). USENIX Association, USA, Article 18, 1–14.](https://www.usenix.org/conference/fast-08/avoiding-disk-bottleneck-data-domain-deduplication-file-system)        

<a name="content_defined">2</a>: [C. Zhang, D. Qi, W. Li and J. Guo, "Function of Content Defined Chunking Algorithms in Incremental Synchronization," in IEEE Access, vol. 8, pp. 5316-5330, 2020, doi: 10.1109/ACCESS.2019.2963625.](https://ieeexplore.ieee.org/document/8949536)        

<a name="TTTD">3</a>: [Chang, BingChun. (2009). A running time improvement for two thresholds two divisors algorithm.](https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=1041&context=etd_projects)   

<a name="ae_regions">4</a>: [Y. Zhang et al., "AE: An Asymmetric Extremum content defined chunking algorithm for fast and bandwidth-efficient data deduplication," 2015 IEEE Conference on Computer Communications (INFOCOM), 2015, pp. 1337-1345, doi: 10.1109/INFOCOM.2015.7218510.](https://ieeexplore.ieee.org/document/7218510)      

             

<a name="tradeoffs">5</a>: [Wei Dong, Fred Douglis, Kai Li, Hugo Patterson, Sazzala Reddy, and Philip Shilane. 2011. Tradeoffs in scalable data routing for deduplication clusters. In Proceedings of the 9th USENIX conference on File and stroage technologies (FAST'11). USENIX Association, USA, 2.](https://www.usenix.org/conference/fast11/tradeoffs-scalable-data-routing-deduplication-clusters)          

<a name="dedup_survey">6</a>: [Jannen, William. “Deduplication: Concepts and Techniques.” (2020).](http://www.cs.williams.edu/~jannen/teaching/s20/cs333/meetings/dedup-survey.pdf)
