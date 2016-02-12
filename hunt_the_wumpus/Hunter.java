/**
 * File: Hunter.java
 *
 * Author: Brian Westerman
 *
 * Stores data for a Hunter object for the arcade game Hunt the Wumpus.
 */

import java.awt.Graphics;
import java.awt.Image;
import javax.swing.*;
import java.util.ArrayList;

public class Hunter extends Cell {
    /**
     * Inherited fields:
     * double x
     * double y
     */

    // The room the hunter is currently in
    private Vertex room;
    // Whether the hunter's arrow is armed
    private boolean armed;
    // Where the hunter's arrow is aimed once it's armed
    public enum Direction { NORTH, EAST, SOUTH, WEST, NULL }
    private Direction aimed;

    // Constructor
    public Hunter(Vertex room) {
        super(0, 0);
        this.room = room;
        this.setPosition(this.room.getX(), this.room.getY());
        this.armed = false;
        this.aimed = Direction.NULL;
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

    // Accessor for room
    public Vertex getRoom() {
        return this.room;
    }

    // Modifier for room
    public void setRoom(Vertex room) {
        this.room = room;
        this.setPosition(room.getX(), room.getY());
    }

    // Accessor for armed
    public boolean isArmed() {
        return this.armed;
    }

    // Modifier for armed
    public void setArmed(boolean armed) {
        this.armed = armed;
    }

    // Accessor for aimed
    public Direction getAimed() {
        return this.aimed;
    }

    // Modifier for aimed
    public void setAimed(Direction aimed) {
        this.aimed = aimed;
    }

    // Shoots the hunter's arrow at the Wumpus
    public void shootArrow(Wumpus wumpus) {
        Vertex lair = wumpus.getHome();
        // Make sure the hunter's arrow is aimed somewhere
        if (this.getAimed() != Direction.NULL) {
            // Check North
            if (this.getAimed() == Direction.NORTH) {
                if (this.room.getNeighbor(Vertex.Direction.NORTH) != null &&
                        lair.equals(this.room.getNeighbor(Vertex.Direction.NORTH))) {
                    // The hunter hit the Wumpus
                    wumpus.setDead(true);
                    System.out.println("You killed the Wumpus, you win!");
                } else {
                    // The hunter missed the Wumpus and the Wumpus comes to eat the hunter
                    wumpus.setHome(this.room);
                    wumpus.setVictorious(true);
                    System.out.println("The Wumpus ate you. Game over.");
                }
            // Check East
            } else if (this.getAimed() == Direction.EAST) {
                if (this.room.getNeighbor(Vertex.Direction.EAST) != null &&
                        lair.equals(this.room.getNeighbor(Vertex.Direction.EAST))) {
                    // The hunter hit the Wumpus
                    wumpus.setDead(true);
                    System.out.println("You killed the Wumpus, you win!");
                } else {
                    // The hunter missed the Wumpus and the Wumpus comes to eat the hunter
                    wumpus.setHome(this.room);
                    wumpus.setVictorious(true);
                    System.out.println("The Wumpus ate you. Game over.");
                }
            // Check South
            } else if (this.getAimed() == Direction.SOUTH) {
                if (this.room.getNeighbor(Vertex.Direction.SOUTH) != null &&
                        lair.equals(this.room.getNeighbor(Vertex.Direction.SOUTH))) {
                    // The hunter hit the Wumpus
                    wumpus.setDead(true);
                    System.out.println("You killed the Wumpus, you win!");
                } else {
                    // The hunter missed the Wumpus and the Wumpus comes to eat the hunter
                    wumpus.setHome(this.room);
                    wumpus.setVictorious(true);
                    System.out.println("The Wumpus ate you. Game over.");
                }
            // Check West
            } else if (this.getAimed() == Direction.WEST) {
                if (this.room.getNeighbor(Vertex.Direction.WEST) != null &&
                        lair.equals(this.room.getNeighbor(Vertex.Direction.WEST))) {
                    // The hunter hit the Wumpus
                    wumpus.setDead(true);
                    System.out.println("You killed the Wumpus, you win!");
                } else {
                    // The hunter missed the Wumpus and the Wumpus comes to eat the hunter
                    wumpus.setHome(this.room);
                    wumpus.setVictorious(true);
                    System.out.println("The Wumpus ate you. Game over.");
                }
            }
        }
        this.setArmed(false);
        this.setAimed(Direction.NULL);
    }

    // Checks whether the Wumpus is within two rooms of the hunter's current position
    public boolean smellWumpus(Landscape scape) throws IllegalAccessError {
        // Find the Wumpus in the landscape's list of agents
        Wumpus wumpus = null;
        for (Cell cell : scape.getAgents()) {
            if (cell instanceof Wumpus) {
                wumpus = (Wumpus) cell;
            }
        }
        if (wumpus == null) {
            throw new IllegalAccessError("Error: hunter not found.");
        }
        // Find all the rooms within two rooms of the hunter
        ArrayList<Vertex> neighbors = this.room.getNeighbors();
        ArrayList<Vertex> neighborsOfNeighbors = new ArrayList<>();
        for (Vertex v : neighbors) {
            for (Vertex n : v.getNeighbors()) {
                neighborsOfNeighbors.add(n);
            }
        }
        // Check whether the Wumpus is in any of those rooms
        for (Vertex v : neighbors) {
            if (wumpus.getHome().equals(v) && !(wumpus.getHome().equals(this.room))) {
                System.out.println("The Wumpus's stench indicates that it is nearby...");
                return true;
            }
        }
        for (Vertex v : neighborsOfNeighbors) {
            if (wumpus.getHome().equals(v) && !(wumpus.getHome().equals(this.room))) {
                System.out.println("The Wumpus's stench indicates that it is nearby...");
                return true;
            }
        }
        return false;
    }

    // Updates the state of the hunter
    @Override
    public void updateState(Landscape scape) {
        this.smellWumpus(scape);
    }

    // Draws the room
    @Override
    public void draw(Graphics g, int x0, int y0, int scale) {
        int xpos = x0 + (int) this.x * scale;
        int ypos = y0 + (int) this.y * scale;
        Image image = new ImageIcon("hunter.png").getImage();
        g.drawImage(image, xpos - 11*scale, ypos - 11*scale, 20*scale, 20*scale, null);
        return;
    }

    public static void main(String[] args) {
        Hunter hunter = new Hunter(new Vertex("test hunter", 100, 100));
        hunter.setRoom(new Vertex("test 2", 50, 50));
        hunter.setArmed(true);
        hunter.setAimed(Direction.EAST);
        hunter.smellWumpus(new Landscape(200, 200));
        hunter.shootArrow(new Wumpus(hunter.getRoom()));
        hunter.updateState(new Landscape(200, 200));
    }

}
