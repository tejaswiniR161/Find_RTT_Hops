import socket
import time
import select
import struct
import matplotlib.pyplot as plt

#defining maximum hops before starting to ping the next server, the port as mentioned in the question 
maximumHops=30
port=33434

#question expects maximum length of the response to be 1500 and the payload to be 1472 and UDP header to be 8 bytes
responseLength=1500

#message data to be sent as asked in the question
data="measurement for class project. questions to student txr177@case.edu or professor mxr136@case.edu"

#payload=str(data+'a'*(1472-len(data))).encode('ascii')

#payload = bytes(data + 'a'*(1472 - len(data)),encoding="ascii")
payload=bytes(data,encoding="ascii")

def pingServer(serverIP,currentTimeOut):
    #defining sender and receiver objects as recommeded in the question, using RAW Sockets
    sender=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL,currentTimeOut)

    receiver=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    #binding to the port
    receiver.bind(("",port))
    endTime=time.time()

    try:
        #sending the payload to the server IP address
        sender.sendto(payload,(serverIP,port))
        #receiving the response and limiting the responseLength as described in the question
        receivedData=select.select([receiver],[],[],currentTimeOut)
        if receivedData[0]==[]:
            return({"res":"timeOut"})

        endTime=time.time()
        data,currentAddress=receiver.recvfrom(responseLength)
        #IP of the endpoint thats end the ICMP packet will be in the 0th index
        currentAddressIP=currentAddress[0] 
        if currentAddressIP.find(serverIP)!=-1:
            print("Destination responded before timeout")

            print("data = ",data)
            #for i in data:
            icmp_header=data[20:28]
            types, hops, checksum, p_id, sequence = struct.unpack(
            'bbHHh', icmp_header)
            #decoded_data=struct.unpack("!H",data[28:30])[0]
            print("types data = ",types)
            print("code = ",hops)
            print("checksum = ",checksum)
            print("PID = ",p_id)
            print("sequence = ",sequence)
            #for i in data:
            #int_data=struct.unpack("!H",data[20:28])[0]
            #print("{int_data}") 
           
            return({"res":"success"})
        #print("received data ",data)
        #print("received address ",currentAddress)
        
    except socket.error:
        print("Something went wrong! ",socket.error)
    finally:
        #closing the sender and the receiver connections
        sender.close()
        receiver.close()

        #returning the current hop's IP to the calling function
    #return(currentAddress[0])

#declarign the coordinate value holders below, x and y list
x=[]
y=[]
labels=[]

targetsFile = open('targets.txt', 'r') 
targets = targetsFile.readlines() 
for target in targets: 
    print("For target = ",target.strip())
    serverDomain=target.strip()
    serverIP=socket.gethostbyname(serverDomain)
    print("address of the server = ",serverIP)
    ans=pingServer(serverIP,maximumHops)

    #ans=numberOfHops(serverIP)
"""
    x.append(ans[0])
    y.append(ans[1])
    labels.append(ans[2])

plt.scatter(x, y)
plt.show()
plt.savefig("ScatterPlotForTargets.png") 
"""

#print("received this from the funstion = ",ans)
#list given and issues while pinging them 
#taobao.com  - stops after 10 hops; used google.com instead
#xhamster.com works perfectly - keeping it
#washingtonpost.com - Stops after 9 hops; used yahoo.com instead
#wp.pl - Stops after 17 hops; used att.com
#mfisp.com - stops after 16 hops; used target.com
#pngtree.com - stopes fatre 22 hops
#study.com - stops after 15 hops
#mynet.com - stops after 20 hops
#eghtesadnews.com - stops after 26 hops

""" 
google.com
xhamster.com
yahoo.com
blogger.com
att.com 
youtube.com
facebook.com
googleadservices.com
gmail.com
apple.com
"""