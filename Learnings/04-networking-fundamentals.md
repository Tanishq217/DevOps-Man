# DevOps — Chapter 4: Networking Fundamentals

**Goal of this chapter:** Understand how computers communicate over networks and learn the networking concepts and commands that are essential for DevOps, cloud, troubleshooting, deployment, and interviews.

## 1. Why Networking is Important in DevOps

DevOps engineers constantly work with:

- Servers
- Cloud machines
- Containers
- APIs
- Databases
- Load balancers
- Web applications
- DNS
- Firewalls
- SSH
- HTTP/HTTPS
- Private and public networks

Almost every application eventually communicates over a network.

For example:

```
Your Laptop
     ↓
Internet
     ↓
Cloud Server
     ↓
Application
     ↓
Database
```

If networking is not understood, troubleshooting DevOps problems becomes very difficult.

For example, if an application cannot connect to a database, the problem could be:

```
Application
    ↓
Wrong IP?
    ↓
Wrong port?
    ↓
DNS problem?
    ↓
Firewall?
    ↓
Routing?
    ↓
Server down?
    ↓
Application configuration?
```

Networking knowledge helps us identify where the problem is.

## 2. Chapter 3 Review — While Loop

Before networking, we revise the previous shell scripting concepts.

A typical while loop:

```bash
while [ condition ]; do
    commands
done
```

Example:

```bash
#!/bin/bash

while true; do
    read -p "Enter a number or q to quit: " input

    if [ "$input" = "q" ]; then
        break
    fi

    echo "You entered: $input"
done
```

## 3. break

`break` immediately terminates the current loop.

Example:

```bash
while true; do

    read -p "Enter q to quit: " input

    if [ "$input" = "q" ]; then
        break
    fi

    echo "Loop is running"

done
```

If the user enters:

```
q
```

the loop stops.

## 4. continue

`continue` skips the remaining commands in the current iteration and starts the next iteration.

Example:

```bash
while true; do

    read -p "Enter something: " input

    if [ "$input" = "q" ]; then
        break
    fi

    if [ -z "$input" ]; then
        continue
    fi

    echo "You entered: $input"

done
```

Concept:

```
continue
   ↓
skip current iteration
   ↓
start next iteration
```

Whereas:

```
break
   ↓
exit loop completely
```

## 5. Regular Expressions — [0-9]+

A regular expression, commonly called regex, is a pattern used to match text.

For example:

```
[0-9]+
```

means:

```
[0-9] → a digit from 0 to 9
+     → one or more occurrences
```

So:

```
123
45
999
7
```

match the pattern.

But:

```
abc
12abc
hello
```

do not represent a string consisting entirely of digits.

## 6. Regex in Shell Scripts

One way to test a pattern in Bash is:

```bash
if [[ "$input" =~ ^[0-9]+$ ]]; then
    echo "Valid number"
else
    echo "Invalid input"
fi
```

The important pieces are:

```
^       → beginning of string
[0-9]   → digit
+       → one or more
$       → end of string
```

Therefore:

```
^[0-9]+$
```

means:

The entire input must contain one or more digits.

## 7. Complete Input Validation Example

```bash
#!/bin/bash

while true; do

    read -p "Enter a number or q to quit: " input

    if [ "$input" = "q" ]; then
        echo "Exiting..."
        break
    fi

    if [[ "$input" =~ ^[0-9]+$ ]]; then
        echo "Valid number: $input"
    else
        echo "Invalid input"
        continue
    fi

done
```

This combines:

- while
- read
- if
- break
- continue
- regex
- user input validation

These concepts are useful in automation scripts.

## 8. GitHub Assignment Workflow

For DevOps assignments, the general workflow is:

```
Create Repository
       ↓
Write Script
       ↓
Test Script
       ↓
Create README.md / notes
       ↓
git add
       ↓
git commit
       ↓
git push
```

Documentation should explain what the script does.

For example:

```markdown
# While Loop Script

This script continuously accepts user input.
It accepts numbers and exits when the user enters `q`.
Invalid input is rejected using regex validation.
```

Good DevOps documentation should explain:

- What was built
- How it works
- How to execute it
- Example output

## 9. Introduction to Networking

A computer network is a system that allows devices to communicate with each other.

Examples of networked devices:

- Laptop
- Phone
- Server
- Router
- Switch
- Cloud instance
- Database server

Communication can happen:

```
Laptop → Router → Internet → Server
```

## 10. Network Communication

When your browser accesses:

```
https://example.com
```

many things happen behind the scenes.

Simplified:

```
Browser
   ↓
DNS
   ↓
IP Address
   ↓
TCP connection
   ↓
HTTPS
   ↓
Web Server
   ↓
Response
```

Understanding these individual pieces is fundamental to DevOps.

## 11. IP Address

An IP address identifies a network interface on an IP network.

IPv4 addresses are written using four decimal numbers separated by dots.

Example:

```
192.168.1.10
```

The four sections are called octets.

```
192 . 168 . 1 . 10
 ↓     ↓    ↓    ↓
octet octet octet octet
```

Each octet ranges from:

```
0 → 255
```

Therefore the IPv4 range is:

```
0.0.0.0
```

