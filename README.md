# JavaGCLogParse

Here you can deploy the insrastructure to AWS usiung terraform

In this particular example we deploy 2 EC2 instances of Ubuntu-16.04 and provision 2 tomcat servers
which are placed behind the ELB.

Further you can use Python3 gclogparser.py script to look through tomcat GC log and execute some actions based on the
requested by the task requirements.

When you execute `python3 gclogparser.py` it will output help with required arguments.

Note about inventory:
it is implied that inventory is represented with text file containing tomcat cluster hosts
addresses (DNS name or IP) - one item per line.
