from system import system


grid = system(structure = 'grid', dimensions = (32,32))


# grid.define_rules({'R':1,'S':0,'T':1.9,'P':0 })
# grid.define_rules([[1, 0], [1.9, 0.01]])
# grid.plot_grid()
# grid.evolve(1)
# grid.plot_grid()

# grid.grid_test(points = 21, repetitions = 1)
grid.plot_solution(folder = 'Aq_grid/')

# grid.evaluate()
