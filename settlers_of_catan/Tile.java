/**
 * File: Tile.java
 *
 * Author: Brian Westerman
 *
 * Produces a Tile object that carry a number between 2 and 12, an enumerated resource, and a position adjacent to other
 * cells, which all produce a hexagonal shape together on the board
 */

import java.awt.Graphics;
import java.awt.Color;
import java.util.ArrayList;

public class Tile extends Cell {
    /**
     * Inherited fields:
     * double x
     * double y
     */

    // ID number to simplify positioning
    private int id;
    // Roll number for adjacent settlements and cities
    private int rollNum;
    // Five resources that each tile can possess one of (plus one Desert tile)
    // 4 wood, 3 brick, 4 sheep, 4 wheat, 3 ore, 1 desert
    public enum Resource { WOOD, BRICK, SHEEP, WHEAT, ORE, DESERT }
    private Resource resource;
    // Boolean for if the tile has a robber on it
    private boolean hasRobber;
    // A list of vertices this tile is adjacent to
    private ArrayList<Vertx> vertices;

    // Constructor
    public Tile(double x0, double y0, int id, int roll, Resource r) {
        super(x0, y0);
        this.id = id;
        this.rollNum = roll;
        this.resource = r;
        this.hasRobber = (this.resource == Resource.DESERT);
        this.vertices = new ArrayList<Vertx>();
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

    // Accessor for ID
    public int getId() {
        return this.id;
    }

    // Modifier for ID
    public void setId(int id) {
        this.id = id;
    }

    // Accessor for rollNum
    public int getRollNum() {
        return this.rollNum;
    }

    // Modifier for rollNum
    public void setRollNum(int roll) {
        this.rollNum = roll;
    }

    // Accessor for resource
    public Resource getResource() {
        return this.resource;
    }

    // Mutator for resource
    public void setResource(Resource r) {
        this.resource = r;
    }

    // Accessor for hasRobber
    public boolean hasRobber() {
        return this.hasRobber;
    }

    // Mutator for hasRobber
    public void setRobber(boolean robber) {
        this.hasRobber = robber;
    }

    // Accessor for gamepieces
    public ArrayList<Vertx> getVertices() {
        return this.vertices;
    }

    // Gives resources to players who have gamepieces adjacent to this tile
    public void giveResources() {
        // If this isn't a desert piece and doesn't have a robber piece sitting on it
        if (!this.hasRobber() && this.resource != Resource.DESERT) {
            for (Vertx vertex : vertices) {
                Vertx.Type type = vertex.getType();
                if (type == Vertx.Type.SETTLEMENT) {
                    // Add one resource of this type to the hand of the player who owns a settlement on this vertex
                    vertex.getPlayer().addResource(this.resource);
                } else if (type == Vertx.Type.CITY) {
                    // Add two resources of this type to the hand of the player who owns a city on this vertex
                    vertex.getPlayer().addResource(this.resource);
                    vertex.getPlayer().addResource(this.resource);
                }
                // Otherwise nothing happens with this OPEN vertex
            }
        }
        // Otherwise this tile doesn't distribute resources
    }

    // Updates the state of each tile in the board
    public void updateState(Landscape scape) {
        // Don't need to do anything here; the game is updated in the method Game.advance()
    }

    // Draws the tile in the landscape display
    public void draw(Graphics g, int x, int y, int scale, Game game) {
        double x0 = x + this.getX();
        double y0 = y + this.getY();
        if (this.equals(game.getBoard().getTiles().get(9))) {
            g.setColor(new Color(0.1f, 0.8f, 0.9f));
            g.fillOval((int) this.getX(), (int) this.getY(), 100, 100);
        }
        // Color depends on the resource and position depends on (x,y)
        if (this.getResource() == Resource.WOOD) {
            g.setColor(new Color(0.1f, 0.5f, 0.1f));
        } else if (this.getResource() == Resource.BRICK) {
            g.setColor(new Color(0.6f, 0.5f, 0.2f));
        } else if (this.getResource() == Resource.SHEEP) {
            g.setColor(new Color(0.5f, 0.9f, 0.2f));
        } else if (this.getResource() == Resource.WHEAT) {
            g.setColor(new Color(0.9f, 0.8f, 0.2f));
        } else if (this.getResource() == Resource.ORE){
            g.setColor(new Color(0.7f, 0.7f, 0.7f));
        } else if (this.getResource() == Resource.DESERT) {
            g.setColor(new Color(1.0f, 1.0f, 0.7f));
        }
        // Draw a vertical hexagon centered at (x,y) that depends on scale
        int[] xPoints = {(int)(this.getX()-(Game.SCALE/12)*(Math.sqrt(3)/2)), (int)this.getX(), (int)(this.getX()+(Game.SCALE/12)*(Math.sqrt(3)/2)),
                (int)(this.getX()+(Game.SCALE/12)*(Math.sqrt(3)/2)), (int)this.getX(), (int)(this.getX()-(Game.SCALE/12)*(Math.sqrt(3)/2))};
        int[] yPoints = {(int)(this.getY()-(Game.SCALE/24)), (int)(this.getY()-(Game.SCALE/12)), (int)(this.getY()-(Game.SCALE/24)),
                (int)(this.getY()+(Game.SCALE/24)), (int)(this.getY()+(Game.SCALE/12)), (int)(this.getY()+(Game.SCALE/24))};
        g.fillPolygon(xPoints, yPoints, 6);
        // if this tile is occupied by the robber, draw a circle representing the robber in the center
        g.setColor(new Color(0.9f, 0.1f, 0.9f));
        if (this.hasRobber) {
            g.fillOval((int) x0, (int) y0, 5, 5);
        }
    }

    // Overrides draw method from abstract class Cell
    @Override
    public void draw(Graphics g, int x, int y, int scale) {
        // Draw method already implemented, with an additional Game argument
    }

    public static void main(String[] args) {
        Game game = new Game(4);
        Tile tile = new Tile(0, 0, 1, 6, Resource.WOOD);
        tile.setId(2);
        tile.getId();
        tile.setRollNum(8);
        tile.getRollNum();
        tile.setResource(Resource.BRICK);
        tile.getResource();
        tile.setRobber(true);
        tile.hasRobber();
        tile.getVertices();
        tile.giveResources();
    }

}