to:

```
255.255.255.255
```

## 12. IPv4

IPv4 uses:

```
32 bits
```

There are four octets:

```
8 + 8 + 8 + 8 = 32 bits
```

Each octet represents 8 bits.

Example:

```
192.168.1.10
```

Conceptually:

```
192       168       1        10
8 bits   8 bits   8 bits   8 bits
```

## 13. Number of IPv4 Addresses

Because IPv4 contains 32 bits:

```
2^32
```

possible addresses exist.

That equals:

```
4,294,967,296
```

addresses.

Not all of these are usable as normal host addresses because some ranges have special purposes.

## 14. Public IP Address

A public IP address is an address that can be routed on the public Internet.

Example concept:

```
Your Network
     ↓
Public IP
     ↓
Internet
```

A cloud server that needs to be reachable directly from the Internet may have a public IP.

## 15. Private IP Address

Private IP addresses are used inside private networks.

Important private IPv4 ranges are:

```
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

Examples:

```
10.0.0.5
172.16.10.20
192.168.1.50
```

Private addresses are not directly routable across the public Internet.

They are commonly used inside:

- Home networks
- Company networks
- Cloud VPCs/VNets
- Internal applications

## 16. Public vs Private IP

| Feature                          | Private IP     | Public IP          |
|----------------------------------|----------------|--------------------|
| Internet routable directly       | No             | Yes                |
| Used inside private networks     | Yes            | Can be             |
| Common examples                  | 192.168.x.x    | ISP/cloud-assigned |
| Common in cloud                  | Yes            | Yes                |
| Usually needs NAT for Internet access | Often       | Not necessarily    |

## 17. IP Address Classes

Historically, IPv4 addresses were divided into classes.

The major classes discussed traditionally are:

- Class A
- Class B
- Class C

This is important for understanding older networking concepts and interview questions.

However, modern networks primarily use CIDR rather than traditional classful networking.

## 18. Class A

Traditional Class A:

```
1.0.0.0 → 126.255.255.255
```

Default subnet mask:

```
255.0.0.0
```

Equivalent CIDR:

```
/8
```

It supports a very large number of hosts per network.

## 19. Class B

Traditional Class B:

```
128.0.0.0 → 191.255.255.255
```

Default subnet mask:

```
255.255.0.0
```

CIDR:

```
/16
```

## 20. Class C

Traditional Class C:

```
192.0.0.0 → 223.255.255.255
```

Default subnet mask:

```
255.255.255.0
```

CIDR:

```
/24
```

## 21. Important Note About Classful Networking

Do not assume modern networks are designed strictly around Class A/B/C.

Modern networking uses CIDR — Classless Inter-Domain Routing.

Examples:

```
10.0.0.0/8
10.0.0.0/16
10.0.0.0/24
10.0.0.0/28
```

The /number tells us how many bits belong to the network portion.

CIDR becomes extremely important in:

- AWS VPCs
- Azure VNets
- GCP VPCs
- Kubernetes networking
- Subnetting
- Routing

## 22. Subnet Mask

A subnet mask tells us which part of an IP address represents the:

**Network**

and which part represents the:

**Host**

Example:

```
IP Address:
192.168.1.10

Subnet Mask:
255.255.255.0
```

Equivalent CIDR:

```
192.168.1.10/24
```

## 23. /24

When we see:

```
192.168.1.0/24
```

the /24 means:

```
24 bits → network portion
8 bits  → host portion
```

Because IPv4 has 32 bits:

```
32 - 24 = 8
```

host bits.

## 24. Number of Addresses in a Subnet

Formula:

```
2^(number of host bits)
```

For /24:

```
host bits = 32 - 24
           = 8
```

Therefore:

```
2^8 = 256
```

total addresses.

Traditionally, in a basic IPv4 subnet:

```
256 total
- 1 network address
- 1 broadcast address
----------------------
254 usable host addresses
```

So a /24 traditionally provides:

```
254 usable host addresses
```

## 25. Example — /26

For:

```
192.168.1.0/26
```

Host bits:

```
32 - 26 = 6
```

Total addresses:

```
2^6 = 64
```

Traditional usable hosts:

```
64 - 2 = 62
```

Therefore:

```
/26 → 64 total → 62 traditional usable hosts
```

## 26. Example — /30

```
192.168.1.0/30
```

Host bits:

```
32 - 30 = 2
```

Total:

```
2^2 = 4
```

Traditional usable:

```
4 - 2 = 2
```

This was commonly useful for small point-to-point IPv4 networks.

## 27. Quick Subnet Table

| CIDR | Host Bits | Total Addresses | Traditional Usable Hosts |
|------|-----------|-----------------|--------------------------|
| /24  | 8         | 256             | 254                      |
| /25  | 7         | 128             | 126                      |
| /26  | 6         | 64              | 62                       |
| /27  | 5         | 32              | 30                       |
| /28  | 4         | 16              | 14                       |
| /29  | 3         | 8               | 6                        |
| /30  | 2         | 4               | 2                        |

Important: The -2 rule is the traditional IPv4 subnet calculation. Some modern environments and special subnet types have different usable-address rules.

## 28. Network Address

The network address identifies the network itself.

For example:

```
192.168.1.0/24
```

The network address is:

```
192.168.1.0
```

It is not normally assigned to a host.

## 29. Broadcast Address

For a traditional IPv4 subnet, the broadcast address is used to communicate with all hosts on that subnet.

For:

```
192.168.1.0/24
```

the broadcast address is:

```
192.168.1.255
```

Therefore the traditional usable range is:

```
192.168.1.1
        ↓
