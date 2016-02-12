/**
 * File: Vertx.java
 * (I'm intentionally misspelling it Vertx because class Vertex is already used for making Graph)
 *
 * Author: Brian Westerman
 *
 * Stores the gamepieces for this game in each vertex on the board called vertx. Each gamepiece is positioned on a 
 * vertex in the graph. Each vertx can contain a settlement or city, or be open. Roads are stored as edges between two
 * vertx object.
 */

import java.awt.*;
import java.util.ArrayList;

public class Vertx extends Cell {
    /**
     * Inherited fields:
     * double x
     * double y
     */

    // Type each vertx can be; starts out as OPEN
    public enum Type { SETTLEMENT, CITY, OPEN }
    private Type type;
    // The player this vertx belongs to; starts out as null
    private Player player;
    // A HashMap of all the edges connected to this vertex indicating whether they contain a road with a boolean value
    // Key: Vertx edge points to; Value: boolean for whether there is a road on this edge
    private HashMap<Vertx, Boolean> edges;

    // Constructor
    public Vertx(double x, double y) {
        super(x, y);
        this.type = Type.OPEN;
        this.player = null;
        this.edges = new HashMap<>();
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

    // Accessor for type
    public Type getType() {
        return this.type;
    }

    // Modifier for type
    public void setType(Type type) {
        this.type = type;
    }

    // Accessor for player
    public Player getPlayer() {
        return this.player;
    }

    // Modifier for player
    public void setPlayer(Player player) {
        this.player = player;
    }

    // Accessor for edges
    public HashMap<Vertx, Boolean> getEdges() {
        return this.edges;
    }

    // Adds an edge from this vertx to v (bidirectional!!!)
    public void setEdge(Vertx v) {
        this.edges.put(v, false);
        v.getEdges().put(this, false);
    }

    // Checks if this vertx is open and there is at least one open vertx between this and the next occupied vertx
    // (settlement or city)
    public boolean isAvailableForSettling(Board board) {
        // Make a list of this vertx's edges
        ArrayList<Object> neighbors = new ArrayList<>();
        for (Object o : this.edges.getEntries()) {
            neighbors.add(o);
        }
        // If this vertx is open, check if the neighboring vertices (already connected by edges) are also open
        if (this.type == Type.OPEN) {
            // Check the neighboring vertices
            for (Object x : neighbors) {
                if (x instanceof Vertx) {
                    Type type = ((Vertx) x).getType();
                    if (type != Type.OPEN) {
                        // At least one neighboring vertx is not open; return false
                        return false;
                    }
                }
            }
            // All the neighboring vertices are open (as well as this vertx); return true
            return true;
        }
        // This vertex isn't open; return false
        return false;
    }

    // Updates the state of each vertx in the board
    public void updateState(Landscape scape) {
        // Don't need to do anything here; the game is updated in the method Game.advance()
    }

    // Draws each vertx in the landscape display
    public void draw(Graphics g, int x, int y, int scale, Game game) {
        double x0 = x + this.getX();
        double y0 = y + this.getY();
        // Set color to correspond to the player (maybe randomize depending on which color player goes in which order)
        Player player = this.getPlayer();
        if (player == game.getPlayers().get(0)) {
            g.setColor(new Color(0.9f, 0.1f, 0.0f));
        } else if (player == game.getPlayers().get(1)) {
            g.setColor(new Color(0.3f, 0.8f, 0.2f));
        } else if (player == game.getPlayers().get(2)) {
            g.setColor(new Color(0.0f, 0.4f, 0.9f));
        } else if (player == game.getPlayers().get(3)) {
            g.setColor(new Color(0.6f, 0.6f, 0.6f));
        }
        // If it's a road, draw a thick line between (x,y) and (x2,y2)
        // If it's a settlement, draw a settlement at (x,y)
        if (this.type == Type.SETTLEMENT) {
            g.fillOval((int) x0, (int) y0, 2, 2);
        }
        // If it's a city, draw a city at (x,y)
        if (this.type == Type.CITY) {
            g.fillOval((int) x0, (int) y0, 4, 4);
        }
    }

    // Overrides draw method from abstract class Cell
    @Override
    public void draw(Graphics g, int x, int y, int scale) {
        // Draw method already implemented, with an additional Game argument
    }

    public static void main(String[] args) {
        Game game = new Game(4);
        Vertx vertx1 = new Vertx(0, 0);
        Vertx vertx2 = new Vertx(1, 1);
        vertx1.setPlayer(new Player(1));
        vertx1.getPlayer();
        vertx1.setType(Type.CITY);
        vertx1.getType();
        vertx1.setEdge(vertx2);
        vertx1.getEdges();
        vertx1.isAvailableForSettling(game.getBoard());
    }

}

