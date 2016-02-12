/**
 * File: LinkedList.java
 * Author: Brian Westerman
 * Date: 09/28/2015
 */

import java.util.*;

/*
 * Creates a LinkedList
 */

public class LinkedList<T> implements Iterable<T> {
    private Node head;
    private Node tail;
    private int numItems;

    private class Node {
        private Node next;
        private Node prev;
        private T data;

        public Node(T data) {
            this.next = null;
            this.prev = null;
            this.data = data;
        }

        public T getThing() {
            return this.data;
        }

        public void setNext(Node n) {
            this.next = n;
        }

        public void setPrev(Node n) {
            this.prev = n;
        }

        public Node getNext() {
            return this.next;
        }
    }

    private class LLIterator implements Iterator<T> {
        private Node nextNode;

        public LLIterator(Node head) {
            this.nextNode = head;
        }

        public Node getNext() {
            return this.nextNode;
        }

        public boolean hasNext() {
            return this.nextNode != null;
        }

        public T next() {
            T data = this.nextNode.getThing();
            this.nextNode = this.nextNode.getNext();
            return data;
        }

        public void remove() {

            while (this.hasNext()) {
                this.next();
            }
            this.nextNode = null;
        }
    }

    public LinkedList() {
        this.head = null;
        this.tail = null;
        this.numItems = 0;
    }

    public LLIterator iterator() {
        return new LLIterator(this.head);
    }

    public Node getHead() {
        return this.head;
    }

    public Node getTail() {
        return this.tail;
    }

    public T getData(Node node) {
        return node.getThing();
    }

    public T get(int index) {
        Node current = this.head;
        for (int i = 0; i < index; i++) {
            current = current.next;
        }
        return this.getData(current);
    }

    public void set(int index, T data) {
        Node current = this.head;
        for (int i = 0; i < index; i++) {
            current = current.next;
        }
        current.data = data;
    }

    public int size() {
        return this.numItems;
    }

    public boolean contains(T s) {
        Node current = this.head;
        while (current != null) {
            if (current.data.equals(s)) {
                return true;
            }
            current = current.next;
        }
        return false;
    }

    public void addFirst(T data) {
        Node newHead = new Node(data);
        if (this.head != null) {
            this.head.prev = newHead;
            newHead.setNext(this.head);
        }
        this.head = newHead;
        this.numItems++;
        if (this.size() == 1) {
            this.tail = newHead;
        }
    }

    public void append(T data) {
        Node newTail = new Node(data);
        if (this.head == null) {
            this.head = newTail;
            this.tail = newTail;
            this.numItems++;
        } else {
            this.tail.next = newTail;
            this.tail.next.prev = this.tail;
            this.tail = this.tail.next;
            this.numItems++;
        }
    }

    public void clear() {
        this.head = null;
        this.tail = null;
        this.numItems = 0;
    }

    public void delete(int index) {
        if (index == 0) {
            this.head = this.head.next;
            if (this.head != null) {
                this.head.prev = null;
            } else if (this.head == null) { // Fix?
                this.tail = null;
            }
            this.numItems--;
        } else if (index == this.size() - 1) {
            this.tail = this.tail.prev;
            this.tail.next = null;
            this.numItems--;
            if (this.tail == null) { // Fix?
                this.head = null;
            }
        } else if (index >= this.size()) {
            System.out.println("Error: out of bounds!");
        } else {
            Node current = this.head;
            for (int i = 0; i < index - 1; i++) {
                current = current.next;
            }
            current.next = current.next.next;
            current.next.prev = current.next.prev.prev;
            this.numItems--;
        }
    }

    public boolean remove(Object obj) {
        Node current = this.head;
        // If list is empty
        if (this.head == null) {
            return false;
        }
        // If list contains only one item
        if (this.head.next == null) {
            if (obj.equals(this.head.getThing())) {
                this.head = null;
                this.tail = null;
                this.numItems--;
                return true;
            }
            return false;
        }
        // If head contains obj
        if (this.head.getThing().equals(obj)) {
            this.head = this.head.next;
            this.head.prev = null;
            this.numItems--;
            return true;
        }
        // If tail contains obj
        // Make sure the method checks all members of the list before checking the tail
        if (this.tail.getThing().equals(obj)) {
            this.tail = this.tail.prev;
            this.tail.next = null;
            this.numItems--;
            return true;
        }
        if (obj == null) {
            for (T item : this) {
                while (this.tail != current.next) {
                    if (current.next.getThing().equals(null)) {
                        current.next = current.next.next;
                        current.next.prev = current.next.prev.prev;
                        this.numItems--;
                        return true;
                    }
                    current = current.next;
                }
            }
            return false;
        }
        for (T item : this) {
            while (this.tail != current.next) {
                if (obj.equals(current.next.getThing())) {
                    current.next = current.next.next;
                    current.next.prev = current.next.prev.prev;
                    this.numItems--;
                    return true;
                }
                current = current.next;
            }
        }
        return false;
    }

    public ArrayList<T> toArrayList() {
        ArrayList<T> arrayList = new ArrayList<T>();
        for (T data : this) {
            arrayList.add(data);
        }
        return arrayList;
    }

    public ArrayList<T> toShuffledList() {
        ArrayList<T> arrayList = this.toArrayList();
        Collections.shuffle(arrayList);
        return arrayList;
    }

    public static void main(String[] args) {

        LinkedList<Integer> llist = new LinkedList<Integer>();

        llist.addFirst(5);
        llist.addFirst(10);
        llist.addFirst(20);

        System.out.printf("\nAfter setup %d\n", llist.size());
        for(Integer item: llist) {
            System.out.printf("thing %d\n", item);
        }

        llist.clear();

        System.out.printf("\nAfter clearing %d\n", llist.size());
        for (Integer item: llist) {
            System.out.printf("thing %d\n", item);
        }

        for (int i=0; i<20; i+=2) {
            llist.addFirst(i);
        }

        System.out.printf("\nAfter setting %d\n", llist.size());
        for (Integer item: llist) {
            System.out.printf("thing %d\n", item);
        }

        ArrayList<Integer> alist = llist.toArrayList();
        System.out.printf("\nAfter copying %d\n", alist.size());
        for(Integer item: alist) {
            System.out.printf("thing %d\n", item);
        }

        alist = llist.toShuffledList();
        System.out.printf("\nAfter copying %d\n", alist.size());
        for(Integer item: alist) {
            System.out.printf("thing %d\n", item);
        }

        Integer x = new Integer(12);
        llist.remove(x);
        System.out.printf("\nAfter removing %d\n", x);
        for (Integer item: llist) {
            System.out.printf("thing %d\n", item);
        }
    }

}