192.168.1.254
```

## 30. DHCP

DHCP stands for:

**Dynamic Host Configuration Protocol**

DHCP automatically provides network configuration to devices.

Without DHCP, users might have to manually configure:

- IP address
- Subnet mask
- Default gateway
- DNS server

DHCP automates this.

## 31. DHCP Process — DORA

The standard DHCP process is remembered as:

```
D → Discover
O → Offer
R → Request
A → Acknowledgement
```

Therefore:

```
DORA
```

## 32. DHCP Discover

The client asks:

Is there a DHCP server available?

Conceptually:

```
Client
   ↓
DHCP Discover
   ↓
Network
```

## 33. DHCP Offer

The DHCP server responds with an offer.

It may include:

- IP address
- Subnet mask
- Default gateway
- DNS information
- Lease duration

## 34. DHCP Request

The client tells the DHCP server:

I want this offered configuration.

## 35. DHCP Acknowledgement

The server confirms the allocation.

The device can now use the network configuration.

Complete flow:

```
Client
  |
  | DHCP Discover
  ↓
Server
  |
  | DHCP Offer
  ↓
Client
  |
  | DHCP Request
  ↓
Server
  |
  | DHCP ACK
  ↓
Client configured
```

## 36. DNS

DNS stands for:

**Domain Name System**

DNS converts human-readable domain names into IP addresses.

Humans prefer:

```
example.com
```

Computers communicate using addresses such as:

```
93.184.216.34
```

DNS provides the mapping.

```
Domain Name
     ↓
DNS
     ↓
IP Address
```

## 37. Why DNS is Needed

Imagine having to remember an IP address for every website.

Instead of:

```
93.x.x.x
142.x.x.x
172.x.x.x
```

we use:

```
google.com
github.com
amazon.com
```

DNS makes this possible.

## 38. DNS Hierarchy

DNS is hierarchical.

Simplified:

```
Root
 ↓
Top-Level Domain
 ↓
Authoritative DNS
 ↓
Domain
```

For:

```
www.example.com
```

we can conceptually think:

```
.
↓
com
↓
example
↓
www
```

## 39. Root DNS Servers

At the top of the DNS hierarchy are the root DNS servers.

They help direct queries toward the appropriate Top-Level Domain servers.

Examples of TLDs:

```
.com
.org
.net
.in
.edu
```

## 40. TLD DNS Servers

TLD means:

**Top-Level Domain**

For:

```
example.com
```

.com is the TLD.

For:

```
example.in
```

.in is the TLD.

The TLD infrastructure helps direct the query toward the authoritative DNS server for the domain.

## 41. Authoritative DNS Server

An authoritative DNS server contains the actual DNS records for a domain.

For example, it may know:

```
example.com → IP address
```

It can also contain records such as:

- A
- AAAA
- CNAME
- MX
- TXT
- NS

We will study these in greater depth later.

## 42. DNS Resolution — Simplified

Suppose we visit:

```
www.example.com
```

Conceptually:

```
Browser
   ↓
DNS Resolver
   ↓
Root
   ↓
.com TLD
   ↓
Authoritative DNS
   ↓
IP Address
   ↓
Browser connects to server
```

In reality, caching often means the resolver does not need to contact every level for every request.

## 43. DNS Caching

DNS responses can be cached.

Caching reduces:

- Network traffic
- Lookup time
- DNS server load

Your computer, browser, router, or DNS resolver may have cached DNS information.

This is one reason DNS changes may not appear immediately everywhere.

## 44. DNS Command — nslookup

Use:

```bash
nslookup example.com
```

This asks a DNS server to resolve the domain.

You may get information including:

- Name
- Address

## 45. curl

`curl` is a command-line tool used to transfer data to or from servers.

Basic example:

```bash
curl https://example.com
```

It can retrieve the HTTP response.

## 46. Why curl is Important in DevOps

`curl` is extremely useful for:

- Testing APIs
- Testing websites
- Checking HTTP responses
- Debugging servers
- Health checks
- CI/CD scripts
- Automation

Example:

```bash
curl https://example.com
```

## 47. HTTP Status Codes with curl

You can inspect HTTP headers:

```bash
curl -I https://example.com
```

You may see:

```
HTTP/1.1 200 OK
```

Common status codes:

| Code | Meaning                |
|------|------------------------|
| 200  | OK                     |
| 201  | Created                |
| 301  | Permanent redirect     |
| 302  | Temporary redirect     |
| 400  | Bad Request            |
| 401  | Unauthorized           |
| 403  | Forbidden              |
| 404  | Not Found              |
| 500  | Internal Server Error  |
| 502  | Bad Gateway            |
| 503  | Service Unavailable    |

These become very important when troubleshooting web applications.

## 48. TCP

TCP stands for:

**Transmission Control Protocol**

TCP is a connection-oriented transport protocol.

It focuses on reliable delivery of data.

TCP provides mechanisms such as:

- Connection establishment
- Sequencing
- Acknowledgements
- Retransmission
- Flow control
- Congestion control

## 49. TCP Three-Way Handshake

TCP commonly establishes a connection using a three-way handshake:

```
Client                  Server

   SYN  ---------------->
        <---------------- SYN-ACK
   ACK  ---------------->
