import socket
import time
import matplotlib.pyplot as plt

#defining maximum hops before starting to ping the next server, the port as mentioned in the question 
maximumHops=30
port=33434

#question expects maximum length of the response to be 1500 and the payload to be 1472 and UDP header to be 8 bytes
responseLength=1500

#message data to be sent as asked in the question
data="measurement for class project. questions to student txr177@case.edu or professor mxr136@case.edu"

#payload=str(data+'a'*(1472-len(data))).encode('ascii')

#payload = bytes(data + 'a'*(1472 - len(data)))

def numberOfHops(serverIP):
    for i in range(1,maximumHops):
        print("pinging the server with current ttl = ",i)
        #Initializing both start and the end time stamps to calculate the RTT, overwriting the end time after the response is recieved from the ping function
        startTime=time.time()
        endTime=time.time()
        #calling the method ping Server defined below
        currentAddress=pingServer(serverIP,i)

        if currentAddress.find(serverIP)!=-1:
            #when the current hop address is same as the server real IP address, changing the end time to the current time stamp
            endTime=time.time()
            print("reached the server already!")
            #number of hops to be plotted on x axis and the RTT on the y axis as per the question
            #sending x,y and the domain name
            return([i,endTime-startTime,serverDomain])

def pingServer(serverIP,currentTimeOut):
    #defining sender and receiver objects as recommeded in the question, using RAW Sockets
    sender=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL,currentTimeOut)

    receiver=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    #binding to the port
    receiver.bind(("",port))

    try:
        #sending the payload to the server IP address
        sender.sendto(b'measurement for class project. questions to student txr177@case.edu or professor mxr136@case.edu',(serverIP,port))

        #receiving the response and limiting the responseLength as described in the question
        data,currentAddress=receiver.recvfrom(responseLength)
        #print("received data ",data)
        #print("received address ",currentAddress)
    except socket.error:
        print("Something went wrong! ",socket.error)
    finally:
        #closing the sender and the receiver connections
        sender.close()
        receiver.close()
        #returning the current hop's IP to the calling function
    return(currentAddress[0])

""" 
def generateScatterPlot(x,y,labels):
    for i in range(len(x)):
        plt.plot(x[i], y[i], 'bo')
        plt.text(x[i] * (1 + 0.05), y[i] * (1 + 0.05) , labels[i], fontsize=12)

    plt.xlim((0, maximumHops))
    plt.ylim((0, max(y)+4))
    plt.show() 
"""

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

    ans=numberOfHops(serverIP)
    x.append(ans[0])
    y.append(ans[1])
    labels.append(ans[2])

plt.scatter(x, y)
plt.show()
plt.savefig("ScatterPlotForTargets.png")

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