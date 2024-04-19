#from array import *
import random
import numpy
import configparser

pokemon_index = open("pokemon_index.txt", "r")
#rating_abilities = open("rating_abilities.txt", "r") # This is for if we want to weigh abilities in a randomizer
pokemon_tiers = open("tiers.txt", "rt")
teams_list = open("teams_list.txt", "r")
iniEdit = configparser.ConfigParser()
iniEdit.read('config.ini')

mon_data = pokemon_index.readlines()
#comparison_data = rating_abilities.readlines()
tier_data = pokemon_tiers.readlines()
teams_data = teams_list.readlines()

pkArray = [
    #mon,ability,attack1,attack2,attack3,attack4
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', '']
           ]
teamArray = [-1, -1, -1, -1, -1]
movesetArray = [-1, -1, -1]
randomArray = [-1, -1, -1, -1, -1, -1]

isDone = False
selection = -1
textInput = ''
countLines = 0
countLines_tier = 0
countTiers = 0
tierSize = 0
currentIndex = 0
randomID = 0


for line in mon_data:
    countLines = countLines+1

for line in tier_data:
    countLines_tier = countLines_tier + 1
    if '\t' in line:
        countTiers = countTiers + 1

def importData():
    teams_output = open("__TEAMS__OUTPUT__.txt", "r")
    for j in range(6):
        pkArray[j][0] = teams_output.readline()
        textInput = teams_output.readline()
        pkArray[j][1] = textInput.replace('Ability: ', '')
        while '- ' not in textInput:
            textInput = teams_output.readline()
        pkArray[j][2] = textInput.replace(' - ', '')
        textInput = teams_output.readline()
        pkArray[j][3] = textInput.replace(' - ', '')
        textInput = teams_output.readline()
        pkArray[j][4] = textInput.replace(' - ', '')
        textInput = teams_output.readline()
        pkArray[j][5] = textInput.replace(' - ', '')
        teams_output.readline()
    teams_output.close()

def writeData(teams_output):
    #
    for a in range(6):

        # if use original movesets
        if iniEdit.get('Settings', 'original_moveset') == 'true':
            textInput = pkArray[a][0]
            textInput = textInput[:textInput.index('(')]
            # print(textInput)
            currentIndex = 0
            for n, line in enumerate(teams_data):
                currentIndex = n

                if textInput in line and '(' in line:
                    k = 2
                    for m in range(0, 10):
                        temp1 = teams_data[currentIndex + m]
                        if '- ' in temp1:
                            # temp1 = temp1.replace(' - ', '')
                            temp1 = temp1.replace('- ', '')
                            temp1 = temp1.replace('\n', '')
                            pkArray[a][k] = temp1
                            # pkArray[i][k] = pkArray[i][k].replace(' - ', '')
                            # print(pkArray[i][k])
                            k = k + 1
                            if k > 5:
                                break
                    break

        teams_output.write(pkArray[a][0] + '\n')
        teams_output.write('Ability: ' + pkArray[a][1] + '\n')
        #if original level

        #if original stats
        teams_output.write(' - ' + pkArray[a][2] + '\n')
        teams_output.write(' - ' + pkArray[a][3] + '\n')
        teams_output.write(' - ' + pkArray[a][4] + '\n')
        teams_output.write(' - ' + pkArray[a][5] + '\n\n')
    #

