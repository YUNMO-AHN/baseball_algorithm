import numpy as np
from math import pow
import argparse

def create_player(hom, tri, dou, hit, bb, ab):
    pa = hom + tri + dou + hit + bb + ab
    h = hom / pa
    t = tri / pa
    d = dou / pa
    s = hit / pa
    b = bb / pa
    a = ab / pa

    on_base = np.zeros((8, 8), dtype = float)
    on_base[0] = [h, b+s, d, t, 0, 0, 0, 0]
    on_base[1] = [h, 0, d/2, t, b+s/2, s/2, d/2, 0]
    on_base[2] = [h, s/2, d, t, b, s/2, d/2, 0]
    on_base[3] = [h, s/2, d, t, b, s/2, 0, 0]
    on_base[4] = [h, 0, d/2, t, s/6, s/3, d/2, b+s/2]
    on_base[5] = [h, 0, d/2, t, s/2, s/2, d/2, b]
    on_base[6] = [h, s/2, d, t, 0, s/2, 0, b]
    on_base[7] = [h, 0, d/2, t, s/2, s/2, d/2, b]

    trans_on_base = np.zeros((9*24 + 1, 9*24 + 1), dtype = float)
    for i in range(27) :
        start = i * 8
        end = i * 8 + 8
        trans_on_base[start:end, start:end] = on_base

    for i in range(9) :
        for j in range(2) :
            start = (i * 24) + (j * 8)
            trans_on_base[start:(start + 8), (start + 8):(start + 16)] = a * np.eye(8, dtype = float)

        trans_on_base[(i * 24) + 16: (i * 24) + 24, (i + 1) * 24] = [a] * 8

    trans_on_base[9 * 24, 9 * 24] = 1

    return trans_on_base

def stat_reader(filename) :

    player = []
    with open(filename, 'r') as f :
        lines = f.readlines()
        for i, line in enumerate(lines) :
            stats = line.split(',')
            hom = int(stats[0])
            tri = int(stats[1])
            dou = int(stats[2])
            hit = int(stats[3])
            bb = int(stats[4])
            ab = int(stats[5])
            name = stats[6]
            player_stat = create_player(hom, tri, dou, hit, bb, ab)
            player.append(player_stat)

    return player

def create_run() :
    r_matrix = [[1, 0, 0, 0, 0, 0, 0, 0],
                [2, 1, 1, 1, 0, 0, 0, 0],
                [2, 1, 1, 1, 0, 0, 0, 0],
                [2, 1, 1, 1, 0, 0, 0, 0],
                [3, 2, 2, 2, 1, 1, 1, 0],
                [3, 2, 2, 2, 1, 1, 1, 0],
                [3, 2, 2, 2, 1, 1, 1, 0],
                [4, 3, 3, 3, 2, 2, 2, 1]]

    run_matrix = np.zeros((9 * 24 + 1, 9 * 24 + 1), dtype = 'float32')

    for i in range(9 * 3) :
        run_matrix[i * 8 : i * 8 + 8, i * 8 : i * 8 + 8] = r_matrix

    return run_matrix

def calculate(order, player, run) :

    situation = np.zeros((1, 9 * 24 + 1), dtype = "float32")
    situation[:, 0] = 1

    runs = 0
    batter = 0

    while situation[:, 9 * 24] < 0.99 :
        index = order[batter]
        player_m = player[index]

        temp = np.dot(situation, (run * player))
        runs += np.sum(temp)

        situation = np.dot(situation, player_m)

        batter += 1
        if batter > 8 :
            batter = 0

    return runs

def inputorder(stat_input) :
    order = [0] * 9
    if len(stat_input) < 2 :
        print("Using default order")
        return order
    elif len(stat_input) != 9 :
        print("Lineup should be nine numbers. Using default lineup instead")
        return order
    else :
        for i, char in enumerate(stat_input) :
            try :
                order[i] = int(char)
            except :
                print("Input should be all numbers. Using default lineup instead")
                return order

    return order

def expect_runs(player_stats, order = [0, 1, 2, 3, 4, 5, 6, 7, 8]) :
    assert(len(order) == 9)
    mat = create_run()
    p_mats = []
    for stats in player_stats :
        p_mat = create_player(*stats[:6])
        p_mats.append(p_mat)

    runs = calculate(order, p_mats, mat)

    return runs

if __name__ == '__main__' :

    parser = argparse.ArgumentParser(description = 'lineup, expected runs.')
    parser.add_argument("filename", nargs = '?', default = 'landers.data', help = "necessary stats")
    parser.add_argument("lineup", nargs = '?', default = '012345678', help = "batting order")
    args = parser.parse_args()

    order = inputorder(args.lineup)
    p_mats = stat_reader(args.filename)
    r_mat = create_run()

    runs = calculate(order, p_mats, r_mat)

    print("This lineup will score an average of {} runs per game.".format(runs))
