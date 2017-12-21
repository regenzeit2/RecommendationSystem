import csv
import math
import copy

import json
import requests

dataFileName = "data.csv"
contextFileName = "context.csv"

num = 3

contentType = 'application/json'
url = 'https://cit-home1.herokuapp.com/api/rs_homework_1'


def readData(file_name):
    list = []
    f = open(file_name)
    for row in csv.reader(f):
        list.append(row)
    f.close()
    return list


def getMetrica(list):
    users = []
    for j in range(0, len(list)):
        if j == num:
            users.append(0)
            continue
        uI = 0
        vI = 0
        uIvI = 0

        for i in range(1, len(list[num])):
            if int(list[num][i]) > 0 and int(list[j][i]) > 0:
                uIvI += int(list[num][i]) * int(list[j][i])
                uI += int(list[num][i]) * int(list[num][i])
                vI += int(list[j][i]) * int(list[j][i])
                vI = math.sqrt(vI)
        res = uIvI / (uI * vI)
        users.append(res)
    return users


def getAvgMark(list):
    sum = 0
    cnt = 0
    for i in range(1, 31):
        if int(list[i]) != -1:
            sum += int(list[i])
            cnt += 1
    return sum / cnt


def getProduct(allUsers, currentUser, dict, sims):
    result = []
    for i in range(1, 31):
        if int(currentUser[i]) == -1:
            numerator = 0
            denominator = 0
            for x in dict:
                if int(allUsers[x][i]) != -1:
                    numerator += sims[x] * (int(allUsers[x][i]) - getAvgMark(allUsers[x]))
                    denominator += abs(sims[x])
            ri = getAvgMark(users[num]) + (numerator / denominator)
            result.append(ri)
    return result


def getRecommendedMovies(allUsers, currentUser, dict):
    movie = {}
    for i in range(1, 31):
        if int(currentUser[i]) == -1:
            avg = 0
            for x in dict:
                avg += int(allUsers[x][i])
            avg /= len(dict)
            movie[i] = avg
    return movie


def sendRequest(num, answer, movie):
    # 2 4 5 11 12 13 14 15 21
    mov1 = 'movie 2'
    mov2 = 'movie 4'
    mov3 = 'movie 5'
    mov4 = 'movie 11'
    mov5 = 'movie 12'
    mov6 = 'movie 13'
    mov7 = 'movie 14'
    mov8 = 'movie 15'
    mov9 = 'movie 21'

    result = json.dumps({'user': num, '1': {
        mov1: round(answer[0], 2),
        mov2: round(answer[1], 2),
        mov3: round(answer[2], 2),
        mov4: round(answer[3], 2),
        mov5: round(answer[4], 2),
        mov6: round(answer[5], 2),
        mov7: round(answer[6], 2),
        mov8: round(answer[7], 2),
        mov9: round(answer[8], 2)},
                         '2': {"movie " + str(movie): round(answer[1], 2)}})

    print(result)

    #post = requests.post(url, data=result, headers={'content-type': contentType})
    #print(post.json())


def getMovie(movies, num):
    movie = 0
    for value in values:
        flag = 0
        for key in movies:
            if movies[key] == value and days[num][int(value)] != "-" and days[num][int(value)] != "Sun" and days[num][
                int(value)] != "Sat":
                movie = key
                flag = 1
                break
        if flag == 1:
            break
    return movie


if __name__ == '__main__':
    users = readData(dataFileName)
    days = readData(contextFileName)
    users = users[1:41]
    days = days[1:41]
    averageMark = getAvgMark(users[num])
    sim = getMetrica(users)
    old = copy.deepcopy(sim)
    sim.sort(reverse=True)

    dictionary = {}
    for i in sim[:5]:
        dictionary[old.index(i)] = i
    result = getProduct(users, users[num], dictionary, sim)
    recommendedMovies = getRecommendedMovies(users, users[num], dictionary)
    values = sorted(list(set(recommendedMovies.values())), reverse=True)

    sendRequest(num, result, getMovie(recommendedMovies, num))
