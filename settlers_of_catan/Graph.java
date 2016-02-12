/**
 * File: Graph.java
 *
 * Author: Brian Westerman
 *
 * Creates a graph that stores Vertex objects and associated data
 */

import java.util.*;

public class Graph<T> {
    // A list of the vertices in the graph
    private ArrayList<Vertex> vertices;
    // The number of vertices in the graph
    private int size;

    public Graph() {
        this.vertices = new ArrayList<>();
        this.size = 0;
    }

    // Accessor for vertices
    public ArrayList<Vertex> getVertices() {
        return this.vertices;
    }

    // Counts the number of vertices in the graph
    public int vertexCount() {
        return this.size;
    }

    // Adds v to the graph
    public void addVertex(Vertex v) {
        this.vertices.add(v);
        this.size++;
    }

    // Removes v from the graph
    public void remove(Vertex vertex) {
        if (this.vertices.remove(vertex)) {
            this.size--;
        } else {
            System.out.println("Error: vertex not found.");
        }
    }

    // Clears all vertices from the graph
    public void clear() {
        this.vertices.clear();
        this.size = 0;
    }

    // Adds v1 and v2 to the graph (if necessary) and adds edges connecting v1 to v2 via direction dir and connecting
    // v2 to v1 via the opposite direction (bidirectional!!!)
    public void addEdge(Vertex v1, Vertex.Direction dir, Vertex v2) {
        // Check if v1 and v2 are already in the graph
        boolean v1inGraph = false;
        boolean v2inGraph = false;
        for (Vertex v : this.vertices) {
            if (v1.equals(v)) {
                v1inGraph = true;
            }
            if (v2.equals(v)) {
                v2inGraph = true;
            }
        }
        // If v1 isn't in the graph, add it to the graph
        if (!v1inGraph) {
            this.addVertex(v1);
        }
        // If v2 isn't in the graph, add it to the graph
        if (!v2inGraph) {
            this.addVertex(v2);
        }
        v1.connect(v2, dir);
        v2.connect(v1, Vertex.opposite(dir));
    }

    // Adds v1 and v2 to the graph (if necessary) and adds edges connecting v1 to v2 and v2 to v1 (bidirectional!!!)
    public void addEdge(Vertex v1, Vertex v2) {
        // Check if v1 and v2 are already in the graph
        boolean v1inGraph = false;
        boolean v2inGraph = false;
        for (Vertex v : this.vertices) {
            if (v1.equals(v)) {
                v1inGraph = true;
            }
            if (v2.equals(v)) {
                v2inGraph = true;
            }
        }
        // If v1 isn't in the graph, add it to the graph
        if (!v1inGraph) {
            this.addVertex(v1);
        }
        // If v2 isn't in the graph, add it to the graph
        if (!v2inGraph) {
            this.addVertex(v2);
        }
        v1.connect(v2);
        v2.connect(v1);
    }

    // Adds v1 and v2 to the graph (if necessary) and adds a unidirectional edge connecting v1 to v2
    public void addEdgeUnidirectional(Vertex v1, Vertex v2) {
        // Check if v1 and v2 are already in the graph
        boolean v1inGraph = false;
        boolean v2inGraph = false;
        for (Vertex v : this.vertices) {
            if (v1.equals(v)) {
                v1inGraph = true;
            }
            if (v2.equals(v)) {
                v2inGraph = true;
            }
        }
        // If v1 isn't in the graph, add it to the graph
        if (!v1inGraph) {
            this.addVertex(v1);
        }
        // If v2 isn't in the graph, add it to the graph
        if (!v2inGraph) {
            this.addVertex(v2);
        }
        v1.connect(v2);
    }

    // Implements a single-source shortest-path algorithm for the graph (Dijkstra's algorithm)
    public void shortestPath(Vertex v0) {
        for (Vertex v : this.vertices) {
            v.setCost(Integer.MAX_VALUE);
        }
        PriorityQueue<Vertex> pq = new PriorityQueue<>();
        // Set comparator to order vertices by lowest cost
        // Is that already the default? Built-in PriorityQueue orders its elements according to their "natural ordering"
        v0.setCost(0);
        pq.add(v0);
        while (pq.size() != 0) {
            Vertex v = pq.poll();
            v.setMarked(true);
            for (Vertex neighbor : v.getNeighbors()) { // Careful if using non-cardinal direction vertices - use getFreeNeighbors() instead
                if (! neighbor.isMarked()) {
                    neighbor.setCost(v.getCost() + 1);
                    pq.remove(neighbor);
                    pq.add(neighbor);
                }
            }
        }
        // Output: the resulting cost of each vertex v in the graph is the shortest distance from v0 to v
    }

    public static void main(String[] args) {
        Graph graph = new Graph<>();
        Vertex vertex1 = new Vertex("Brian");
        Vertex vertex2 = new Vertex("Kenny");
        Vertex vertex3 = new Vertex("Anne");
        Vertex vertex4 = new Vertex("Gary");
        Vertex vertex5 = new Vertex("Grammy");
        Vertex vertex6 = new Vertex("Grandad");
        graph.addVertex(vertex1);
        graph.addVertex(vertex2);
        graph.addVertex(vertex3);
        graph.addVertex(vertex4);
        graph.addVertex(vertex5);
        graph.addVertex(vertex6);
        graph.addEdge(vertex1, Vertex.Direction.NORTH, vertex2);
        graph.addEdge(vertex1, Vertex.Direction.EAST, vertex3);
        graph.addEdge(vertex1, Vertex.Direction.SOUTH, vertex4);
        graph.addEdge(vertex1, Vertex.Direction.WEST, vertex5);
        graph.shortestPath(vertex1);
        vertex1.compareTo(vertex2);
    }

}
