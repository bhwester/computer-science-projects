/**
 * File: Vertex.java
 *
 * Author: Brian Westerman
 *
 * A vertex class that stores data for vertex objects that will be part of a Graph
 * In Hunt the Wumpus, stores the data for each room in the cave
 */

import java.lang.reflect.Array;
import java.awt.Graphics;
import java.awt.Color;
import java.util.*;

public class Vertex extends Cell implements Comparable<Vertex> {
    /**
     * Inherited fields:
     * double x
     * double y
     */

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
    // Whether the room has been visited by the hunter
    private boolean visible;
    // The "name" of each node
    private String label;
    // Whether the vertex is a pit
    private boolean pit;
    // Whether the vertex is a bat
    private boolean bats;

    // Constructor
    public Vertex(String label, double x, double y) {
        super(x, y);
        this.edges = new HashMap<>();
        this.freeEdges = new ArrayList<>();
        this.cost = 0;
        this.marked = false;
        this.visible = false;
        this.label = label;
        this.pit = false;
        this.bats = false;
    }

    /**
     * Inherited methods:
     * setPosition(double tx, double ty)
     * getX()
     * getCol()
     * getY()
     * getRow()
     * toString()
     */

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

    // Modifier for visible
    public void setVisible(boolean visible) {
        this.visible = visible;
    }

    // Accessor for label
    public String getLabel() {
        return this.label;
    }

    // Accessor for pit
    public boolean isPit() {
        return this.pit;
    }

    // Modifier for pit
    public void setPit(boolean pit) {
        this.pit = pit;
    }

    // Accessor for bat
    public boolean isBats() {
        return this.bats;
    }

    // Modifier for bats
    public void setBats(boolean bats) {
        this.bats = bats;
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

    // Connects this vertex to another vertex (bidirectional!!!)
    public void connect(Vertex to, Direction dir) {
        this.edges.put(dir, to);
        to.getEdges().put(opposite(dir), this);
    }

    // Connects this vertex to another vertex, without a cardinal direction (bidirectional!!!)
    public void connect(Vertex to) {
        this.freeEdges.add(to);
        to.getFreeEdges().add(this);
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
            neighbors.add(this.getNeighbor(Direction.NORTH));
        }
        if (this.getNeighbor(Direction.EAST) != null) {
            neighbors.add(this.getNeighbor(Direction.EAST));
        }
        if (this.getNeighbor(Direction.SOUTH) != null) {
            neighbors.add(this.getNeighbor(Direction.SOUTH));
        }
        if (this.getNeighbor(Direction.WEST) != null) {
            neighbors.add(this.getNeighbor(Direction.WEST));
        }
        return neighbors;
    }

    // Gets all edges that don't have a specified cardinal direction
    public ArrayList<Vertex> getFreeNeighbors() {
        return this.freeEdges;
    }

    // Prints out the number of neighbors, the cost, and whether this vertex is marked
    public String toString() {
        return this.getLabel() + ": Number of neighbors: " + this.getNeighbors().size()
                + ", cost: " + this.cost + ", marked: " + this.marked + ".";
    }

    // Implements a comparator
    public int compareTo(Vertex v) {
        return (this.cost - v.cost);
    }

    // Updates the state of the room
    @Override
    public void updateState(Landscape scape) {
        // Doesn't need to do anything
    }

    // Draws the room
    @Override
    public void draw(Graphics g, int x0, int y0, int scale) {
        if (!this.visible) return;

        int xpos = x0 + (int) this.x*scale;
        int ypos = y0 + (int) this.y*scale;
        int border = 2;
        int half = 10*scale / 2;
        int eighth = 10*scale / 8;
        int sixteenth = 10*scale / 16;

        // Draw rectangle for the walls of the cave
        if (this.cost <= 2) {
            // Wumpus is nearby
            g.setColor(Color.red);
        } else {
            // Wumpus is not nearby
            g.setColor(Color.black);
        }
        if (!this.isPit()) {
            g.drawRect(xpos + border - 11 * scale, ypos + border - 11 * scale, (scale * 20 - 2 * border), (scale * 20 - 2 * border));
        } else {
            g.fillRect(xpos + border - 11 * scale, ypos + border - 11 * scale, (scale * 20 - 2 * border), (scale * 20 - 2 * border));
        }
        // Draw doorways as boxes
        g.setColor(Color.black);
        if (this.edges.containsKey(Direction.NORTH)) {
            g.fillRect(xpos + border - 11 * scale + 27, ypos + border - 11 * scale, eighth + sixteenth, eighth);
        }
        if (this.edges.containsKey(Direction.SOUTH)) {
            g.fillRect(xpos + border - 11 * scale + 27, ypos + border - 11 * scale + (scale * 20 - 2 * border) - 3, eighth + sixteenth, eighth);
        }
        if (this.edges.containsKey(Direction.WEST)) {
            g.fillRect(xpos + border - 11 * scale, ypos + border - 11 * scale + 28, eighth, eighth + sixteenth);
        }
        if (this.edges.containsKey(Direction.EAST)) {
            g.fillRect(xpos + border - 11 * scale + (scale * 20 - 2 * border) - 3, ypos + border - 11 * scale + 28, eighth, eighth + sixteenth);
        }
    }

    public static void main(String[] args) {
        Vertex vertex1 = new Vertex("Brian", 0, 0);
        Vertex vertex2 = new Vertex("Kenny", 1, 1);
        Vertex vertex3 = new Vertex("Anne", 2, 2);
        Vertex vertex4 = new Vertex("Gary", 3, 3);
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
