# MOON: Modular Cache Coherence API for for Disaggregated Datacenter Netowrks 

Contributors: Adit Gupta, Seung-seob Lee, Anurag Khandelwal 

## Overview 
MOON is a new API that provides functionally complete primitives for cache coher- ence in a high-level language and decouples the coherence protocol from the architecture. Specifically, MOON specifies a set of function calls in python that can be used by a cache coherence developer to make any protocol desired. The function calls must be correctly implemented by an architecture developer so that the cache coherence programmer does not depend on the underlying architecture. The API’s shim layer then converts the cache coherence program into kernel code that can be plugged into the datacenter architecture. This allows for a wide array of protocols to be plugged into a large number of computer architectures. This also reduces the time to change and update cache coherence proto- cols in systems, crucial for increasing efficiency, throughput, and bandwidth utilization of datacenters.

## Key Functionalities 
- Decouple the cache coherence protocol implementation from the architecture design
- Provide a complete and correct primitive set of functions that can implement any cache coherence protocol
- Allow any cache coherence protocol to be implemented on an arbitrary architecture with simplicity. Given k cache coherence protocols and m architectures, a developer could implement km different architectures with different cache coherence protocols in O(k + m) time 

## Important Note for Datacenter Architecture Design 

Within MOON, the abstraction provided for cache coherence is split into three parts: 
- requestor
- invalidator
- directory

The requestor and invalidator are co-located in the compute blades of a datacenter, and are responsible for requesting and invalidating memory blocks for the blade’s cache (and application requests) respectively. On the other hand, the directory entity is responsible for global state management and responding to memory requests by applications/CPU's. The major benefit of this modular approach is that it decouples the separate functionalities within the compute blade from one another - the request functionality is implemented in a different module than invalidation functions. It is up to the architecture developer to fit these three "entities" into their code, but it is required that there are three separate modules for each of the entities. 

## Design Overview 
As seen in the diagram below, there are many crucial entities that are created in MOON:
- interconnect: a module to deliver messages between entities; provided by the architecture developer
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

The cache coherence developer only needs to change the match action table inside of the protocol-specific code that is written. The shim layer then generates the kernel code from the match action table and the developers simply need to plug this into the architecture modules for the requestor, invalidator, and directory 

## Usage
1. Add new subfolder to /protocol folder for your newly created protocol, xxx at the location ```/protocol/xxx```
2. Make a cache state defintion file at ```/protocol/xxx/cache_state_xxx.py```. This defines the states that are used in the protocol (variable to integer defintion). See ```/protocol/msi/cache_state_msi.py`` as an example
3. Create the ```requestor_xxx.py```, ```requestor_xxx.py```, and ```directory_xxx.py``` files inside of ```/protocol/xxx```, copying and pasting the match action table format from ```requestor_msi.py```, ```requestor_.py```, and ```directory_msi.py``` files
4. Update the match action tables of ```requestor_xxx.py```, ```requestor_xxx.py```, and ```directory_xxx.py``` in the ```/protocol/xxx``` subfolder, using functions that exist in ```framework/requestor/requestor_arch.py```, ```framework/directory/directory_arch.py```, ```framework/invalidator/invalidator_arch.py```, and ```framework/interconnect/interconnect.py``, which are the sets of valid 
5. Create tests in ```/protocol/xxx/tests_xxx.py```. You can use the ```framework/test/test_environment.py``` file to help create tests environments of controllers to check the validity of state transitions in the protocol developed. See ```/protocol/msi/tests_msi.py``` as an example
6. Run shim layer to generate kernel code using ```/generator/python_to_c.py```
