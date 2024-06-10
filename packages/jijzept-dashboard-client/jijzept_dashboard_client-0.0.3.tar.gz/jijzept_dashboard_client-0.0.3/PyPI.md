# JijZeptDashboard-Client

The JijZeptDashboard-Client has two features. The first feature is to add 
descriptions to your mathematical model using JijModeling. The second feature 
is to register your mathematical model on the JijZeptDashboard.

## How to use

You can register your mathematical model on the JijZeptDashboard as follows:

```python
import jijmodeling as jm
import jijzept_dashboard_client as jdc

# Define your mathematical model with JijModeling
d = jm.Placeholder("d", ndim=2, description="Distance matrix")
N = d.len_at(0, latex="N", description="Number of cities")
i = jm.Element("i", belong_to=(0, N), description="City index")
j = jm.Element("j", belong_to=(0, N), description="City index")
t = jm.Element("t", belong_to=(0, N), description="City index")
x = jm.BinaryVar("x", shape=(N, N), description="Assignment matrix")

problem = jm.Problem("TSP")
problem += jm.sum([i, j], d[i, j] * jm.sum(t, x[i, t] * x[j, (t + 1) % N]))
problem += jm.Constraint("one-city", jm.sum(i, x[i, t]) == 1, forall=t)
problem += jm.Constraint("one-time", jm.sum(t, x[i, t]) == 1, forall=i)

# Add descriptions to your mathematical model
jdc_problem = jdc.Problem.from_jm_problem(
    problem,
    objective_description="Minimize total distance",
    constraint_descriptions={
        "one-city": "Each city is visited exactly once",
        "one-time": "Each person visits exactly one city",
    }
)

# Register your mathematical model on the JijZeptDashboard
client = jdc.JijZeptDashboardClient(
    url="*** url for registration ***",
    email="*** your email address ***",
    password="*** your password ***",
)
response = client.register_model(jdc_problem, project_id=1)
```

You can add descriptions to the objective function and constraints by 
using `jdc.Problem.from_jm_problem`. On the other hand, to add descriptions 
to decision variables, placeholders and elements, you need to use JijModeling.

## Define a problem in an alternative way

You can define a mathematical model with descriptions using the constractor 
of `jdc.Problem` as follows:

```python
import jijmodeling as jm
import jijzept_dashboard_client as jdc

# Define your mathematical model with JijModeling
d = jm.Placeholder("d", ndim=2, description="Distance matrix")
N = d.len_at(0, latex="N", description="Number of cities")
i = jm.Element("i", belong_to=(0, N), description="City index")
j = jm.Element("j", belong_to=(0, N), description="City index")
t = jm.Element("t", belong_to=(0, N), description="City index")
x = jm.BinaryVar("x", shape=(N, N), description="Assignment matrix")

problem = jdc.Problem("TSP")
problem += (
    jm.sum([i, j], d[i, j] * jm.sum(t, x[i, t] * x[j, (t + 1) % N])),
    "Minimize total distance",
)
problem += (
    jm.Constraint("one-city", jm.sum(i, x[i, t]) == 1, forall=t),
    "Each city is visited exactly once",
)
problem += (
    jm.Constraint("one-time", jm.sum(t, x[i, t]) == 1, forall=i),
    "Each person visits exactly one city",
)
```
