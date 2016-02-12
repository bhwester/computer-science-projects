/**
 * File: HashMap.java
 *
 * Author: Brian Westerman
 *
 * Creates a HashMap that stores entries with a key and value.
 */

import java.util.Collection;

public class HashMap<K, V> {
    // An array holding all the entries
    private EntryNode[] entries;
    // The number of entries in the HashMap
    private int size;

    // Constructor
    public HashMap() {
        this.entries = new EntryNode[100];
        this.size = 0;
    }

    // Add a new entry to the HashMap, replacing an existing entry with the same key if need be
    public void put(Object key, Object value) {
        if (this.get(key) == null) {
            // Check if the array is at least half full; if it is, double the size of the array and copy all the entries in
            if (this.size >= this.entries.length / 2) {
                EntryNode[] oldEntries = this.entries;
                this.entries = new EntryNode[this.entries.length * 2];
                this.size = 0;
                for (EntryNode node : oldEntries) {
                    while (node != null) {
                        put(node.key, node.value);
                        node = node.next;
                    }
                }
            }
            // Add the new node
            int index = (key.hashCode() % this.entries.length);
            this.entries[index] = new EntryNode(key, value, this.entries[index]);
            this.size++;
        } else {
            // Replace the existing node with the new node
            EntryNode node = entries[key.hashCode() % entries.length];
            while (!node.key.equals(key)) {
                node = node.next;
            }
            node.value = value;
        }
    }

    // Get the value of the entry specified by key
    public Object get(Object key) {
        EntryNode node = this.entries[key.hashCode() % this.entries.length];
        while (node != null) {
            if (node.key.equals(key)) {
                return node.value;
            } else {
                node = node.next;
            }
        }
        return null;
    }

    // Get the number of entries in the HashMap
    public int size() { return this.size; }

    // Checks if the HashMap has 0 entries
    public boolean isEmpty() { return this.size == 0; }

    // Removes all entries from the HashMap and sets the size to 0
    public void clear() {
        this.size = 0;
        this.entries = new EntryNode[100];
    }

    // Accessor for entries
    public EntryNode[] getEntries() {
        return this.entries;
    }

    // Removes and returns the entry specified by key, otherwise returns null
    public Object remove(Object key) {
        Object value = get(key);
        if (value == null) {
            return null;
        } else {
            int index = (key.hashCode() % this.entries.length);
            if (entries[index].key.equals(key)) {
                this.entries[index] = this.entries[index].next;
            } else {
                EntryNode node = this.entries[index];
                while (! node.next.key.equals(key)) {
                    node = node.next;
                }
                node.next = node.next.next;
            }
            this.size--;
            return value;
        }
    }

    public static void main(String[] args) {
        HashMap map = new HashMap();
        map.put("Brian", 99);
        map.put("Mathias", 98);
        map.put("Alex", 97);
        map.put("Young", 96);
        map.put("Young", 95);
        map.put("Neil", 94);
        System.out.println(map.size());
        map.remove("Mathias");
        System.out.println(map.size());
        System.out.println("Brian: " + map.get("Brian"));
        System.out.println("Alex: " + map.get("Alex"));
        System.out.println("Young: " + map.get("Young"));
        System.out.println("Neil: " + map.get("Neil"));
    }

    private class EntryNode<T> {
        // The key for the entry
        public Object key;
        // The value for the entry
        public Object value;
        // The next node in the chain for the case of hashCode collisions
        public EntryNode next;

        // Constructor
        public EntryNode(Object key, Object object, EntryNode next) {
            this.key = key;
            this.value = object;
            this.next = next;
        }
    }

}
