/**
 * File: Wumpus.java
 *
 * Author: Brian Westerman
 *
 * Stores data for a Wumpus object for the arcade game Hunt the Wumpus.
 */

import java.awt.Graphics;
import java.awt.Image;
import javax.swing.*;

public class Wumpus extends Cell {
    /**
     * Inherited fields:
     * double x
     * double y
     */

    // The room the Wumpus makes its home in
    private Vertex home;
    // Whether the Wumpus is dead
    private boolean dead;
    // Whether the Wumpus is victorious over the hunter
    private boolean victorious;
    // Whether the Wumpus is visible
    private boolean visible;

    // Constructor
    public Wumpus(Vertex home) {
        super(0, 0);
        this.home = home;
        this.setPosition(this.home.getX(), this.home.getY());
        this.dead = false;
        this.victorious = false;
        this.visible = false;
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

    // Accessor for home
    public Vertex getHome() {
        return this.home;
    }

    // Modifier for home
    public void setHome(Vertex home) {
        this.home = home;
        this.setPosition(home.getX(), home.getY());
    }

    // Accessor for dead
    public boolean isDead() {
        return this.dead;
    }

    // Modifier for dead
    public void setDead(boolean dead) {
        this.dead = dead;
        if (this.dead) {
            this.setVisible(true);
        }
    }

    // Accessor for victorious
    public boolean isVictorious() {
        return this.victorious;
    }

    // Modifier for victorious
    public void setVictorious(boolean victorious) {
        this.victorious = victorious;
        if (this.victorious) {
            this.setVisible(true);
        }
    }

    // Accessor for visible
    public boolean isVisible() {
        return this.visible;
    }

    // Modifier for visible
    public void setVisible(boolean visible) {
        this.visible = visible;
    }

    // Checks whether the hunter is in the same room as the Wumpus - if so, the Wumpus eats the hunter
    public void checkHunter(Landscape scape) throws IllegalAccessError {
        // Find the hunter in the landscape's list of agents
        Hunter hunter = null;
        for (Cell cell : scape.getAgents()) {
            if (cell instanceof Hunter) {
                hunter = (Hunter) cell;
            }
        }
        if (hunter == null) {
            throw new IllegalAccessError("Error: hunter not found.");
        }
        if (hunter.getRoom().equals(this.getHome()) && !this.isDead()) {
            this.setVictorious(true);
            hunter = new Hunter(new Vertex("null", 0, 0));
            System.out.println("The Wumpus ate you. Game over.");
        }
    }

    // Updates the state of the Hunter
    @Override
    public void updateState(Landscape scape) {
        this.checkHunter(scape);
    }

    // Draws the room
    @Override
    public void draw(Graphics g, int x0, int y0, int scale) throws IllegalStateException {
        int xpos = x0 + (int) this.x * scale;
        int ypos = y0 + (int) this.y * scale;
        Image image = null;
        if (this.isDead() && this.isVisible()) {
            // The Wumpus is dead because the hunter killed it, draw it in black because it's dead
            image = new ImageIcon("dead_wumpus.png").getImage();
        } else if (this.isVictorious() && this.isVisible()) {
            // The Wumpus is victorious, draw it in red for eating the hunter
            image = new ImageIcon("wumpus.png").getImage();
        }
        g.drawImage(image, xpos - 11*scale, ypos - 11*scale, 20*scale, 20*scale, null);
        return;
    }

    public static void main(String[] args) {
        Wumpus wumpus = new Wumpus(new Vertex("test Wumpus", 100, 100));
        wumpus.setHome(new Vertex("test 2", 50, 50));
        wumpus.setDead(true);
        wumpus.setDead(false);
        wumpus.setVictorious(true);
        wumpus.checkHunter(new Landscape(200, 200));
        wumpus.updateState(new Landscape(200, 200));
    }

}