```

After this, the TCP connection can be used to exchange data.

## 50. Why TCP is Reliable

Suppose data gets lost.

TCP can detect the missing information and retransmit it.

Conceptually:

```
Sender
  ↓
Data
  ↓
Network
  X
Packet lost
  ↓
Receiver does not acknowledge correctly
  ↓
Sender retransmits
```

This reliability introduces overhead.

## 51. UDP

UDP stands for:

**User Datagram Protocol**

UDP is connectionless and has less protocol overhead than TCP.

It does not provide TCP-style guarantees for:

- Delivery
- Ordering
- Retransmission

Therefore UDP can be useful when speed and low overhead are more important than guaranteed delivery.

## 52. TCP vs UDP

| Feature        | TCP                          | UDP                                      |
|----------------|------------------------------|------------------------------------------|
| Connection     | Connection-oriented          | Connectionless                           |
| Reliability    | Yes                          | No delivery guarantee                    |
| Ordering       | Yes                          | No guarantee                             |
| Retransmission | Yes                          | No                                       |
| Overhead       | Higher                       | Lower                                    |
| Speed/latency  | Generally more overhead      | Generally lower overhead                 |
| Examples       | HTTPS, SSH                   | DNS, gaming, streaming/real-time traffic |

Important: Saying “UDP is always faster” is an oversimplification. UDP has lower protocol overhead and can support low-latency applications, but actual application performance depends on the protocol and implementation.

## 53. Common TCP Use Cases

TCP is commonly used by:

- HTTP/HTTPS
- SSH
- FTP
- SMTP
- Database connections

For example:

```
Browser
   ↓
TCP
   ↓
HTTPS
   ↓
Web Server
```

## 54. Common UDP Use Cases

UDP is commonly used by:

- DNS queries
- Real-time communication
- Online gaming
- Streaming-related protocols
- DHCP

Modern applications may also use protocols such as QUIC, which runs over UDP.

## 55. Ports

An IP address identifies a host/interface.

A port helps identify a service/application endpoint on that host.

Think:

```
IP address → Which machine?
Port       → Which service?
```

Example:

```
192.168.1.10:22
```

means:

```
IP   = 192.168.1.10
Port = 22
```

## 56. Port Range

TCP and UDP ports are 16-bit numbers.

Range:

```
0 → 65535
```

Important ranges:

**Well-known ports**

```
0–1023
```

**Registered ports**

```
1024–49151
```

**Dynamic/private ports**

```
49152–65535
```

## 57. Important Ports

| Port | Protocol/Service     | Common Use                  |
|------|----------------------|-----------------------------|
| 20   | FTP                  | FTP data                    |
| 21   | FTP                  | FTP control                 |
| 22   | SSH                  | Secure remote access        |
| 23   | Telnet               | Remote access, insecure     |
| 25   | SMTP                 | Email transfer              |
| 53   | DNS                  | DNS                         |
| 67   | DHCP                 | DHCP server                 |
| 68   | DHCP                 | DHCP client                 |
| 80   | HTTP                 | Web traffic                 |
| 110  | POP3                 | Email                       |
| 123  | NTP                  | Time synchronization        |
| 143  | IMAP                 | Email                       |
| 443  | HTTPS                | Secure web traffic          |
| 3306 | MySQL                | MySQL                       |
| 5432 | PostgreSQL           | PostgreSQL                  |
| 6379 | Redis                | Redis                       |
| 8080 | Common alternative HTTP | Web/application servers  |

Ports identify endpoints, and the exact service running on a port can vary. A server can be configured to run a service on a non-standard port.

## 58. Port 22 — SSH

SSH stands for:

**Secure Shell**

It is commonly used for securely accessing remote machines.

Example:

```bash
ssh username@server-ip
```

For example:

```bash
ssh ubuntu@203.0.113.10
```

SSH is extremely important in DevOps because cloud servers are frequently administered remotely.

## 59. Port 80 — HTTP

HTTP commonly uses:

```
TCP port 80
```

Example:

```
http://example.com
```

HTTP itself does not provide encryption.

## 60. Port 443 — HTTPS

HTTPS commonly uses:

```
TCP port 443
```

HTTPS means HTTP protected using TLS.

Example:

```
https://example.com
```

The communication is encrypted using TLS.

## 61. HTTP

HTTP stands for:

**Hypertext Transfer Protocol**

It is an application-layer protocol used for communication between clients and servers.

Typical flow:

```
Client
  ↓
HTTP Request
  ↓
Server
  ↓
HTTP Response
  ↓
Client
```

Example request:

```
GET /index.html
```

## 62. HTTPS

HTTPS is HTTP over a secure TLS connection.

Simplified:

```
HTTP
 +
