This repository contains a Java program that demonstrates the use of vector clocks for tracking logical timestamps in a distributed system. Key features include:

- Initialization of vector clocks set to zero.
- Incrementing own logical clock with each internal event.
- Incrementing own logical clock and piggybacking vector clocks on messages sent.
- Updating vector clocks upon receiving messages by taking the maximum of received and own clocks.
- User input to specify the number of processes, events, and communication lines.
- Utilization of dictionary data structure to manage processes and their vector clock values.
- Logging and display of vector clocks before and after each communication between processes.

Example Run:
User inputs specify 3 processes. Client connections are established, and vector clocks of sender and receiver are printed before and after each communication.
