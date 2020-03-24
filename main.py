import mido
import numpy as np
from matplotlib import pyplot as plt
import random
from mido import MidiFile, MidiTrack, Message


def createMIDI(specimen, index):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=12, time=0))

    for i in range(len(specimen)):
        track.append(Message('note_on', note=specimen[i], velocity=64, time=128))
        track.append(Message('note_off', note=specimen[i], velocity=127, time=64))

    mid.save('new_song_' + str(index) + '.mid')


def generateSpecimen(length):
    list = []
    for i in range(length):
        # notes are from 36 - C2 to 95 - B6
        list.append(random.randint(48, 71))
    return np.array(list)


def isInMajor(note, key):
    if abs(note - key) == 0 or abs(note - key) == 2 or abs(note - key) == 4 or abs(note - key) == 5 or abs(
            note - key) == 7 or abs(note - key) == 9 or abs(note - key) == 11 or abs(note - key) == 12:
        return True
    else:
        return False


def rateSpecimen(specimen):
    # min ze wszystkich wystąpień każdej nuty + maximum z długości wszystkich powtarzających się sekwencji o długości co najmniej 5 * liczba wystąpień tej sekwencji * jej długość
    dict = {}
    key = specimen[0]
    notes_in_key = 0
    for i in range(len(specimen)):
        if isInMajor(specimen[i], key):
            notes_in_key += 1
        if dict.keys().__contains__(str(specimen[i])):
            dict[str(specimen[i])] += 1
        else:
            dict[str(specimen[i])] = 1

    return notes_in_key


def mutateSpecimen(specimen, mutation_chance):
    for i in range(len(specimen)):
        if random.random() <= mutation_chance:
            specimen[i] = random.randint(48, 71)

    return specimen


def breedSpecimen(specimen_1, specimen_2, breed_chance):
    new_specimen = []
    for i in range(len(specimen_1)):
        if random.random() <= breed_chance:
            new_specimen.append(specimen_1[i])
        else:
            new_specimen.append(specimen_2[i])
    return np.array(new_specimen)


def tournamentSelection(specimen_list):
    new_list = []
    while len(new_list) != len(specimen_list):
        num_of_contestants = random.randint(2, 10)
        contestants = []
        for i in range(num_of_contestants):
            contestants.append(specimen_list[random.randint(0, len(specimen_list) - 1)])
        best = max(contestants, key=lambda specimen: (specimen[1]))
        new_list.append(best)

    return np.array(new_list)


def doGenerations(number_of_gens, specimen_number, specimen_size, mutation_chance, breed_chance):
    specimen_list = []
    for i in range(specimen_number):
        specimen = generateSpecimen(specimen_size)
        specimen_list.append((specimen, rateSpecimen(specimen)))
    for i in range(number_of_gens):
        tournamentSelection(specimen_list)
        for j in range(specimen_number):
            specimen_list[j] = (mutateSpecimen(specimen_list[j][0], mutation_chance), 0)
            second_parent = specimen_list[random.randint(0, len(specimen_list) - 1)]
            specimen_list[j] = (breedSpecimen(specimen_list[j][0], second_parent[0], breed_chance), 0)
            specimen_list[j] = (specimen_list[j][0], rateSpecimen(specimen_list[j][0]))
        print("Gen " + str(i) + " finished. Best score: " + str(max(specimen_list, key=lambda spec: (spec[1]))[1]))

    for i in range(specimen_number):
        createMIDI(specimen_list[i][0], specimen_list[i][1])


doGenerations(1000, 50, 50, 0.01, 0.1)