def randByTier(countTiers, selection):
    totalSections = 0
    tierString = ''
    #tiersSubtract supplies extra steps for the tiers to take by making them count more
    tiersSubtract = int(iniEdit.get('Settings', 'omit_first_x_tiers')) * -1
    countTiers = countTiers + tiersSubtract
    currentSection = tiersSubtract

    #get random ID for the tier we want, formula is (x^2)/100, tiers divided parallel to the y axis
    tierSize = 100 / countTiers
    randomID = random.randint(0, 100)
    #print(randomID, end=' ')
    #randomID = (randomID * randomID) / 100
    #print(randomID, end=' ')
    tierPlacing = 0
    for j in range(100):
        temp = 100 - (tierSize * j)
        temp = (temp*temp) / 100
        #print(temp)
        tierPlacing = j
        if randomID >= temp:
            break
    #print('a')
    #print(tierPlacing, end=' ')
    randomID = tierPlacing
    #if selection == 4:
    #   randomID = random.randint(1, countTiers)

    for j, line in enumerate(tier_data):
        currentIndex = j
        #grab them line by line
        textInput = tier_data[currentIndex]
        #textInput = textInput.replace('\n', '')
        #count up the sections
        if '\t' in textInput:
            if totalSections > currentSection:
                currentSection = currentSection + 1
            elif totalSections == currentSection:
                currentSection = currentSection + 1
                totalSections = totalSections + 1
            else:
                totalSections = totalSections + 1
        #print(j)
        if randomID == currentSection and '\t' not in textInput:
            tierString = tierString + textInput

    #print(tierString)
    tierString = tierString.replace('\n', ', ')
    tierList = tierString.split(', ')
    endResult = ''
    #print('c')
    while len(endResult) < 2:
        if len(tierList) < 2:
            break
        randomID = random.randint(1, len(tierList)-1)
        endResult = tierList[randomID]
    #print('c and a half')
    #print(endResult)
    for j, line in enumerate(mon_data):
        #endResult = endResult.lower()
        if endResult in line and '(' in line:
            endResult = line.replace('\n', '')
            break
    #print('d')
    return endResult

def changeDigit(token):
    if not token.isdigit():
        return -1
    else:
        token = int(token)
        return token


print('RL vs SLK Randomizer Tool')

