import random
from itertools import permutations

def judge(real, expect):
    """判定用の関数
    引数
    :param list real: 真実の数
    :param list expect: 予測された数

    戻しち
    :rtype: tuple: (eat, bite)
    """
    assert len(real) == len(expect)
    eat, bite = 0, 0
    for si, expdig in enumerate(expect):
        for ri, reldig in enumerate(real):
            if ri == si and reldig == expdig:
                eat += 1
            elif ri != si and reldig == expdig:
                bite += 1
    return (eat, bite)

def search_candidates(known_results, digit):
    """
    既知の結果から、相手の数字のあり得る候補を列挙する

    :param known_results: 既知の結果のリスト。1回毎の結果はDictionaryになっている。
        * known_res[i]["expect"]: i+1回目の回答の回答数字
        known_res[i]["eat"]: その数字でのeat
        known_res[i]["bite"]: その数字でのbite
    :param int digit: 桁数
    :return list: 相手の数字のあり得る候補
    """
    probables = []
    for candidate in permutations(range(10), r=digit):
        # 今までの結果と照らしておかしくないか、検討する
        candidate = list(candidate)
        probability = True
        for known_result in known_results:
            if judge(candidate, known_result["expect"]) == (known_result["eat"], known_result["bite"]):
                probability = probability and True
                continue
            else:
                probability = False
                break
        if probability == True:
            probables.append(candidate)
    return probables


if __name__ == "__main__":
    random.seed()

    digit = int(input("何桁で勝負しますか？: "))
    own = input("あなたの番号を入力してください: ")
    assert len(own) == digit
    own = [int(own[i]) for i in range(digit)]
    opponent = random.sample([0,1,2,3,4,5,6,7,8,9], k=digit)
    numtrial = 0
    cpu_knownres = []

    while True:
        numtrial += 1
        # 回答の入力
        while True:
            expect = input("予想する数字を入力してください: ")
            if len(expect) == digit:
                expectlist = [int(expect[i]) for i in range(digit)]  # リスト化
                break
            else:
                print(f"入力する数字は{digit:d}桁でなければなりません。")
                continue

        # 判定
        eat, bite = judge(opponent, expectlist)

        # 3 EATを出せた場合、ゲームを終わらせる
        if eat == digit:
            print(f"{numtrial}回で正解しました。")
            break

        # CPU側の攻撃
        print("cpu considering...", end=" ")
        candidates = search_candidates(cpu_knownres, digit)
        print(f"{len(candidates)} candidates found!")
        cpu_expect = random.choice(candidates)
        cpueat, cpubite = judge(own, cpu_expect)
        cpu_knownres.append({"expect": cpu_expect, "eat": cpueat, "bite": cpubite})
        if cpueat == digit:
            print(f"{numtrial}回で負けました。CPUの数字: {opponent}")
            break

        # 結果の表示
        print(f"Your call {expect}: {eat:2d} EAT, {bite:2d} BITE"
              + f" / CPU call {cpu_expect}: {cpueat} EAT, {cpubite} BITE")