TLS
 =
HTTPS
```

TLS provides security properties such as:

- Encryption
- Integrity protection
- Server authentication through certificates

## 63. SSL vs TLS

You may hear:

```
SSL certificate
```

In modern systems, HTTPS uses TLS, not the old SSL protocols.

People still commonly say “SSL certificate,” but technically modern HTTPS certificates are used with TLS.

## 64. TLS Certificates

When you visit:

```
https://example.com
```

the server presents a digital certificate.

The certificate helps the client verify the server's identity.

The connection is then established using cryptographic mechanisms that provide secure communication.

This helps protect against attackers trying to intercept or modify traffic.

## 65. HTTP vs HTTPS

| Feature               | HTTP                        | HTTPS                  |
|-----------------------|-----------------------------|------------------------|
| Typical port          | 80                          | 443                    |
| Encryption            | No TLS encryption           | TLS protected          |
| Server authentication | No TLS certificate          | Yes                    |
| Security              | Lower                       | Higher                 |
| Common use            | Non-sensitive/plain web traffic | Modern websites/APIs |

## 66. ICMP

ICMP stands for:

**Internet Control Message Protocol**

It is used for network-level control, diagnostic, and error-reporting purposes.

One common use is connectivity testing with:

```
ping
```

## 67. ping

Example:

```bash
ping google.com
```

`ping` commonly sends ICMP Echo Requests and waits for Echo Replies.

Conceptually:

```
Your computer
     |
     | ICMP Echo Request
     ↓
Destination
     |
     | ICMP Echo Reply
     ↓
Your computer
```

## 68. What Does ping Tell Us?

It can help determine:

- Whether a destination responds to ICMP
- Approximate round-trip time
- Packet loss

Example output may contain:

```
64 bytes from ...
time=20 ms
```

The time represents approximate round-trip time.

## 69. Important ping Limitation

If:

```bash
ping example.com
```

fails, it does not necessarily mean the server is down.

The destination may:

- Block ICMP
- Block ping through a firewall
- Have network restrictions

Therefore:

```
Ping failure ≠ guaranteed server failure
```

This is an important real-world troubleshooting point.

## 70. MAC Address

MAC stands for:

**Media Access Control**

A MAC address identifies a network interface at the Data Link layer.

A traditional MAC address is:

```
48 bits
```

Usually represented as six hexadecimal pairs.

Example:

```
00:1A:2B:3C:4D:5E
```

## 71. MAC vs IP Address

| MAC Address                          | IP Address                  |
|--------------------------------------|-----------------------------|
| Usually 48-bit                       | IPv4 is 32-bit              |
| Data Link layer                      | Network layer               |
| Associated with network interface    | Logical network address     |
| Used within local network communication | Used for IP routing      |
| Example: 00:1A:2B:3C:4D:5E           | 192.168.1.10                |

A MAC address and IP address serve different purposes.

## 72. How MAC and IP Work Together

Suppose:

```
Computer A
IP: 192.168.1.10
```

wants to communicate with:

```
Computer B
IP: 192.168.1.20
```

Within the local network, IP communication ultimately needs a link-layer destination address such as a MAC address.

Protocols such as ARP can map an IPv4 address to a MAC address on a local network.

Simplified:

```
IP Address
    ↓
ARP
    ↓
MAC Address
    ↓
Ethernet frame
```

## 73. ARP

ARP stands for:

**Address Resolution Protocol**

It is used in IPv4 local networks to discover the MAC address associated with an IP address.

Example concept:

```
Who has 192.168.1.20?
        ↓
Computer B responds:
        ↓
