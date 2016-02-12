/**
 * File: Vertex.java
 *
 * Author: Brian Westerman
 *
 * A vertex class that stores data for vertex objects that will be part of a Graph
 */

import java.lang.reflect.Array;
import java.util.*;

public class Vertex implements Comparable<Vertex> {
    // Enum for compass directions, clockwise from North
    public enum Direction { NORTH, EAST, SOUTH, WEST }
    // A HashMap of all the edges connected to this vertex that specify a cardinal direction
    private HashMap<Direction, Vertex> edges;
    // A list of all the edges connected to this vertex that don't specify a cardinal direction
    private ArrayList<Vertex> freeEdges;
    // The cost used in graph traversal
    private int cost;
    // Whether the vertex has been marked in graph traversal
    private boolean marked;
    // The "name" of each node
    private String label;

    //********
    // Holds a Vertx object for Project 8 - Settlers of Catan
    private Vertx vertx;
    //********

    // Generic constructor
    public Vertex(String label) {
        this.edges = new HashMap<>();
        this.freeEdges = new ArrayList<>();
        this.cost = 0;
        this.marked = false;
        this.vertx = null;
        this.label = label;
    }

    // Constructor for carrying a specified Vertx object for Settlers of Catan
    public Vertex(Vertx v) {
        this.edges = new HashMap<>();
        this.freeEdges = new ArrayList<>();
        this.cost = 0;
        this.marked = false;
        this.vertx = v;
        this.label = null;
    }

    // Accessor for vertx
    public Vertx getVertx() {
        return this.vertx;
    }

    // Modifier for vertx
    public void setVertx(Vertx v) {
        this.vertx = v;
    }

    // Accessor for edges
    public HashMap<Direction, Vertex> getEdges() {
        return this.edges;
    }

    // Accessor for freeEdges
    public ArrayList<Vertex> getFreeEdges() {
        return this.freeEdges;
    }

    // Accessor for cost
    public int getCost() {
        return this.cost;
    }

    // Modifier for cost
    public void setCost(int cost) {
        this.cost = cost;
    }

    // Accessor for marked
    public boolean isMarked() {
        return this.marked;
    }

    // Modifier for marked
    public void setMarked(boolean marked) {
        this.marked = marked;
    }

    // Accessor for label
    public String getLabel() {
        return this.label;
    }

    // Returns the compass opposite of a direction
    public static Direction opposite(Direction d) {
        if (d == Direction.NORTH) {
            return Direction.SOUTH;
        } else if (d == Direction.EAST) {
            return Direction.WEST;
        } else if (d == Direction.SOUTH) {
            return Direction.NORTH;
        } else {
            return Direction.EAST;
        }
    }

    // Connects this vertex to another vertex (unidirectional!!!)
    public void connect(Vertex to, Direction dir) {
        this.edges.put(dir, to);
    }

    // Connects this vertex to another vertex, without a cardinal direction (unidirectional!!!)
    public void connect(Vertex to) {
        this.freeEdges.add(to);
    }

    // Gets the neighboring vertex specified by dir
    public Vertex getNeighbor(Direction dir) {
        return (Vertex) this.edges.get(dir);
    }

    /*
    // Gets all four neighboring vertices
    public Collection<Vertex> getNeighbors() {
        return this.edges.values();
    }
    */

    // Gets all four neighboring vertices
    public ArrayList<Vertex> getNeighbors() {
        ArrayList<Vertex> neighbors = new ArrayList<>();
        if (this.getNeighbor(Direction.NORTH) != null) {
            neighbors.add(this);
        }
        if (this.getNeighbor(Direction.EAST) != null) {
            neighbors.add(this);
        }
        if (this.getNeighbor(Direction.SOUTH) != null) {
            neighbors.add(this);
        }
        if (this.getNeighbor(Direction.WEST) != null) {
            neighbors.add(this);
        }
        return neighbors;
    }

    // Gets all edges that don't have a specified cardinal direction
    public ArrayList<Vertex> getFreeNeighbors() {
        return this.freeEdges;
    }

    // Prints out the number of neighbors, the cost, and whether this vertex is marked
    public String toString() {
        return "Number of neighbors: " + this.getNeighbors().size()
                + ", cost: " + this.cost + ", marked: " + this.marked + ".";
    }

    // Implements a comparator
    public int compareTo(Vertex v) {
        return (this.cost - v.cost);
    }

    public static void main(String[] args) {
        Vertex vertex1 = new Vertex("Brian");
        Vertex vertex2 = new Vertex("Kenny");
        Vertex vertex3 = new Vertex("Anne");
        Vertex vertex4 = new Vertex("Gary");
        Vertex.opposite(Direction.NORTH);
        Vertex.opposite(Direction.EAST);
        Vertex.opposite(Direction.SOUTH);
        Vertex.opposite(Direction.WEST);
        vertex1.compareTo(vertex2);
        vertex1.connect(vertex2, Direction.NORTH);
        vertex1.connect(vertex3, Direction.EAST);
        vertex1.connect(vertex4, Direction.SOUTH);
    }

}
