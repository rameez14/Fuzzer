### Fuzzer implementation

### Introduction 

The purpose of this assignment was to implement a small fuzzer that can identify SQL injections.The assignment was to determine and take into consideration dynamic SQLi testing using static payloads and using pre-defined payloads. I was also required to test pages that require authentication. 

### Implementation 

I managed to implement SQL injection. I managed to find SQL injections login and the grades pages as I believe there was no other places where a SQL injection that could be used. I also took into consideration endpoints. I also looked at params and data. The differences between these two are that params form the query string that contains the the URL whereas, data is used for the body of a request alongside its files. I have also implemented a session variable which can remember data from requests to requests mainly for each user. 