192.168.1.20 = AA:BB:CC:DD:EE:FF
```

This allows the sender to construct the appropriate Ethernet frame.

## 74. OSI Model

OSI stands for:

**Open Systems Interconnection**

The OSI model divides networking into 7 layers.

From bottom to top:

```
7  Application
6  Presentation
5  Session
4  Transport
3  Network
2  Data Link
1  Physical
```

## 75. OSI Layer 1 — Physical

Responsible for physical transmission.

Examples:

- Cables
- Electrical signals
- Fiber
- Radio signals
- Physical network hardware

## 76. OSI Layer 2 — Data Link

Responsible for communication over a local network/link.

Examples:

- Ethernet
- MAC addresses
- Switches
- Frames

## 77. OSI Layer 3 — Network

Responsible for logical addressing and routing.

Examples:

- IP
- Routers
- IPv4
- IPv6

## 78. OSI Layer 4 — Transport

Responsible for end-to-end transport.

Examples:

- TCP
- UDP

Ports are also associated with transport-layer communication.

## 79. OSI Layer 5 — Session

Responsible for managing communication sessions between applications.

In modern networking, session functionality may be implemented as part of application protocols rather than as a distinct layer.

## 80. OSI Layer 6 — Presentation

Concerned with how data is represented.

Examples include concepts such as:

- Encoding
- Serialization
- Encryption
- Compression

Again, modern protocols often combine these responsibilities with other layers.

## 81. OSI Layer 7 — Application

Closest to the applications users interact with.

Examples:

- HTTP
- DNS
- SMTP
- SSH

## 82. OSI Quick Revision

| Layer | Name         | Examples              |
|-------|--------------|-----------------------|
| 7     | Application  | HTTP, DNS, SSH        |
| 6     | Presentation | Encoding, encryption  |
| 5     | Session      | Session management    |
| 4     | Transport    | TCP, UDP              |
| 3     | Network      | IP, routing           |
| 2     | Data Link    | Ethernet, MAC         |
| 1     | Physical     | Cables, signals       |

A useful mnemonic from Layer 7 → 1:

```
A P S T N D P
```

## 83. TCP/IP Model

In real-world networking, the TCP/IP model is often more practical than the seven-layer OSI model.

A simplified version:

```
Application
Transport
Internet
Link
```

Mapping approximately:

```
OSI 7/6/5 → Application
OSI 4     → Transport
OSI 3     → Internet
OSI 2/1   → Link
```

## 84. Networking Command — ip addr

On Linux:

```bash
ip addr
```

or:

```bash
ip a
```

shows network interfaces and addresses.

Example information includes:

- interface name
- MAC address
- IPv4 address
- IPv6 address
- interface state

## 85. ifconfig

Another command is:

```bash
ifconfig
```

It can display network interface information.

However, on modern Linux systems, `ip` from the iproute2 suite is generally preferred.

## 86. Important Mac Note

You are using a MacBook, so some commands from Linux lectures will behave differently.

For example:

```bash
ip addr
```

is a Linux command and may not be available by default on macOS.

On macOS, commonly use:

```bash
ifconfig
```

To inspect interfaces.

For IP information, you may also use:

```bash
ipconfig getifaddr en0
```

for a particular interface.

We will distinguish Linux commands from macOS equivalents throughout the DevOps course so you don't get confused when practicing on your Mac.

## 87. hostname -I

On Linux:

```bash
hostname -I
```

can display the machine's IP addresses.

This is useful when you want to quickly identify the local IP address.

Again, this exact option is Linux-specific and may not work on macOS.

## 88. /etc/hosts

The file:

```
/etc/hosts
```

contains local hostname-to-IP mappings.

View it:

```bash
cat /etc/hosts
```

Example:

```
127.0.0.1 localhost
```

The hosts file can allow a machine to resolve a hostname locally without asking DNS.

Conceptually:

```
Hostname
   ↓
/etc/hosts
   ↓
IP address
```

If there is a matching entry, local host resolution can use it.

## 89. ip route

On Linux:

```bash
ip route
```

displays the routing table.

Example:

```
default via 192.168.1.1 dev eth0
```

This can tell us:

- Default gateway
- Routes
- Network interfaces

## 90. What is a Default Gateway?

A default gateway is where a device sends traffic when it does not have a more specific route for the destination.

Example:

```
Laptop
   ↓
Default Gateway
   ↓
Internet
```

In a home network, the router commonly acts as the default gateway.

## 91. Routing

Routing determines where packets should be sent.

Imagine:

```
Laptop
  ↓
Router A
  ↓
Router B
  ↓
Server
```

Each router makes forwarding decisions based on routing information.

## 92. ss

`ss` stands for socket statistics.

On Linux:

```bash
ss
```

It provides information about network sockets.

Useful:

```bash
ss -tuln
```

This is commonly used to inspect listening TCP/UDP ports.

Meaning:

```
-t → TCP
-u → UDP
-l → listening
-n → numeric addresses/ports
```

## 93. Why ss is Important

Suppose your application is supposed to run on port:

```
8080
```

but users cannot connect.

You can check:

```bash
ss -tuln
```

and determine whether something is actually listening on that port.

This is a very common DevOps troubleshooting technique.

## 94. traceroute

`traceroute` shows the network path toward a destination.

Linux:

```bash
traceroute google.com
```

macOS commonly has:

```bash
traceroute google.com
```

It can show intermediate network hops.

Concept:

```
Your Computer
     ↓
Hop 1
     ↓
Hop 2
     ↓
Hop 3
     ↓
Destination
```

## 95. Why traceroute is Useful

Suppose:

```bash
ping example.com
```

is slow or fails.

`traceroute` can help identify where the path appears to have problems.

However, some routers intentionally do not respond to traceroute probes, so missing responses do not automatically indicate a failure.

## 96. Authentication vs Authorization

These two concepts are extremely important in DevOps and security.

**Authentication**

Answers:

Who are you?

Examples:

- Username/password
- SSH key
- Fingerprint
- OAuth login
- MFA

**Authorization**

Answers:

What are you allowed to do?

Examples:

- Can read?
- Can write?
- Can delete?
- Can access server?
- Can deploy?

## 97. Easy Way to Remember

```
Authentication
     ↓
WHO are you?

Authorization
     ↓
WHAT can you do?
```

Example:

You log into a cloud platform.

```
Authentication
↓
Verify that you are Tanishq

Authorization
↓
Determine whether you can create a VM
```

## 98. NAT

NAT stands for:

**Network Address Translation**

NAT translates network addresses between different address spaces.

A common example is a private home network accessing the Internet.

```
Laptop
192.168.1.10
      ↓
Router/NAT
      ↓
