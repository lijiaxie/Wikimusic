from models import *
from params import *

def alpha():
    order = 10
    alphas = []
    for affine in range(0, 8):
        for i in range(1, order+1):
            # linear positive
            if affine == 1:
                alphas.append(i)
            # poly pos
            elif affine == 2:
                alphas.append(i ** 2)
            # expo pos
            elif affine == 3:
                alphas.append(2 ** i)
            # unif neg
            elif affine == 4:
                if i == order:
                    alphas.append(order)
                else:
                    alphas.append(-1)
            # lin neg
            elif affine == 5:
                if i == order:
                    alphas.append(sum(range(1, order+1)))
                else:
                    alphas.append(-i)
            # poly neg
            elif affine == 6:
                if i == order:
                    alphas.append(sum([(i ** 2) for i in range(1,order+1)]))
                else:
                    alphas.append(-(i ** 2))
            # expo neg
            elif affine == 7:
                if i == order:
                    alphas.append(sum([(2 ** i) for i in range(1,order+1)]))
                else:
                    alphas.append(-(2 ** i))
            # unif pos
            else:
                alphas.append(1)
        print(alphas)
        alphas = []


def counter_test():
    order = 5
    alphas = [-1,-2,-3,-4,15]
    hist = [[1,2,3,4],[2,3,4,5],[3,4,5,6],[4,5,6,7],[5,6,7,8]]

    with ExecTimer() as t:
        counters = [ct(x) for x in hist]
        for i, ctr in enumerate(counters):
            for key in ctr.keys():
                ctr[key] *= alphas[i]
        # ensure that the first counter in list has positive values
        counters.reverse()
        ct_sum1 = sum(counters, ct())

    print("For loop with key update: %.05f" % t.interval)

    with ExecTimer() as t:
        counters = [ct(x * abs(alphas[i])) for i, x in enumerate(hist)]
        counters.reverse()
        ct_sum2 = ct()
        for i in range(len(counters)):
            if alphas[len(counters) - i - 1] > 0:
                ct_sum2 += counters[i]
            else:
                ct_sum2 -= counters[i]


    print("For loop for sum with abs: %.05f" % t.interval)


def path_test():
    g = Graph(BINARY, DB)
    order = 10
    for affine in [0,1,2,3,4,5,6,7]:
        times = []
        for _ in range(100):
            with ExecTimer() as t:
               g.get_path(5,order,affine)
            times.append(t.interval)
        print("Affine: %d - Time: %.05f" % (affine, sum(times) / len(times)))


if __name__ == "__main__":
    path_test()