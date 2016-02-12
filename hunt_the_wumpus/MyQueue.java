/**
 * File: MyQueue.java
 * Author: Brian Westerman
 * Date: 10/26/2015
 */

import java.util.*;
import java.util.Iterator;

/*
 * Creates a Queue
 */

public class MyQueue<T> implements Iterable<T> {
    private LinkedList<T> linkedList;
    private int maxSize;

    public MyQueue() {
        this.linkedList = new LinkedList<T>();
        this.maxSize = Integer.MAX_VALUE;
    }

    public MyQueue(int max) {
        this.linkedList = new LinkedList<T>();
        this.maxSize = max;
    }

    public Iterator<T> iterator() {
        return this.linkedList.iterator();
    }

    public LinkedList<T> getLinkedList() {
        return this.linkedList;
    }

    public int getMaxSize() {
        return this.maxSize;
    }

    // Store in another variable if using in a loop
    public int size() {
        return this.linkedList.size();
    }

    public boolean isEmpty() {
        return this.linkedList.size() == 0;
    }

    public boolean add(T data) throws IllegalStateException {
        if (this.size() < this.getMaxSize()) {
            this.linkedList.append(data);
            return true;
        } else {
            throw new IllegalStateException();
        }
    }

    public boolean offer(T data) {
        if (this.size() < this.getMaxSize()) {
            this.linkedList.append(data);
            return true;
        } else {
            return false;
        }
    }

    public T remove() throws NoSuchElementException {
        if (this.linkedList.getHead() != null) {
            T head = this.linkedList.get(0);
            this.linkedList.delete(0);
            return head;
        } else {
            throw new NoSuchElementException();
        }
    }

    public T poll() {
        if (this.linkedList.getHead() != null) {
            T head = this.linkedList.get(0);
            this.linkedList.delete(0);
            return head;
        } else {
            return null;
        }
    }

    public T element() throws NoSuchElementException {
        if (this.linkedList.getHead() != null) {
            return this.linkedList.get(0);
        } else {
            throw new NoSuchElementException();
        }
    }

    public T peek() {
        if (this.linkedList.getHead() != null) {
            return this.linkedList.get(0);
        } else {
            return null;
        }
    }

    public static void main(String[] args) {
        MyQueue<Integer> queue1 = new MyQueue<Integer>(5);
        MyQueue<Integer> queue2 = new MyQueue<Integer>(5);
        for (int i = 0; i < 5; i++) {
            queue1.add(i+1);
        }
        for (int i = 0; i < 5; i++) {
            queue2.offer(i + 1);
        }
        int size1 = queue1.size();
        for (int i = 0; i < size1; i++) {
            System.out.println("queue1 size: " + queue1.size());
            System.out.println(queue1.element());
            System.out.println(queue1.remove());
        }
        int size2 = queue2.size();
        for (int i = 0; i < size2; i++) {
            System.out.println("queue2 size: " + queue2.size());
            System.out.println(queue2.peek());
            System.out.println(queue2.poll());
        }
    }

}
