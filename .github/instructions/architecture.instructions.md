# Architecture Instructions

The system follows an event-driven cognitive architecture.

All components communicate through the Event Bus.

Example flow:

input_event
   ↓
perception
   ↓
memory
   ↓
reasoning
   ↓
planning
   ↓
action

Modules must subscribe to events and publish results.

No direct calls between modules.