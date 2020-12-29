from hashlib import sha1


ALPHABET_SIZE = 26


def build_message(param1, param2, param3, param4, param5):

    message = param1 + param2 + param3 + param4 + param5

    return message.encode("utf-8")  # + (" " * (586 - len(message.encode("utf-8")))).encode("utf-8")

#
# def send_type(param2):
#
#     param1 = ('~' * 32)
#     param3 = ('~' * 40)
#     param4 = '1'
#     param5 = ('~' * 2)
#
#     return build_message(param1, str(param2), param3, param4, param5)


# CLIENT


def divide_to_domains(original_len, num_of_servers):
    """
    divide tasks to n servers fairly
    :raise TypeError if len or servers are not integers
    :param original_len: length of strings in search ranges
    :param num_of_servers: amount of servers requiring for task
    :return: return list of tasks: [(start1,end1), (start2,end2),...,(startn,endn)]
       where n is the amount of servers available to work
    """
    if int(original_len) != original_len:
        raise TypeError("length of string must be integer")
    if int(num_of_servers) != num_of_servers:
        raise TypeError("amount of server must be integer")

    domains = [None] * num_of_servers
    domains_str = [None] * num_of_servers
    last = 'z' * original_len

    count_permutations = __get_count_permutations(original_len)
    per_server = count_permutations // num_of_servers
    str_as_int = 0

    for i in range(len(domains)):
        start = __get_string_value(str_as_int, original_len)

        if str_as_int >= count_permutations:
            start = last
        str_as_int += per_server
        end = __get_string_value(str_as_int, original_len)

        if str_as_int >= count_permutations:
            end = last
        domains[i] = (start, end)
        domains_str[i] = start + end
        str_as_int += 1
    domains[len(domains) - 1] = (domains[len(domains) - 1][0], last)

    return domains_str


def __get_count_permutations(strLen):
    """
    :param strLen: length of required strings
    :return: amount of different strings could be generated in given length
    """
    return ALPHABET_SIZE ** strLen


def __get_string_value(to_convert, length):
    """
    translate int to string with given len
     when 0 is 'aaa...a'
    :param to_convert: integer value of string
    :param length: required string length
    :return: string value of given number with given length
    """
    str_val = ""
    while to_convert > 0:
        c = int(to_convert % 26)
        str_val = chr(c + 97) + str_val
        to_convert = int(to_convert // 26)
        length = length - 1
    while length > 0:
        str_val = 'a' + str_val
        length -= 1
    return str_val


# SERVER


def solve(hashed_word, start_range, end_range):
    """
    Solve get a given hash string hashed using a sha1 hash, and search
    at the given range the original word

    :param hashed_word: String. word after hash using sha1.
    :param start_range: String. represent the first word to start the hash search at.
    :param end_range: String. represent the last word to end the hash search at.

    :return: String represent the hashed word or None if didn't found is in the given range.
    """
    # hash_digest = hashed_word
    range_words = strange(start_range.lower(), end_range.lower())

    for tryWord in iter(range_words):
        if sha1(tryWord.encode()).hexdigest() == hashed_word:
            return tryWord

    return None


def split_message(message):
    magic_cookie = message[0].hex()
    message_type = message[1].hex()
    dest_port = int.from_bytes(message[2], byteorder='big')
    return magic_cookie, message_type, dest_port


def check_legal_offer(magic_cookie, message_type, dest_port):
    flag1 = True
    flag2 = True
    flag3 = True
    if not magic_cookie == 'feedbeef':
        flag1 = False
    if not message_type == '02':
        flag2 = False
    if not dest_port._eq_('13117'):
        flag3 = False
    return flag1 and flag2 and flag3






def strange(start, end_or_len, sequence="abcdefghijklmnopqrstuvwxyz"):
    """
    Strage function get two range of string and return object containing all the words between this range.

    site: https://stackoverflow.com/questions/14927114/is-it-possible-to-make-a-letter-range-in-python

    :param sequence:
    :param start: String. represent the first word to start from the list.
    :param end_or_len: represent the end string or the length of the list.

    :return: Object. data containing all the word between the given range.
    """
    seq_len = len(sequence)
    start_int_list = [sequence.find(c) for c in start]
    if isinstance(end_or_len, int):
        inclusive = True
        end_int_list = list(start_int_list)
        i = len(end_int_list) - 1
        end_int_list[i] += end_or_len - 1
        while end_int_list[i] >= seq_len:
            j = end_int_list[i] // seq_len
            end_int_list[i] = end_int_list[i] % seq_len
            if i == 0:
                end_int_list.insert(0, j-1)
            else:
                i -= 1
                end_int_list[i] += j
    else:
        end_int_list = [sequence.find(c) for c in end_or_len]

    while len(start_int_list) < len(end_int_list) or (len(start_int_list) == len(end_int_list) and start_int_list <= end_int_list):
        yield ''.join([sequence[i] for i in start_int_list])
        i = len(start_int_list)-1
        start_int_list[i] += 1
        while start_int_list[i] >= seq_len:
            start_int_list[i] = 0
            if i == 0:
                start_int_list.insert(0,0)
            else:
               i -= 1
               start_int_list[i] += 1
