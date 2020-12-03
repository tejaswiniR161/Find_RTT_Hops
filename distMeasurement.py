import socket
import time
import select
import struct
import matplotlib.pyplot as plt

#defining maximum hops before starting to ping the next server, the port as mentioned in the question 
maximumHops=40
port=33434

#question expects maximum length of the response to be 1500 and the payload to be 1472 and UDP header to be 8 bytes
responseLength=1500

#message data to be sent as asked in the question
data="measurement for class project. questions to student txr177@case.edu or professor mxr136@case.edu"

#payload=str(data+'a'*(1472-len(data))).encode('ascii')

#payload = bytes(data + 'a'*(1472 - len(data)),encoding="ascii")
payload=bytes(data + 'a'*(1472 - len(data)),encoding="ascii")

def pingServer(serverIP,currentTimeOut):
    #defining the start time to calculate the RTT for the current ping
    startTime=time.time()

    #defining sender and receiver objects as recommeded in the question, using RAW Sockets
    sender=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL,currentTimeOut)
    receiver=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    #binding to the port
    receiver.bind(("",port))
    #declaring the end time to calculate the RTT; this is overwritten later when the response from the server is received
    endTime=time.time()

    try:
        #sending the payload to the server IP address
        sender.sendto(payload,(serverIP,port))
        
        receivedData=select.select([receiver],[],[],currentTimeOut)

        #checking if response was received before the maximumHops limit was reached; return [0] to indicate timeOut, the return data is handled by the caller
        if receivedData[0]==[]:
            return([0])

        #receiving the response and limiting the responseLength as described in the question
        data,currentAddress=receiver.recvfrom(responseLength)
        #IP of the endpoint thats end the ICMP packet will be in the 0th index
        currentAddressIP=currentAddress[0] 

        if currentAddressIP.find(serverIP)!=-1:
            #overwitting the end time variable with the current time stamp to calculate the RTT
            endTime=time.time()
            
            #based on the ttl in the icmp packet header, we can find the total number of hops the packet had to make
            #the number of hops left in the last icmp packet header
            ttlFromResponse=struct.unpack("!B",data[36:37])[0]
            #total hops made to reach the destination = the maximum number of hops specified in the program minus the number of hops pending in the last icm packet header
            hops=maximumHops-ttlFromResponse
            RTT=endTime-startTime
            receivedDataLength=len(data)
            return([1,hops,RTT,receivedDataLength])
        
    except socket.error:
        print("Something went wrong! ",socket.error)
    finally:
        #closing the sender and the receiver connections
        sender.close()
        receiver.close()

#declarign the coordinate value holders below, x and y list
x=[]
y=[]
labels=[]

targetsFile = open('targets.txt', 'r') 
targets = targetsFile.readlines() 
print()
for target in targets: 
    serverDomain=target.strip()
    print()
    print("--------- Pinging "+serverDomain+" ---------")
    serverIP=socket.gethostbyname(serverDomain)
    ans=pingServer(serverIP,maximumHops)
    #check if there was no response in the given time
    if ans==None or ans[0]==0:
        print("Maximum wait time exceeded. Pinging the next domain in targets.txt") 
    else:
        #printing the returned values and appending the RTT to x coordinates' list and hops to y coordinates' list respectively
        print("RTT =  ",ans[2])
        print("Hops = ",ans[1])
        print("The address on the ICMP packet header was matched with the host address of the domain")
        print("Received response length (inclusive of headers)= ",ans[3])
        x.append(ans[1])
        y.append(ans[2])

    print("---------------------------")
    print()
#generate the graph based on the x and y list values
plt.scatter(x, y)
plt.savefig("ScatterPlotForTargets.png") 
#plt.show()