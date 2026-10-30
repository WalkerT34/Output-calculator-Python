Objective and Result
Create a calculator in Python to determine a plant's average hourly throughput and compare the required throughput against the equipment's rated (nameplate) capacity.
Input Data
60 million tonnes/year; 330 days; 24 hours/day; rated capacity: 8,000 tonnes/hour. Reserve = (rated capacity / required throughput − 1) × 100%. Calculations are prohibited if input values ​​are zero or negative.
Algorithm
Obtain four input values ​​→ convert strings to numbers → validate ranges → call the calculation function → compute the reserve → output "sufficient" if the reserve is ≥ 0, or "insufficient" if the reserve is < 0.
