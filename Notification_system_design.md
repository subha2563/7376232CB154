# Stage 1

## Approach and System Design

### Priority Logic
To establish the Priority Inbox, every incoming notification is evaluated based on two primary dimensions to determine its rank:
1. **Categorical Weight:** A hardcoded priority dictionary ensures `Placement` (Weight: 3) > `Result` (Weight: 2) > `Event` (Weight: 1).
2. **Recency:** The ISO-formatted string is parsed into a Unix timestamp/Datetime object to act as the secondary sorting factor (tie-breaker). Newer timestamps hold a higher value.

### Efficient Top 'N' Maintenance (The Min-Heap Strategy)
The primary constraint of this system is maintaining performance as the volume of continuous notifications scales indefinitely. 

**Why not standard sorting?**
Gathering all notifications and sorting them `O(N log N)` every time a user loads the inbox or a new notification arrives is highly inefficient and memory-intensive.

**The Solution:**
I implemented a **Min-Heap (Priority Queue)** constrained to a maximum size of `N` (where N=10). 
1. As new notifications stream in, they are packaged into a tuple: `(Weight, Timestamp, ID)`.
2. While the heap size is under 10, we simply push incoming items into it.
3. Once the heap reaches 10 items, the "lowest priority" item among the top 10 automatically sits at the root of the Min-Heap.
4. For every subsequent incoming notification, we use a `Push-Pop` operation: we insert the new notification and instantly drop the root if the new notification is of higher value. 

### Performance Profile
* **Time Complexity:** `O(K + N log K)` where `N` is the total number of notifications and `K` is our priority threshold (10). Because `K` is a tiny constant, the insertion time for any new notification is effectively `O(1)`.
* **Space Complexity:** `O(K)`. The application only ever holds 10 items in active sorting memory, making it exceptionally lightweight and highly scalable regardless of how large the database or incoming stream grows.
