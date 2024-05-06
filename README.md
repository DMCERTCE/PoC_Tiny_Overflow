# PoC_Tiny_Overflow
Proof-of-concept for a heap overflow and memory leak in TinyWeb 1.94 - All versions most likely affected.

Failure to properly validate the HTTP Request Method and other request fields allows a attacker to target the server by sending a large payload.
The underlying session thread will terminate with runtime error 203 (Heap Overflow) and subsequently cause a memory leak in the main application.

It is possible to consume all 2GB of the 32-bit application leading to an all-out DoS.  

PoC Script contains code to demonstrate the attack. Notice that timeout may differ according to available bandwidth.
Script takes ip - port as argument.

I take no responsibility in how you use the supplied code. 

![image](https://github.com/DMCERTCE/PoC_Tiny_Overflow/assets/168325622/7aea8e5c-d624-433d-bc2e-6425e7898865)
![image](https://github.com/DMCERTCE/PoC_Tiny_Overflow/assets/168325622/1d3aefc4-c0de-40a9-9895-05561c118e9c)
![image](https://github.com/DMCERTCE/PoC_Tiny_Overflow/assets/168325622/e0973b58-7678-49f0-82d8-5a9efb7404ed)
