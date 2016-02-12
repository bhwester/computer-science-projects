/**
 * File: Board.java
 *
 * Author: Brian Westerman
 *
 * Keeps track of, and draws, all the pieces on the board. This includes tile objects and a graph object that holds all
 * objects of type Vertx (where settlements, cities, and roads are stored).
 */

import java.lang.reflect.Array;
import java.util.ArrayList;

public class Board {
    // All the vertices on the board
    private Graph<Vertx> boardGraph;
    // A list of all the tiles on the board
    private ArrayList<Tile> tiles;
    // A list of all the ports on the board


    // Constructor
    public Board() {
        this.boardGraph = new Graph<>();
        this.tiles = new ArrayList<>();
    }

    // Accessor for boardGraph
    public Graph getBoardGraph() {
        return this.boardGraph;
    }

    // Accessor for vertices (type Vertx) behind boardGraph
    public ArrayList<Vertx> getVertices() {
        ArrayList<Vertx> vertices = new ArrayList<>();
        for (Vertex v : this.boardGraph.getVertices()) {
            vertices.add(v.getVertx());
        }
        return vertices;
    }

    // Accessor for tiles
    public ArrayList<Tile> getTiles() {
        return this.tiles;
    }

    // Set vertx to settlement
    public void setSettlement(Vertx v) {
        v.setType(Vertx.Type.SETTLEMENT);
    }

    // Set vertx to city
    public void setCity(Vertx v) {
        v.setType(Vertx.Type.CITY);
    }

    // Set two vertices contain a road between them
    public void setRoad(Vertx v1, Vertx v2) {
        // Check if they are adjacent vertices?
        v1.getEdges().put(v2, true);
        v2.getEdges().put(v1, true);
        // Roads never die!!!
    }

    public static void main(String[] args) {
        Game game = new Game(4);
        game.setUp();
        Board board0 = new Board();
        Board board = game.getBoard();
        board.getBoardGraph();
        board.getVertices();
        board.getTiles();
        board.setSettlement(new Vertx(0, 0));
        board.setCity(new Vertx(1, 1));
        board.setRoad(new Vertx(2, 2), new Vertx(3, 3));
        board0.getBoardGraph();
        board0.getVertices();
        board0.getTiles();
        board0.setSettlement(new Vertx(0, 0));
        board0.setCity(new Vertx(1, 1));
        board0.setRoad(new Vertx(2, 2), new Vertx(3, 3));
    }

}
