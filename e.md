now template engine is working fine. lets │ 
│     move on to ad some extra work level user │ 
│     variables. in the works details screen   │ 
│    there are schedule items, qty unit etc.   │ 
│    at last there is a column named           │ 
│    "variation". it gives a way to user to    │ 
│    vary the qty of each schedule on later    │ 
│    stages after work has been created. under │ 
│     this column user will put the updated    │ 
│    qty of each schedule (note that this will │ 
│     not update the original qty of the work  │ 
│    but add additional info that at later     │ 
│    stage the qty is varied to that number).  │ 
│    this variation in qty is a property of    │ 
│    individual work and must be saved in the  │ 
│    work model for later use. there may be    │ 
│    multiple variations in the same work viz  │ 
│    variation 1, variation 2 etc. later we    │ 
│    will use this data in variation,          │ 
│    comparision, vitiation reports for calculations. i need this variation column in a separate file in appropriate folder for modularity. so in ui there is no need to show the variation column by default. give user a way to add variation instead. 