Public IP
      ↓
Internet
```

The private IP is not directly routed across the Internet.

The router performs address translation.

## 99. Why NAT is Used

NAT is commonly used to:

- Allow private networks to access the Internet
- Reduce the need for public IPv4 addresses
- Hide internal addressing from external networks

NAT is an important concept for cloud networking.

## 100. NAT and DevOps/Cloud

In cloud environments, you will encounter concepts such as:

```
Private Subnet
     ↓
NAT Gateway
     ↓
Internet
```

For example, a private server may need to download software updates from the Internet without being directly reachable from the Internet.

This is a very common cloud architecture pattern.

## 101. Putting Everything Together

When you type:

```
https://example.com
```

many networking concepts work together.

Simplified flow:

```
              Your Computer
                    |
                    ↓
              DNS Resolution
                    |
                    ↓
              IP Address
                    |
                    ↓
              Routing
                    |
                    ↓
             TCP / QUIC
                    |
                    ↓
                 HTTPS
                    |
                    ↓
               Port 443
                    |
                    ↓
              Web Server
                    |
                    ↓
              HTTP Response
```

And if your computer is inside a private network:

```
Computer
   ↓
Private IP
   ↓
NAT / Router
   ↓
Public Internet
   ↓
Destination Server
```

This is the bigger picture you should understand rather than memorizing isolated terms.

## 102. DevOps Troubleshooting Example

Suppose your application cannot reach:

```
https://api.example.com
```

Don't randomly change things.

Troubleshoot layer by layer.

**Step 1 — DNS**

```bash
nslookup api.example.com
```

Does the domain resolve?

**Step 2 — Connectivity**

```bash
ping api.example.com
```

Does the destination respond to ICMP?

Remember: ping can fail even when the service is working.

**Step 3 — Route**

Linux:

```bash
ip route
```

Check whether the machine has an appropriate route/default gateway.

**Step 4 — HTTP/HTTPS**

```bash
curl -I https://api.example.com
```

Does the web server respond?

**Step 5 — Port**

Check whether the expected service is listening.

On Linux:

```bash
ss -tuln
```

**Step 6 — Firewall/Security**

Check:

- Local firewall
- Cloud security rules
- Network ACLs
- Security groups
- Server firewall

**Step 7 — Application**

If networking works but the application still fails, investigate:

- Application configuration
- Credentials
- Database
- Environment variables
- Application logs

This systematic approach is much better than guessing.

## 103. The Networking Troubleshooting Mental Model

Remember this:

```
DNS
 ↓
IP
 ↓
Route
 ↓
Port
 ↓
Protocol
 ↓
Application
```

For example:

```
Does the name resolve?
        ↓
Does the IP exist/reach?
        ↓
Is there a route?
        ↓
Is the port reachable/listening?
        ↓
Is the protocol working?
        ↓
