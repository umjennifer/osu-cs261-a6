# Name: Jennifer Um
# OSU Email: umj@oregonstate.du
# Course: CS261 - Data Structures
# Assignment: 6 - Hash Map Implementation
# Due Date: 2022-03-11
# Description: Implement a hash map using chaining.

from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
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
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clear the contents of a hashmap without changing the underlying hash table capacity.
        :return: None
        """
        for i in range(self.buckets.length()):
            self.buckets.set_at_index(i, LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """
        Return the value associated with a key.
        :param key: key to find the value of
        :return:
            - Value associated with a key.
            - If key is not found, return none.
        """
        h = self.hash_function(key)
        i = h % self.buckets.length()
        node_matching_key = self.buckets.get_at_index(i).contains(key)

        if node_matching_key is not None:
            return node_matching_key.value
        return None


    def put(self, key: str, value: object) -> None:
        """
        Update the key/ value pair in the hash map.
            - If key exists, update associated value.
            - If key does not exist, add the key/ value pair.
        :param key: key of the node to update
        :param value: value of the key
        :return: none
        """
        h = self.hash_function(key)
        i = h % self.buckets.length()
        node_matching_key = self.buckets.get_at_index(i).contains(key)

        if node_matching_key is None:
            self.buckets.get_at_index(i).insert(key,value)
            self.size += 1
        else:
            self.buckets.get_at_index(i).remove(key)
            self.buckets.get_at_index(i).insert(key,value)


    def remove(self, key: str) -> None:
        """
        Remove a key and its associated value.
            - If a key is not in the hash map, do nothing.
        :param key: key of the node to be removed
        :return: none
        """
        h = self.hash_function(key)
        i = h % self.buckets.length()

        if self.buckets.get_at_index(i).contains(key):
            self.buckets.get_at_index(i).remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Check if a given key in the hash map.
        :param key: key to search for
        :return:
            - True if key is in the hash map
            - otherwise, return False
        """
        if self.size == 0:
            return False

        h = self.hash_function(key)
        i = h % self.buckets.length()

        if self.buckets.get_at_index(i).contains(key):
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        Get the number of empty buckets in a hash table
        :return: the number of empty buckets
        """
        empty_buckets_count = 0
        for i in range(self.buckets.length()):
            if self.buckets.get_at_index(i).length() == 0:
                empty_buckets_count += 1

        return empty_buckets_count

    def table_load(self) -> float:
        """
        Get the current hash table load factor.
        :return: the current hash table load factor
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal hash table.
            - Key / value pairs must remain the same.
            - Keys must be rehashed.
            - If new_capacity is less than one, do nothing.
        :param new_capacity: new capacity of the hash table
        :return: none
        """
        if new_capacity < 1:
            return

        da = self.get_keys()
        # create a hash map we can reference
        old = HashMap(self.capacity, self.hash_function)
        for i in range(self.capacity):
            old.buckets.set_at_index(i, self.buckets.get_at_index(i))

        # clear bucket and reset capacity, but keep size and hash function
        self.clear()
        self.capacity = new_capacity
        self.buckets = DynamicArray()

        for _ in range(new_capacity):
            self.buckets.append(LinkedList())

        for i in range(da.length()):
            key = da.get_at_index(i)
            value = old.get(key)
            self.put(key, value)

    def get_keys(self) -> DynamicArray:
        """
        Get a dynamic array of all the keys in the hash map.
            - Order does not matter.
        :return: a dynamic array of keys
        """
        da = DynamicArray()
        for i in range(self.capacity):
            for node in self.buckets.get_at_index(i):
                da.append(node.key)
        return da


# BASIC TESTING
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
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)
    #
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
    # #
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
    # print("pre", m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print("postadd",m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity, m)

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
    # print(m.size, m.capacity, m)
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
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    #
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))
    #
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
    # #
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
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'),"\n", m)

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

    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    # print("m.capacity=", m.capacity)
    # print(m)
    #
    # print()
    # m.resize_table(1)
    # print(m.get_keys())
    # print("m.capacity=", m.capacity)
    # print(m)

    # print()
    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
