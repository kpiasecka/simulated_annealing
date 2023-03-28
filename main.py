from src import MakeSpan, ProblemInstance, SA, GeometricCooling, IterativeCondition

instance = ProblemInstance.generate(10, 20)
criteria = MakeSpan()
cooling = GeometricCooling(.95)
condition = IterativeCondition(1000)
sa = SA(
    temp=1000,
    cooling=cooling,
    stop_condition=condition,
    criteria=criteria,
    problem_instance=instance
)
sa.solve()
sa.plot()
