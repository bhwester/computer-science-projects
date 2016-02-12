/**
 * File: HuntTheWumpus.java
 *
 * Author: Brian Westerman
 *
 * Runs a game of Hunt the Wumpus.
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.Random;
import java.util.ArrayList;

public class HuntTheWumpus {
    // Stores the game's Landscape
    public Landscape scape;
    // Stores the game's LandscapeDisplay
    public LandscapeDisplay display;
    // Stores the game's Graph
    public Graph<Vertex> graph;
    // Stores the game's Hunter
    public Hunter hunter;
    // Stores the game's Wumpus
    public Wumpus wumpus;
    // Status of the game
    public enum GameState { PLAY, PAUSE, STOP }
    private GameState state;
    // User input into the command line
    private JLabel textMessage;
    // The number of milliseconds to pause between iterations
    private int pause;
    // Simulation control
    private int iteration;

    // Constructor
    public HuntTheWumpus() {
        Random r = new Random();
        this.scape = new Landscape(200, 200);
        this.display = new LandscapeDisplay(this.scape, 3);
        // Set up a random graph created from 25 nodes
        this.graph = new Graph<>();
        this.newGraph(this.scape);
        // Place the hunter and the Wumpus on a random vertex in the graph
        ArrayList<Vertex> rooms = this.graph.getVertices();
        Vertex hunterRoom = rooms.get(r.nextInt(rooms.size()));
        Vertex wumpusHome = rooms.get(r.nextInt(rooms.size()));
        // Give the hunter a different vertex if it's the same as the Wumpus's vertex
        while (wumpusHome.equals(hunterRoom)) {
            hunterRoom = rooms.get(r.nextInt(rooms.size()));
        }
        this.hunter = new Hunter(hunterRoom);
        this.wumpus = new Wumpus(wumpusHome);
        rooms.get(r.nextInt(rooms.size())).setPit(true);
        rooms.get(r.nextInt(rooms.size())).setBats(true);
        this.state = GameState.PLAY;
        // Set up the UI controls
        this.setupUI();
        this.pause = 100;
        // Add all Cell objects to the landscape
        this.scape.addAgent(this.hunter);
        this.scape.addAgent(this.wumpus);
        for (Object v : this.graph.getVertices()) {
            this.scape.addAgent((Vertex) v);
        }
        this.iteration = 0;
    }

    // Sets up a new graph created from 25 nodes with edges between adjacent nodes
    public void newGraph(Landscape scape) {
        double width = scape.getWidth();
        double height = scape.getHeight();
        // Initialize 25 vertices in a grid and add them to the graph
        Vertex v1 = new Vertex("1", width*1/10, height*1/10);
        Vertex v2 = new Vertex("2", width*3/10, height*1/10);
        Vertex v3 = new Vertex("3", width*5/10, height*1/10);
        Vertex v4 = new Vertex("4", width*7/10, height*1/10);
        Vertex v5 = new Vertex("5", width*9/10, height*1/10);
        Vertex v6 = new Vertex("6", width*1/10, height*3/10);
        Vertex v7 = new Vertex("7", width*3/10, height*3/10);
        Vertex v8 = new Vertex("8", width*5/10, height*3/10);
        Vertex v9 = new Vertex("9", width*7/10, height*3/10);
        Vertex v10 = new Vertex("10", width*9/10, height*3/10);
        Vertex v11 = new Vertex("11", width*1/10, height*5/10);
        Vertex v12 = new Vertex("12", width*3/10, height*5/10);
        Vertex v13 = new Vertex("13", width*5/10, height*5/10);
        Vertex v14 = new Vertex("14", width*7/10, height*5/10);
        Vertex v15 = new Vertex("15", width*9/10, height*5/10);
        Vertex v16 = new Vertex("16", width*1/10, height*7/10);
        Vertex v17 = new Vertex("17", width*3/10, height*7/10);
        Vertex v18 = new Vertex("18", width*5/10, height*7/10);
        Vertex v19 = new Vertex("19", width*7/10, height*7/10);
        Vertex v20 = new Vertex("20", width*9/10, height*7/10);
        Vertex v21 = new Vertex("21", width*1/10, height*9/10);
        Vertex v22 = new Vertex("22", width*3/10, height*9/10);
        Vertex v23 = new Vertex("23", width*5/10, height*9/10);
        Vertex v24 = new Vertex("24", width*7/10, height*9/10);
        Vertex v25 = new Vertex("25", width*9/10, height*9/10);
        this.graph.addVertex(v1);
        this.graph.addVertex(v2);
        this.graph.addVertex(v3);
        this.graph.addVertex(v4);
        this.graph.addVertex(v5);
        this.graph.addVertex(v6);
        this.graph.addVertex(v7);
        this.graph.addVertex(v8);
        this.graph.addVertex(v9);
        this.graph.addVertex(v10);
        this.graph.addVertex(v11);
        this.graph.addVertex(v12);
        this.graph.addVertex(v13);
        this.graph.addVertex(v14);
        this.graph.addVertex(v15);
        this.graph.addVertex(v16);
        this.graph.addVertex(v17);
        this.graph.addVertex(v18);
        this.graph.addVertex(v19);
        this.graph.addVertex(v20);
        this.graph.addVertex(v21);
        this.graph.addVertex(v22);
        this.graph.addVertex(v23);
        this.graph.addVertex(v24);
        this.graph.addVertex(v25);
        // Add edges between vertices
        v1.connect(v2, Vertex.Direction.EAST);
        v2.connect(v3, Vertex.Direction.EAST);
        v3.connect(v4, Vertex.Direction.EAST);
        v4.connect(v5, Vertex.Direction.EAST);
        v6.connect(v7, Vertex.Direction.EAST);
        v7.connect(v8, Vertex.Direction.EAST);
        v8.connect(v9, Vertex.Direction.EAST);
        v9.connect(v10, Vertex.Direction.EAST);
        v11.connect(v12, Vertex.Direction.EAST);
        v12.connect(v13, Vertex.Direction.EAST);
        v13.connect(v14, Vertex.Direction.EAST);
        v14.connect(v15, Vertex.Direction.EAST);
        v16.connect(v17, Vertex.Direction.EAST);
        v17.connect(v18, Vertex.Direction.EAST);
        v18.connect(v19, Vertex.Direction.EAST);
        v19.connect(v20, Vertex.Direction.EAST);
        v21.connect(v22, Vertex.Direction.EAST);
        v22.connect(v23, Vertex.Direction.EAST);
        v23.connect(v24, Vertex.Direction.EAST);
        v24.connect(v25, Vertex.Direction.EAST);
        v1.connect(v6, Vertex.Direction.SOUTH);
        v6.connect(v11, Vertex.Direction.SOUTH);
        v11.connect(v16, Vertex.Direction.SOUTH);
        v16.connect(v21, Vertex.Direction.SOUTH);
        v2.connect(v7, Vertex.Direction.SOUTH);
        v7.connect(v12, Vertex.Direction.SOUTH);
        v12.connect(v17, Vertex.Direction.SOUTH);
        v17.connect(v22, Vertex.Direction.SOUTH);
        v3.connect(v8, Vertex.Direction.SOUTH);
        v8.connect(v13, Vertex.Direction.SOUTH);
        v13.connect(v18, Vertex.Direction.SOUTH);
        v18.connect(v23, Vertex.Direction.SOUTH);
        v4.connect(v9, Vertex.Direction.SOUTH);
        v9.connect(v14, Vertex.Direction.SOUTH);
        v14.connect(v19, Vertex.Direction.SOUTH);
        v19.connect(v24, Vertex.Direction.SOUTH);
        v5.connect(v10, Vertex.Direction.SOUTH);
        v10.connect(v15, Vertex.Direction.SOUTH);
        v15.connect(v20, Vertex.Direction.SOUTH);
        v20.connect(v25, Vertex.Direction.SOUTH);
    }

    // Checks whether the hunter is on a pit or whether it is neighboring a pit
    public void checkPit() {
        Vertex room = this.hunter.getRoom();
        // If the hunter is on a pit, immobilize the hunter
        if (room.isPit()) {
            System.out.println("You fell into a pit and died! Game over.");
            this.hunter = new Hunter(new Vertex("null", 0, 0));
        }
        // Give feedback if the hunter is neighboring a pit
        for (Vertex v : room.getNeighbors()) {
            if (v.isPit()) {
                System.out.println("You feel a breeze...");
            }
        }
    }

    // Checks whether the hunter is in a room with bats
    public void checkBats() {
        Random r = new Random();
        if (this.hunter.getRoom().isBats()) {
            // Send the hunter to a random room by reassigning its vertex to a random vertex in the graph
            this.hunter.setRoom(this.graph.getVertices().get(r.nextInt(this.graph.getVertices().size())));
            System.out.println("You were carried to a different room by bats!");
        }
    }

    // Checks whether the game is completed
    public void checkGameOver() {
        // If the Wumpus is dead or victorious (therefore visible), immobilize the hunter by replacing it with a new hunter not on the graph
        if (this.wumpus.isVisible()) {
            this.hunter = new Hunter(new Vertex("null", 0, 0));
        }
    }

    // Sets up the UI controls for the Hunt the Wumpus simulation
    private void setupUI() {
        // Add elements to the UI
        this.textMessage = new JLabel("Your text here.");
        JButton pause = new JButton("Pause");
        JButton quit = new JButton("Quit");
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        panel.add(this.textMessage);
        panel.add(pause);
        panel.add(quit);
        this.display.add(panel, BorderLayout.SOUTH);
        this.display.pack();
        // Listen for keystrokes
        Control control = new Control();
        pause.addActionListener(control);
        quit.addActionListener(control);
        this.display.addKeyListener(control);
        this.display.setFocusable(true);
        this.display.requestFocus();
    }

    // Provides simple keyboard control to the simulation by implementing the KeyListener interface
    private class Control extends KeyAdapter implements ActionListener {
        // Controls the simulation in response to key presses
        public void keyTyped(KeyEvent e) {
            Random r = new Random();
            // While the game is in play, "p" pauses the game
            if (("" + e.getKeyChar()).equalsIgnoreCase("p") &&
                    state == GameState.PLAY) {
                state = GameState.PAUSE;
                System.out.println("*** Simulation paused ***");
            // While the game is paused, "p" puts the game in play
            } else if (("" + e.getKeyChar()).equalsIgnoreCase("p") &&
                    state == GameState.PAUSE) {
                state = GameState.PLAY;
                System.out.println("*** Simulation resumed ***");
            // Hitting the space bar arms the hunter
            } else if (("" + e.getKeyChar()).equalsIgnoreCase(" ") &&
                    state == GameState.PLAY) {
                if (!hunter.isArmed()) {
                    // The hunter isn't armed, arm the hunter's arrow
                    hunter.setArmed(true);
                } else if (!(hunter.getAimed() == Hunter.Direction.NULL)) {
                    // The hunter is armed and is aiming the arrow, so shoot the arrow
                    hunter.shootArrow(wumpus);
                } else {
                    // The hunter is armed but isn't aiming the arrow, so disarm the arrow
                    hunter.setArmed(false);
                }
            // "w" moves the hunter one space North or aims the arrow North
            } else if (("" + e.getKeyChar()).equalsIgnoreCase("w") &&
                    state == GameState.PLAY) {
                if (hunter.isArmed()) {
                    // The hunter is armed, aim the hunter's arrow North
                    hunter.setAimed(Hunter.Direction.NORTH);
                } else {
                    // The hunter isn't armed, move the hunter one space North and make the room visible
                    if (hunter.getRoom().getNeighbor(Vertex.Direction.NORTH) != null) {
                        hunter.setRoom(hunter.getRoom().getNeighbor(Vertex.Direction.NORTH));
                        hunter.getRoom().setVisible(true);
                    }
                }
            // "a" moves the hunter one space West or aims the arrow West
            } else if (("" + e.getKeyChar()).equalsIgnoreCase("a") &&
                    state == GameState.PLAY) {
                if (hunter.isArmed()) {
                    // The hunter is armed, aim the hunter's arrow West
                    hunter.setAimed(Hunter.Direction.WEST);
                } else {
                    // The hunter isn't armed, move the hunter one space West and make the room visible
                    if (hunter.getRoom().getNeighbor(Vertex.Direction.WEST) != null) {
                        hunter.setRoom(hunter.getRoom().getNeighbor(Vertex.Direction.WEST));
                        hunter.getRoom().setVisible(true);
                    }
                }
            // "s" moves the hunter one space South or aims the arrow South
            } else if (("" + e.getKeyChar()).equalsIgnoreCase("s") &&
                    state == GameState.PLAY) {
                if (hunter.isArmed()) {
                    // The hunter is armed, aim the hunter's arrow South
                    hunter.setAimed(Hunter.Direction.SOUTH);
                } else {
                    // The hunter isn't armed, move the hunter one space South and make the room visible
                    if (hunter.getRoom().getNeighbor(Vertex.Direction.SOUTH) != null) {
                        hunter.setRoom(hunter.getRoom().getNeighbor(Vertex.Direction.SOUTH));
                        hunter.getRoom().setVisible(true);
                    }
                }
            // "d" moves the hunter one space East or aims the arrow East
            } else if (("" + e.getKeyChar()).equalsIgnoreCase("d") &&
                    state == GameState.PLAY) {
                if (hunter.isArmed()) {
                    // The hunter is armed, aim the hunter's arrow East
                    hunter.setAimed(Hunter.Direction.EAST);
                } else {
                    // The hunter isn't armed, move the hunter one space East and make the room visible
                    if (hunter.getRoom().getNeighbor(Vertex.Direction.EAST) != null) {
                        hunter.setRoom(hunter.getRoom().getNeighbor(Vertex.Direction.EAST));
                        hunter.getRoom().setVisible(true);
                    }
                }
            // "r" replays the game, resetting it to its initial characteristics
            } else if (("" + e.getKeyChar()).equalsIgnoreCase("r")) {
                state = GameState.PLAY;
                scape = new Landscape(200, 200);
                display.dispose();
                display = new LandscapeDisplay(scape, 3);
                setupUI();
                graph = new Graph<>();
                newGraph(scape);
                // Place the hunter and the Wumpus on a random vertex in the graph
                ArrayList<Vertex> rooms = graph.getVertices();
                Vertex hunterRoom = rooms.get(r.nextInt(rooms.size()));
                Vertex wumpusHome = rooms.get(r.nextInt(rooms.size()));
                // Give the hunter a different vertex if it's the same as the Wumpus's vertex
                while (wumpusHome.equals(hunterRoom)) {
                    hunterRoom = rooms.get(r.nextInt(rooms.size()));
                }
                hunter = new Hunter(hunterRoom);
                wumpus = new Wumpus(wumpusHome);
                rooms.get(r.nextInt(rooms.size())).setPit(true);
                rooms.get(r.nextInt(rooms.size())).setBats(true);
                scape.addAgent(hunter);
                scape.addAgent(wumpus);
                for (Object v : graph.getVertices()) {
                    scape.addAgent((Vertex) v);
                }
                System.out.println("*** New game started ***");
                iteration = 0;
                iterate();
            // "q" quits the game
            } else if (("" + e.getKeyChar()).equalsIgnoreCase("q")) {
                state = GameState.STOP;
                System.out.println("*** Simulation ended ***");
            }
        }

        // Allow the user to type input to play, pause, or quit the game
        public void actionPerformed(ActionEvent event) {
            System.out.println(event.getActionCommand());

            if (event.getActionCommand().equalsIgnoreCase("Pause") &&
                    state == GameState.PLAY) {
                state = GameState.PAUSE;
                ((JButton) event.getSource()).setText("Play");
            } else if (event.getActionCommand().equalsIgnoreCase("Play") &&
                    state == GameState.PAUSE) {
                state = GameState.PLAY;
                ((JButton) event.getSource()).setText("Pause");
            } else if (event.getActionCommand().equalsIgnoreCase("Quit")) {
                state = GameState.STOP;
            }
        }

    }

    // Implements one iteration (time step) of the elevator simulation
    public void iterate() {
        this.iteration++;
        if (this.state == GameState.PLAY) {
            // update the landscape, display
            this.graph.shortestPath(this.wumpus.getHome());
            this.checkPit();
            this.checkBats();
            this.checkGameOver();
            this.scape.advance();
            this.display.repaint();
        }
        // Pause for refresh
        try {
            Thread.sleep(this.pause);
        } catch (InterruptedException ie) {
            // do threads get insomnia? YAHHHHHH
            ie.printStackTrace();
        }
    }

    public static void main(String[] args) {
        HuntTheWumpus game = new HuntTheWumpus();
        // Keep iterating through the game while the game is in play
        while (game.state != GameState.STOP) {
            game.iterate();
        }
        // Remove the display once the game is ended
        game.display.dispose();
    }

}
