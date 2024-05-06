# PoC_Tiny_Overflow
Proof-of-concept for overflow and resulting memory leak in TinyWeb 1.94

Failure to properly validate the HTTP Request Method and other request fields allows a attacker to target the server by sending a large payload.
The underlying session thread will terminate with runtime error 203 (Heap Overflow) and subsequently a memory leak in the main application.

By doing this several times it is possible to consume all 2GB of the 32-bit application leading to a DoS.  

PoC Script contains code to demonstrate the attack. Notice that timeout may differ according to available bandwidth.
Script takes ip - port as argument.
