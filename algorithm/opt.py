from b_order import *

def p_order(c_order, team) :

    p_with = np.random.choice([True, False])
    length = len(c_order)

    if p_with  :
        fst, sec = np.random.choice(length, 2, replace = True)
        c_order[fst], c_order[sec] = c_order[sec], c_order[fst]
    else :
        index = np.random.choice(range(length))
        num = c_order[index]
        inv = set(c_order) - {num}
        val = list(set(team) - inv)
        swap = np.random.choice(val)
        c_order[index] = swap

    return c_order

def algorithms(p_mat, r_mat, order, it, printer, team) :

    max_score = -1.0
    max_order = None

    for t in range(args.it) :
        n_order = p_order(order.copy(), team)
        c_score = calculate(order, p_mat, r_mat)
        n_score = calculate(n_order, p_mat, r_mat)

        if n_score > max_score :
            max_score = n_score
            max_order = n_order

        prob = min(1, pow(3000, 5 * (n_score - c_score)))
        accept = np.random.choice([True, False], p = [prob, 1 - prob])

        if accept :
            order = n_order

        if (t % printer == 0) :
            print(t, order, c_score)
            print("max: ", t, max_order, max_score)

    runs = calculate(order, p_mat, r_mat)

    return (max_score, max_order)
    return (runs, order)

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='best batting lineup.')
    parser.add_argument("it", type=int, help="number of iterations")
    parser.add_argument("samples", type=int, help="number of samples")
    parser.add_argument("printer", type=int, help="print every nth lineup")
    parser.add_argument("filename", nargs='?', default='landers.data', help="file with necessary statistics")
    args = parser.parse_args(['100', '1', '10'])

    print("Which team do you want to predict? ")
    args.filename = input()
    
    p_mat = stat_reader(args.filename)
    r_mat = create_run()

    order = [0,1,2,3,4,5,6,7,8]

    samp = []
    for i in range(args.samples):
        print("sample", i + 1, ":")
        result = algorithms(p_mat, r_mat, order, args.it, args.printer, range(len(p_mat)))
        samp.append(result)

    samp.sort(reverse=True)
    best = samp[0]

    print("Final ordering: {}".format(best[1]))
    print("This lineup will score an average of {} runs per game.".format(best[0]))
