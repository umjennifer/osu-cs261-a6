# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        for i in range(self.buckets.length()):
            self.buckets[i] = None
        self.size = 0

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        """
        # quadratic probing required
        h = self.hash_function(key)
        i = h % self.buckets.length()
        j = 0
        i_initial = i
        while self.buckets[i] is not None:
            if self.buckets[i].is_tombstone is False:
                if self.buckets[i].key == key:
                    return self.buckets[i].value
            j += 1
            i = (i_initial + (j * j)) % self.capacity


    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required
        load_factor = self.table_load()
        if load_factor >= 0.5:
            # print("load_factor=", self.table_load()) # TODO: DEBUG
            self.resize_table(self.capacity * 2)
        h = self.hash_function(key)
        i = h % self.buckets.length()

        if self.buckets[i] is None:
            self.buckets[i] = HashEntry(key, value)
            self.size += 1
        elif self.buckets[i].is_tombstone is True:
            self.buckets[i] = HashEntry(key, value)
        else: # self.buckets[i] is not None and self.buckets[i] is not a tombstone
            j = 0
            i_initial = i
            while self.buckets[i] is not None:
                # print("i=",i, "key=", key, "value=", value, "j=",j, "i_initial=", i_initial, "self.buckets[i]=", self.buckets[i], end=" ")
                if self.buckets[i].key == key:
                    if self.buckets[i].is_tombstone is False: # matching key and is not tombstone record
                        self.buckets[i].value = value
                        return
                    else:  # matching key and is tombstone record
                        self.buckets[i].value = value
                        self.buckets[i].is_tombstone = False
                        return
                else: # self.buckets[i] is not None and not matching key
                    if self.buckets[i].is_tombstone is True:
                        self.buckets[i] = HashEntry(key, value)
                        return
                    else:
                        j += 1
                        i = (i_initial + (j * j)) % self.capacity
                    # print("  new_i=", i)
                # print(self)
            if i != i_initial:
                # print("pt a key=", key, "prechange self.buckets[i]=", self.buckets[i])
                self.buckets[i] = HashEntry(key, value)
                self.size += 1

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        # quadratic probing required
        h = self.hash_function(key)
        i = h % self.buckets.length()
        j = 0
        i_initial = i
        while self.buckets[i] is not None:
            if self.buckets[i].is_tombstone is False:
                if self.buckets[i].key == key:
                    self.buckets[i].is_tombstone = True
                    self.size -= 1
                    return
            j += 1
            i = (i_initial + (j * j)) % self.capacity



    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        # quadratic probing required
        if self.size == 0:
            return False
        h = self.hash_function(key)
        i = h % self.buckets.length()
        j = 0
        i_initial = i
        while self.buckets[i] is not None:
            if self.buckets[i].is_tombstone is False:
                if self.buckets[i].key == key:
                    return True
            j += 1
            i = (i_initial + (j * j)) % self.capacity
        return False

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        """
        empty_buckets_count = 0
        for i in range(self.buckets.length()):
            if self.buckets[i] is None:
                empty_buckets_count += 1
            elif self.buckets[i].is_tombstone is True:
                empty_buckets_count += 1
        # print("empty_buckets=", empty_buckets_count, "self.size=", self.size, "self=", self)
        return empty_buckets_count


    def table_load(self) -> float:
        """
        TODO: Write this implementation
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1:
            return
        da = self.get_keys()
        old = HashMap(self.capacity, self.hash_function)
        old.size = self.size
        for i in range(self.capacity):
            old.buckets[i] = self.buckets[i]

        self.clear()
        self.capacity = new_capacity
        self.buckets = DynamicArray()
        for _ in range(new_capacity):
            self.buckets.append(None)

        for i in range(da.length()):
            # print("a")
            key = da[i]
            value = old.get(key)
            self.put(key, value)

        # print("old size=", old.size, "\n", old)
        # print("new size=", self.size, "\n", self)




    def get_keys(self) -> DynamicArray:
        """
        TODO: Write this implementations
        """
        da = DynamicArray()
        for i in range(self.capacity):
            if self.buckets[i] is not None and self.buckets[i].is_tombstone is False:
                da.append(self.buckets[i].key)
        return da


if __name__ == "__main__":

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)


    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # # this test assumes that put() has already been correctly implemented
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     # print(m.empty_buckets(), m.size, m.capacity)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     # if i % 10 == 9:
    #     #     print("i=", i, "empty_buckets=", m.empty_buckets(), "load=",m.table_load(), "size=",m.size, "cap=",m.capacity)
    #     if 29 <= i <= 39:
    #         print("i=", i, "empty_buckets=", m.empty_buckets(), "load=",m.table_load(), "size=",m.size, "cap=",m.capacity)


    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    # #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         result &= m.contains_key(str(key))
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))
    #
    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    #
    # m.resize_table(1)
    # print(m.get_keys())
    #
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())

    print("\nself- put example")
    print("-----------------------------")
    m = HashMap(40, hash_function_2)
    m.put('str0', 200)
    m.put('str1', 500)
    m.put('str10', 3000)
    m.put('str2', 800)
    m.put('str3', 1100)
    m.put('str4', 1400)
    m.put('str5', 1700)
    m.put('str6', 2000)
    m.put('str7', 2300)
    m.put('str8', 2600)
    m.put('str9', 2900)
    print("ori size=", m.size)
    # print(m)
    m.put('str10', 3100)
    print("new size=", m.size)
    # print(m)