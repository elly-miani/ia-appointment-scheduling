# IA-APPOINTMENT-SCHEDULING
A simple webapp to schedule meetings with time and location constraints using constraint programming techniques.

## How to Run
You need to run a local Python web server to use the web application.

From the root folder: `python webserver.py`

The web server will run on `http://localhost:8000/`


## Case study
An estate agent needs a tool to automatically schedule next week appointments based on his and his clients' constraints.

Each appointment will be characterized by:
- The **client** who requested it
- The **day** in which it will take place
- The **time slot** in which it will take place
- The **property** that will be shown to the client.

These constraints are:
- *His own schedule*: monday-friday working hours from 8am-6pm with a lunch break between 12am-2pm
- *The client availability*: specified for each appointment requested in terms of available days and time intervals.
- *The time needed to get to the property* area from the previous appointment

To simplify the problem we assume:
- Time is divided into discrete slots of 30 min.
- Each appointment requires 2 time slots.
- There are 4 available properties: A, B, C, D.
- Appointments that take place in the same property require no interval between them.
- The time needed to move from one property to the next is:
  - (A -> B) = 1 time slot
  - (A -> C) = 1 time slot
  - (A -> D) = 2 time slots
  - (B -> C) = 2 time slots
  - (B -> D) = 1 time slot
  - (C -> D) = 1 time slot
