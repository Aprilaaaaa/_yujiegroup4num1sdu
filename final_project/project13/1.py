from gmssl import sm3, func

A = 0
B = 7
G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
h = 1


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = extended_gcd(b, a % b)
    return d, y, x - (a // b) * y


def inverse_mod(a, n):
    d, x, y = extended_gcd(a, n)
    if d != 1:
        raise ValueError(f"{a} has no inverse modulo {n}")
    return x % n


def point_add(p, q):
    if p == 0:
        return q
    if q == 0:
        return p
    x1, y1 = p
    x2, y2 = q
    if x1 == x2 and y1 == y2:
        slope = (3 * x1 * x1 + A) * inverse_mod(2 * y1, P)
    else:
        slope = (y2 - y1) * inverse_mod(x2 - x1, P)
    x3 = (slope * slope - x1 - x2) % P
    y3 = (slope * (x1 - x3) - y1) % P
    return x3, round(y3)


def point_double(p):
    if p == 0:
        return 0
    x, y = p
    slope = (3 * x * x + A) * inverse_mod(2 * y, P)
    x3 = (slope * slope - 2 * x) % P
    y3 = (slope * (x - x3) - y) % P
    return x3, round(y3)


def point_inverse(p):
    x, y = p
    return x, (P - y) % P


def point_multiply(s, p):
    if s % N == 0 or p == 0:
        return 0
    n = p
    r = 0
    s_bin = bin(s)[2:]
    
    for i in reversed(range(len(s_bin))):
        if s_bin[i] == '1':
            r = point_add(r, n)
        n = point_double(n)

    return r


def hash_to_point(msg):
    x = int(sm3.sm3_hash(func.bytes_to_list(bytes(msg, encoding='utf-8'))), 16) % N
    return point_multiply(x, G)


def combine_set(msg_set):
    hash_set = point_add(0, 0)
    for msg in msg_set:
        hash_set = point_add(hash_set, hash_to_point(msg))
    return hash_set


def add_message(hash_set, msg):
    hash_value = hash_to_point(msg)
    hash_set = point_add(hash_set, hash_value)
    return hash_set


def remove_message(hash_set, msg):
    hash_value = hash_to_point(msg)
    hash_set = point_add(hash_set, point_inverse(hash_value))
    return hash_set


if __name__ == '__main__':
    a = "thirteen"
    b = "project"
    c = "ECMH"
    print("---------------------------------------------------------------------")
    print("               Calculating the hash values of a, b, and c             ")
    print("---------------------------------------------------------------------")
    hash_a = hash_to_point(a)
    print("hash(a):")
    print(hash_a)
    hash_b = hash_to_point(b)
    print("hash(b):")
    print(hash_b)
    hash_c = hash_to_point(c)
    print("hash(c):")
    print(hash_c)
    print("---------------------------------------------------------------------")
    print("     Testing whether hash({a, b}) == hash({b, a})                     ")
    print("---------------------------------------------------------------------")
    set_ab = [a, b]
    hash_ab = combine_set(set_ab)
    print("hash({a, b}):")
    print(hash_ab)
    set_ba = [b, a]
    hash_ba = combine_set(set_ba)
    print("hash({b, a}):")
    print(hash_ba)
    print("---------------------------------------------------------------------")
    print("hash({a, b}) == hash({b, a})?", hash_ab == hash_ba)
    print("---------------------------------------------------------------------")
    print("      Testing whether hash(a) + hash(b) == hash({a, b})              ")
    print("---------------------------------------------------------------------")
    hash_add_ab = add_message(hash_to_point(a), b)
    print("hash(a) + hash(b):")
    print(hash_add_ab)
    print("hash({a, b}):")
    print(hash_ab)
    print("---------------------------------------------------------------------")
    print("hash(a) + hash(b) == hash({a, b})?", hash_add_ab == hash_ab)
    print("---------------------------------------------------------------------")
    print("      Testing whether hash({a, b, c}) - hash(c) == hash({a, b})      ")
    print("---------------------------------------------------------------------")
    set_abc = [a, b, c]
    hash_abc = combine_set(set_abc)
    print("hash({a, b, c}):")
    print(hash_abc)
    hash_abc_remove_c = remove_message(hash_abc, c)
    print("hash({a, b, c}) - hash(c):")
    print(hash_abc_remove_c)
    print("hash({a, b}):")
    print(hash_ab)
    print("---------------------------------------------------------------------")
    print("hash({a, b, c}) - hash(c) == hash({a, b})?", hash_abc_remove_c == hash_ab)
    print("---------------------------------------------------------------------")