while not isDone:

    #Startup
    print('\n0: Exit\n1: Teambuilder\n2: Dex\n3: Random Team (Weighted)\n4: True Random Team\n5: Random Single Pokemon')
    while selection < 0 or selection > 6:
        selection = input()
        selection = changeDigit(selection)
    print('\t'+selection.__str__())

    #teambuilder
    if selection == 1:
        teams_output = open("__TEAMS__OUTPUT__.txt", "r")
        importData()
        print('Team\n\tSlot 1: '+pkArray[0][0]+'\n\tSlot 2: '+pkArray[1][0]+'\n\tSlot 3: '+pkArray[2][0]+'\n\tSlot 4: '+pkArray[3][0]+'\n\tSlot 5: '+pkArray[4][0]+'\n\tSlot 6: '+pkArray[5][0])
        pkCopy = numpy.array(pkArray)
        pkCopy = str(pkCopy[:, 0])
        textInput = input('Edit which?\n').lower()
        textInput = str(textInput)

        if textInput.isdigit():
            currentMon = int(textInput)
            currentMon = currentMon - 1
            if not (-1 < currentMon < 6):
                currentMon = 0
        elif textInput in pkCopy.lower():
            textInput = str(textInput)
            for i in range(6):
                temp = pkArray[i][0]
                if str(textInput) in temp.lower():
                    currentMon = i
        else:
            selection = -1
            break

        selection = 0
        print('Do what with '+pkArray[currentMon][0]+'?')
        print('0: Exit\n1: PKMN Species\n2: Ability\n3: Moves')
        while selection < 0 or selection > 3:
            selection = input()
            selection = changeDigit(selection)
        selection = int(input())
        if pkArray[currentMon][0] != '' and currentMon > 0:
            currentMon = 1
            print('')

        while selection != 0:
            if selection == 1:
                pass
            elif selection == 2:
                pass
            elif selection == 3:
                selection = 0
                print('1: ' + pkArray[currentMon][2], end='')
                print('2: ' + pkArray[currentMon][3], end='')
                print('3: ' + pkArray[currentMon][4], end='')
                print('4: ' + pkArray[currentMon][5], end='')
                while selection < 1 or selection > 4:
                    selection = input()
                    selection = changeDigit(selection)

            selection = -1

    #dex
    elif selection == 2:
        textInput = input().lower()
        if textInput == '0':
            selection = -1
        for i, line in enumerate(mon_data):
            currentIndex = i

            if textInput in line.lower():
                if 'Ability:' in line:
                    print(mon_data[currentIndex-1], end='')
                elif '(' in line:
                    print(mon_data[currentIndex], end='')
                    print(mon_data[currentIndex+1], end='')
                    print(mon_data[currentIndex+2])
                else:
                    print(mon_data[currentIndex-2], end='')

    #random team weighted
    elif selection == 3:

        teams_output = open("__TEAMS__OUTPUT__.txt", "w")
        print('Team includes:')
        pkArray[0][0] = ''
        pkArray[1][0] = ''
        pkArray[2][0] = ''
        pkArray[3][0] = ''
        pkArray[4][0] = ''
        pkArray[5][0] = ''
        randomArray = [-1, -1, -1, -1, -1, -1]

        for i in range(6):
            pkArray[i][0] = randByTier(countTiers, selection)
            print(pkArray[i][0])

            for j, line in enumerate(mon_data):
                #
                if pkArray[i][0] in line and '(' in line:
                    currentIndex = j
                    break

            randomArray[i] = currentIndex
            # for abilities
            currentIndex = currentIndex + 1
            textInput = mon_data[currentIndex]
            textInput = textInput.replace('Ability: ', '')
            textInput = textInput.replace('\n', '')
            textInput = textInput.replace(', ', ',')
            newList = textInput.split(',')
            randomID = random.randint(1, len(newList))
            pkArray[i][1] = newList[randomID - 1].title()
            # print(pkArray[i][1])

            # for moves
            currentIndex = currentIndex + 1
            # print(currentIndex)
            movesetArray = [-1, -1, -1, -1]
            textInput = mon_data[currentIndex]
            textInput = textInput.replace('\n', '')
            textInput = textInput.replace(', ', ',')
            newList = textInput.split(',')

            randomID = random.randint(1, len(newList))
            movesetArray[0] = randomID
            pkArray[i][2] = newList[randomID - 1].title()

            while randomID in movesetArray:
                randomID = random.randint(1, len(newList))
            movesetArray[1] = randomID
            pkArray[i][3] = newList[randomID - 1].title()

            while randomID in movesetArray:
                randomID = random.randint(1, len(newList))
            movesetArray[2] = randomID
            pkArray[i][4] = newList[randomID - 1].title()

            while randomID in movesetArray:
                randomID = random.randint(1, len(newList))
            pkArray[i][5] = newList[randomID - 1].title()

        writeData(teams_output)
        teams_output.close()
        selection = -1

    #true random team
    elif selection == 4:
        teams_output = open("__TEAMS__OUTPUT__.txt", "w")
        print('Team includes:')
        pkArray[0][0] = ''
        pkArray[1][0] = ''
        pkArray[2][0] = ''
        pkArray[3][0] = ''
        pkArray[4][0] = ''
        pkArray[5][0] = ''
        randomArray = [-1, -1, -1, -1, -1, -1]

        for i in range(6):

            pkArray[i][0] = randByTier(countTiers, selection)
            print(pkArray[i][0])

            for j, line in enumerate(mon_data):
                #
                if pkArray[i][0] in line and '(' in line:
                    currentIndex = j
                    break

            randomArray[i] = currentIndex
            #for abilities
            currentIndex = currentIndex + 1
            textInput = mon_data[currentIndex]
            textInput = textInput.replace('Ability: ', '')
            textInput = textInput.replace('\n', '')
            textInput = textInput.replace(', ', ',')
            newList = textInput.split(',')
            randomID = random.randint(1, len(newList))
            pkArray[i][1] = newList[randomID-1].title()
            #print(pkArray[i][1])

            #for moves
            currentIndex = currentIndex + 1
            movesetArray = [-1, -1, -1, -1]
            textInput = mon_data[currentIndex]
            textInput = textInput.replace('\n', '')
            textInput = textInput.replace(', ', ',')
            newList = textInput.split(',')

            randomID = random.randint(1, len(newList))
            movesetArray[0] = randomID
            pkArray[i][2] = newList[randomID - 1].title()

            while randomID in movesetArray:
                randomID = random.randint(1, len(newList))
            movesetArray[1] = randomID
            pkArray[i][3] = newList[randomID - 1].title()

            while randomID in movesetArray:
                randomID = random.randint(1, len(newList))
            movesetArray[2] = randomID
            pkArray[i][4] = newList[randomID - 1].title()

            while randomID in movesetArray:
                randomID = random.randint(1, len(newList))
            pkArray[i][5] = newList[randomID - 1].title()

        #write to file then close
        writeData(teams_output)

        teams_output.close()
        selection = -1

    #random single mon
    elif selection == 5:
        selection = -1

    #exit
    elif selection == 0:
        pokemon_index.close()
        #rating_abilities.close()
        pokemon_tiers.close()
        isDone = True