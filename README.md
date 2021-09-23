# cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes


** **

## Project Description Template

The purpose of this Project Description is to present the ideas proposed and decisions made during the preliminary envisioning and inception phase of the project. The goal is to analyze an initial concept proposal at a strategic level of detail and attain/compose an agreement between the project team members and the project customer (mentors and instructors) on the desired solution and overall project direction.

This template proposal contains a number of sections, which you can edit/modify/add/delete/organize as you like.  Some key sections we’d like to have in the proposal are:

- Vision: An executive summary of the vision, goals, users, and general scope of the intended project.

- Solution Concept: the approach the project team will take to meet the business needs. This section also provides an overview of the architectural and technical designs made for implementing the project.

- Scope: the boundary of the solution defined by itemizing the intended features and functions in detail, determining what is out of scope, a release strategy and possibly the criteria by which the solution will be accepted by users and operations.

Project Proposal can be used during the follow-up analysis and design meetings to give context to efforts of more detailed technical specifications and plans. It provides a clear direction for the project team; outlines project goals, priorities, and constraints; and sets expectations.

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

Within scope: 
- Selecting size of regions that contain fingerprints
- Testing algorithms for intelligent assignment of regions to dedup pods


** **

## 4. Solution Concept

This section provides a high-level outline of the solution.

Global Architectural Structure Of the Project:

This section provides a high-level architecture or a conceptual diagram showing the scope of the solution. If wireframes or visuals have already been done, this section could also be used to show how the intended solution will look. This section also provides a walkthrough explanation of the architectural structure.

 

Design Implications and Discussion:

This section discusses the implications and reasons of the design decisions made during the global architecture design.

## 5. Acceptance criteria

Deliver a repeatable test configuration that can be used for different algorithms. 
- Scalable for testing cloud workload
- Uses containers and kubernetes to scale independent of hardware 

Implement two (stretch goal four) distribution algorithms  
- Collect data on optimal size of regions for each algorithm  
- Collect data on rate of duplication for each algorithm

## 6.  Release Planning:

Release planning section describes how the project will deliver incremental sets of features and functions in a series of releases to completion. Identification of user stories associated with iterations that will ease/guide sprint planning sessions is encouraged. Higher level details for the first iteration is expected.

Detailed user stories and plans are on the Taiga board: https://tree.taiga.io/project/amanbatra-cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes

Release #1 (due by Week 5):

…

Release #2 (due by Week 7):

…

Release #3 (due by Week 9):

…

Release #4 (due by Week 11):

…

Release #5 (due by Week 13):


** **

## General comments

Remember that you can always add features at the end of the semester, but you can't go back in time and gain back time you spent on features that you couldn't complete.

** **

For more help on markdown, see
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

In particular, you can add images like this (clone the repository to see details):

![alt text](https://github.com/BU-NU-CLOUD-SP18/sample-project/raw/master/cloud.png "Hover text")


