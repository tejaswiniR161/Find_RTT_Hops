import socket
import time
import matplotlib.pyplot as plt

maximumHops=30
port=33434
timeOut=30
serverDomain="google.com"

#question expects maximum length of the response to be 1500 and the payload to be 1472 and UDP header to be 8 bytes
responseLength=1500

#message data to be sent as asked in the question
data="measurement for class project. questions to student txr177@case.edu or professor mxr136@case.edu"

#payload=str(data+'a'*(1472-len(data))).encode('ascii')
payload = bytes(data + 'a'*(1472 - len(data)))

serverIP=socket.gethostbyname(serverDomain)
print("address of the server = ",serverIP)



def numberOfHops(serverIP):
    startTime=time.time()
    endTime=time.time()
    for i in range(1,maximumHops):
        print("pinging the server with current ttl = ",i)
        currentAddress=pingServer(serverIP,i)
        if currentAddress.find(serverIP)!=-1:
            endTime=time.time()
            print("reached the server already!")

            #number of hops to be plotted on x axis and the RTT on the y axis as per the question
            return([i,endTime-startTime,serverDomain])

def pingServer(serverIP,currentTimeOut):
    #defining sender and receiver objects
    sender=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL,currentTimeOut)

    receiver=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    receiver.bind(("",port))

    try:
        sender.sendto(b'measurement for class project. questions to student txr177@case.edu or professor mxr136@case.edu',(serverIP,port))
        data,currentAddress=receiver.recvfrom(responseLength)
        print("received data ",data)
        print("received address ",currentAddress)
    except socket.error:
        print("Something went wrong! ",socket.error)
    finally:
        sender.close()
        receiver.close()
    return(currentAddress[0])

def generateScatterPlot(x,y,labels):
    for i in range(len(x)):
        plt.plot(x[i], y[i], 'bo')
        plt.text(x[i] * (1 + 0.05), y[i] * (1 + 0.05) , labels[i], fontsize=12)

    plt.xlim((0, maximumHops))
    plt.ylim((0, max(y)+4))
    plt.show()

x=[]
y=[]
targets=[]
ans=numberOfHops(serverIP)
x.append(ans[0])
y.append(ans[1])
targets.append(ans[2])

generateScatterPlot(x,y,targets)
print("received this from the funstion = ",ans)