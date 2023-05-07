# MOON: Modular Cache Coherence API for for Disaggregated Datacenter Netowrks 

Contributors: Adit Gupta, Seung-seob Lee, Anurag Khandelwal 

## Overview 
MOON is a new API that provides functionally complete primitives for cache coher- ence in a high-level language and decouples the coherence protocol from the architecture. Specifically, MOON specifies a set of function calls in python that can be used by a cache coherence developer to make any protocol desired. The function calls must be correctly implemented by an architecture developer so that the cache coherence programmer does not depend on the underlying architecture. The API’s shim layer then converts the cache coherence program into kernel code that can be plugged into the datacenter architecture. This allows for a wide array of protocols to be plugged into a large number of computer architectures. This also reduces the time to change and update cache coherence proto- cols in systems, crucial for increasing efficiency, throughput, and bandwidth utilization of datacenters.

## Key Functionalities 
- Decouple the cache coherence protocol implementation from the architecture design
- Provide a complete and correct primitive set of functions that can implement any cache coherence protocol
- Allow any cache coherence protocol to be implemented on an arbitrary architecture with simplicity. Given k cache coherence protocols and m architectures, a developer could implement km different architectures with different cache coherence protocols in O(k + m) time 

## Design Overview 
As seen in the diagram below, there are many crucial entities that are created in MOON:
- interconnect: a module to deliver messages between entities; provided by the archi- tecture developer
- requestor, invalidator, and directory arch(itecture) files: definitions of functions that must be implemented in kernel code by architecture developer
- protocol specific files for requestor, invalidator, and directory: implementation of cache coherence protocol (i.e. MSI, MOESI, etc.) for each entity using functions defined in arch files
- requestor, invalidator, and directory class files: initializes match action table and inherits run entity
- run entity: a class that acts as “main” function. Calls functions that are in the match action table of each entity upon receiving a message
- shim layer: module that generates kernel code given all high-level language files completed
- kernel files for requestor, invalidator, and directory: output code from shim layer which is in the language of choice of architecture (developer choice)

<p align = "center">
<img src = "images/moon_overview.png" width="60%" height="30%">
</p>
<p align = "center">
Figure 1: Diagram of MOON API
</p>

## Usage

