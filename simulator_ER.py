from system import system


grid = system(structure = 'ER', dimensions = (1000,0.01))


# grid.define_rules({'R':1,'S':0,'T':1.9,'P':0 })
# grid.define_rules([[1, 0], [1.9, 0.01]])
# grid.plot_grid()
# grid.evolve(100)
# grid.plot_grid()

grid.degree_distribution(cumulative = True, scale = 'loglog')


# grid.plot_solution()
# grid.grid_test(points = 21, repetitions = 1)

# grid.evaluate()
