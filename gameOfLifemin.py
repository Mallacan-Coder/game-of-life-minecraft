def main():
	from mcpi.minecraft import Minecraft
	from mcpi import block
	import time
	import psutil
	import random
	import numpy as np
	mc = Minecraft.create(address="localhost")
	gridSize = [16, 16]

	mc.postToChat("Choose the X dimension for the grid! (Wait 5 seconds for default size [16])")
	for i in range(100):
		p = mc.player.pollChatPosts()
		try:
			gridSize[0] = int(p[0].message)
		except:
			pass
		time.sleep(0.05)

	mc.postToChat("Choose the Y dimension for the grid! (Wait 5 seconds for default size [16])")
	for i in range(100):
		p = mc.player.pollChatPosts()
		try:
			gridSize[1] = int(p[0].message)
		except:
			pass
		time.sleep(0.05)

	mc.postToChat("Building variables...")

	posX = -556
	posY = 4
	posZ = 1003

	mc.postToChat("Defining functions...")

	def createBlankGrid(size):
		matr = []
		for i in range(size[0]):
			lin = []
			for j in range(size[1]):
				lin.append(15)
			matr.append(lin)

		for i in range(size[0]):
			for j in range(size[1]):
				mc.setBlock((posX + i + 1, posY, posZ + j), 251, 15)

		return matr

	def createBlankGridEdit(size):
		matr = []
		for i in range(size[0]):
			lin = []
			for j in range(size[1]):
				lin.append(15)
			matr.append(lin)

		for i in range(size[0]):
			for j in range(size[1]):
				mc.setBlock((posX + i + 1, posY, posZ - j - 3), 251, 15)

		return matr


	def getGridEdit(size):
		lis = []
		for i in range(size[0]):
			for j in range(size[1]):
				lis.append(mc.getBlock((posX + i + 1, posY, posZ - j - 3)))
		return lis

	def createRandomGrid(size):
		matr = []
		for i in range(size[0]):
			lin = []
			for j in range(size[1]):
				lin.append(random.choice([0, 15]))
			matr.append(lin)

		for i in range(size[0]):
			for j in range(size[1]):
				mc.setBlock((posX + i + 1, posY, posZ + j + 1), 251, matr[i][j])

		return matr

	def clean(size):
		for i in range(size[0]):
			for j in range(size[1]):
				mc.setBlock((posX + i + 1, posY, posZ + j), 0)
				mc.setBlock((posX + i + 1, posY, posZ - j - 3), 0)
	def gridToBinary(grid):
		matr = []
		for i in range(gridSize[0]):
			lin = []
			for j in range(gridSize[1]):
				if grid[i][j] == 15:
					lin.append(0)
				elif grid[i][j] == 0:
					lin.append(1)
			matr.append(lin)

		return matr

	def binaryToGrid(grid):
		matr = []
		for i in range(gridSize[0]):
			lin = []
			for j in range(gridSize[1]):
				if grid[i][j] == 0:
					lin.append(15)
				elif grid[i][j] == 1:
					lin.append(0)
			matr.append(lin)

		return matr

	def editToGrid(grid):
		grid = np.asarray(np.reshape(np.array(grid), gridSize))
		matr = []
		for i in range(gridSize[0]):
			lin = []
			for j in range(gridSize[1]):
				if grid[i][j] == 251:
					lin.append(15)
				elif grid[i][j] == 252:
					lin.append(0)
			matr.append(lin)

		return matr
	mc.postToChat(gridSize)
	def minecraft(grid):
		for i in range(gridSize[0]):
			for j in range(gridSize[1]):
				mc.setBlock((posX + i + 1, posY, posZ + j), 251, grid[i][j])
	 
	def calculateNextGen(grid):
		newState = []
		for i in range(gridSize[0]):
			lin = []
			for j in range(gridSize[1]):
				lin.append(0)
			newState.append(lin)

		for i in range(gridSize[0]):
			for j in range(gridSize[1]):
				nVecinos = grid[i % gridSize[0]][(j - 1)% gridSize[1]] +     grid[i % gridSize[0]][(j + 1)% gridSize[1]] + \
							   grid[(i + 1)% gridSize[0]][(j - 1)% gridSize[1]] + grid[(i + 1)% gridSize[0]][(j + 1)% gridSize[1]] + \
							   grid[(i + 1)% gridSize[0]][j % gridSize[1]] +     grid[(i - 1)% gridSize[0]][j % gridSize[1]] + \
							   grid[(i - 1)% gridSize[0]][(j + 1) % gridSize[1]] + grid[(i - 1)% gridSize[0]][(j - 1)% gridSize[1]]


				if nVecinos == 3 and grid[i][j] == 0:
					newState[i][j] = 1
				elif grid[i][j] == 1 and (nVecinos <= 1 or nVecinos >= 4):
					newState[i][j] = 0
				elif (nVecinos == 3 or nVecinos == 2) and grid[i][j] == 1:
					newState[i][j] = 1

		return newState

	def insertarGlider(grid):
		gridNew = grid
		gridNew[1][2] = 1
		gridNew[2][3] = 1
		gridNew[3][1:4] = [1, 1, 1]

		return gridNew
	gen = 0
	mc.postToChat("Starting Game...")
	mensaje = ""
	grid = createBlankGrid(gridSize)
	run = False
	while True:
		if mensaje == "glider":
			grid = createBlankGrid(gridSize)
			gridBin = gridToBinary(grid)
			gridBin = insertarGlider(gridBin)
			grid = binaryToGrid(gridBin)
			minecraft(grid)
		elif mensaje == "stop":
			clean(gridSize)
			break
		elif mensaje == "pause":
			run = False
		elif mensaje == "resume" or mensaje == "start":
			run = True

		elif mensaje == "gen":
			mensaje = ""
			mc.postToChat(str(gen) + "º generation")
		elif mensaje == "custom":
			mensaje = ""
			createBlankGridEdit(gridSize)

		elif mensaje == "update grid":
			mc.postToChat("Wait a minute, this can take a little bit :)")
			a = getGridEdit(gridSize)
			a = editToGrid(a)
			grid = a
			mc.postToChat("Type start to copy the draw!")
			mensaje = ""

		p = mc.player.pollChatPosts()
		try:
			mensaje = p[0].message
		except:
			pass


		if run:
			gridBin = gridToBinary(grid)
			newGrid = calculateNextGen(gridBin)
			grid = binaryToGrid(newGrid)
			minecraft(grid)
			time.sleep(0.1)
			gen += 1

try:
	main()
except:
	mc.postToChat("Some error ruined your experience, sorry... I guess lol")