Is the application healthy?
```

This mental model will become extremely useful later with:

- Docker
- Kubernetes
- AWS
- Azure
- Load balancers
- Microservices

## 104. Important Commands — Linux

| Command        | Purpose                                      |
|----------------|----------------------------------------------|
| ip addr        | Show network interfaces and IP addresses     |
| ip a           | Short form of ip addr                        |
| ifconfig       | Display interface information                |
| hostname -I    | Show local IP addresses                      |
| cat /etc/hosts | View local hostname mappings                 |
| ip route       | Show routing table                           |
| nslookup       | Perform DNS lookup                           |
| curl           | Communicate with HTTP/other servers          |
| ss             | Display socket/network information           |
| ping           | Test ICMP connectivity                       |
| traceroute     | Show path toward destination                 |

## 105. Mac vs Linux Networking Commands

Since you use a MacBook, remember that the college environment may demonstrate Linux commands that don't exist by default on macOS.

| Purpose          | Linux              | macOS                     |
|------------------|--------------------|---------------------------|
| Show interfaces  | ip addr            | ifconfig                  |
| Show IP          | hostname -I        | ipconfig getifaddr en0    |
| Routing table    | ip route           | netstat -rn               |
| DNS lookup       | nslookup           | nslookup                  |
| Test connectivity| ping               | ping                      |
| HTTP requests    | curl               | curl                      |
| Trace route      | traceroute         | traceroute                |
| Network sockets  | ss                 | lsof -i / netstat         |

Important: Don't worry if a Linux command doesn't work on your Mac. It doesn't necessarily mean you did something wrong.

Later, when we work with actual Linux servers/cloud machines, these Linux commands will become directly relevant.

## 106. Important Ports — Quick Revision

```
22    → SSH
53    → DNS
67    → DHCP Server
68    → DHCP Client
80    → HTTP
123   → NTP
443   → HTTPS
3306  → MySQL
5432  → PostgreSQL
6379  → Redis
8080  → Common application/web port
```

Most important for now:

```
22  → SSH
53  → DNS
80  → HTTP
443 → HTTPS
```

## 107. Important Definitions

**IP Address**  
Logical network address used for communication at the IP layer.

**MAC Address**  
Link-layer address associated with a network interface.

**Port**  
A transport-layer endpoint number used to identify a service/application endpoint.

**Protocol**  
A set of rules governing communication.

**DNS**  
Translates domain names into IP addresses and provides other DNS information.

**DHCP**  
Automatically provides network configuration to clients.

**TCP**  
Reliable, connection-oriented transport protocol.

**UDP**  
Connectionless transport protocol with lower overhead and no TCP-style delivery guarantees.

**ICMP**  
Protocol used for network control, diagnostics, and error reporting.

**HTTP**  
Application protocol commonly used for web communication.

**HTTPS**  
HTTP protected by TLS.

**NAT**  
Translates network addresses between address spaces.

## 108. Exam/Interview Questions

### Networking Basics

- What is a computer network?
- What is an IP address?
- What is IPv4?
- How many bits are in an IPv4 address?
- What is an octet?
- What is the range of an IPv4 octet?
- What is a public IP?
- What is a private IP?
- What are the private IPv4 ranges?
- What is a subnet mask?
- What does /24 mean?
- How do you calculate the number of hosts in a subnet?
- What is CIDR?
- What are Class A, B, and C addresses?
- Why is CIDR more relevant than traditional classes today?

### DHCP

- What is DHCP?
- Why is DHCP used?
- Explain DORA.
- What happens during DHCP Discover?
- What happens during DHCP Offer?
- What happens during DHCP Request?
- What happens during DHCP ACK?

### DNS

- What is DNS?
- Why is DNS required?
- What is DNS resolution?
- What is a DNS resolver?
- What is a root DNS server?
- What is a TLD?
- What is an authoritative DNS server?
- What is DNS caching?
- How do you perform a DNS lookup from the terminal?

### TCP/UDP

- What is TCP?
- What is UDP?
- What is the TCP three-way handshake?
- Why is TCP considered reliable?
- Why is UDP useful?
- Give examples of TCP use cases.
- Give examples of UDP use cases.
- Difference between TCP and UDP.

### Ports

- What is a port?
- What is the range of TCP/UDP ports?
- What is port 22?
- What is port 53?
- What is port 80?
- What is port 443?
- What is port 3306?
- What is port 5432?

### HTTP/HTTPS

- What is HTTP?
- What is HTTPS?
- Difference between HTTP and HTTPS.
- Why is HTTPS secure?
- What is TLS?
- What is a TLS certificate?
- Why is port 443 commonly used for HTTPS?

### ICMP

- What is ICMP?
- What does ping use?
- What information can ping provide?
- Why can ping fail even when a server is working?

### MAC

- What is a MAC address?
- How many bits is a traditional MAC address?
- Difference between MAC and IP.
- What is ARP?

### Commands

- What does ip addr do?
- What does ifconfig do?
- What does ip route show?
- What does nslookup do?
- What does curl do?
- What does ss -tuln show?
- What does traceroute do?
- What does /etc/hosts contain?

### Security

- Difference between authentication and authorization.
- What is NAT?
- Why is NAT used?
- How does NAT relate to private and public IP addresses?

## 109. Practical Checklist

Before considering Chapter 4 complete, you should be able to:

- Explain what networking is
- Explain IPv4
- Explain the 32-bit IPv4 structure
- Explain octets
- Explain public IP
- Explain private IP
- Remember private IPv4 ranges
- Understand subnet masks
- Understand CIDR
- Calculate hosts for simple IPv4 subnets
- Understand traditional Class A/B/C
- Explain DHCP
- Explain DORA
- Explain DNS
- Understand DNS hierarchy
- Explain DNS caching
- Understand TCP
- Understand UDP
- Explain TCP three-way handshake
- Explain ports
- Remember important ports
- Explain HTTP
- Explain HTTPS
- Understand TLS certificates
- Explain ICMP
- Use ping
- Understand MAC addresses
- Understand ARP
- Understand the OSI model
- Understand the TCP/IP model
- Use nslookup
- Use curl
- Understand ip addr
- Understand ip route
- Understand ss
- Understand traceroute
- Understand /etc/hosts
- Explain NAT
- Explain authentication vs authorization
- Understand basic network troubleshooting

## 110. Chapter 4 — Final Mental Map

This is the most important diagram to remember from the chapter:

```
                         NETWORKING
                              |
          +-------------------+-------------------+
          |                   |                   |
         IP                  DNS                 DHCP
          |                   |                   |
     Addressing          Name → IP          Automatic config
          |
     +----+----+
     |         |
  Public     Private
     |         |
 Internet      LAN
               |
              NAT
               |
            Internet
```

Then communication:

```
Application
    ↓
HTTP / HTTPS / DNS / SSH
    ↓
TCP / UDP
    ↓
IP
    ↓
Ethernet / MAC
    ↓
Physical Network
```

And troubleshooting:

```
DNS
 ↓
IP
 ↓
Routing
 ↓
Port
 ↓
TCP/UDP
 ↓
HTTP/HTTPS
 ↓
Application
```

The single most important DevOps idea from this chapter:

**When an application cannot communicate with another service, don't randomly change configurations. Break the problem into DNS → IP → routing → port → protocol → application and test each layer.**

That mindset will be extremely important when we reach Cloud, Docker, Kubernetes, CI/CD, and real server troubleshooting.
