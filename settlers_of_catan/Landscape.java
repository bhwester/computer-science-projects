// Bruce Maxwell
// CS 231 Fall 2012
// Project 7
// *Utilizes Bruce Maxwell's Landscape class from the Elevator Simulation project.

import java.util.*;

public class Landscape {
    private double width;
    private double height;
    private LinkedList<Cell> agents;

    // Constructor
    public Landscape(double rows, double cols) {
        this.agents = new LinkedList<Cell>();
        this.height = rows;
        this.width = cols;
    }

    // get rid of all of the agents
    public void reset() {
        agents.clear();
    }
 
    // modify to round
    public int getRows() {
        return (int)(height + 0.5);
    }

    // add method
    public double getHeight() {
        return height;
    }

    // modify to round
    public int getCols() {
        return (int)(width + 0.5);
    }

    // add method
    public double getWidth() {
        return width;
    }

    public void addAgent(Cell a) {
        agents.addFirst(a);
    }

    public void removeAgent(Cell a) {
        agents.remove(a);
    }

    public ArrayList<Cell> getAgents() {
        return agents.toArrayList();
    }

    public String toString() {
        ArrayList<String> s = new ArrayList<String>();

        for(int i=0;i<height;i++) {
            for(int j=0;j<width;j++) {
                s.add(" ");
            }
            s.add("\n");
        }

        for( Cell item: agents ) {
            int r = item.getRow();
            int c = item.getCol();

            if(r >= 0 && r < height && c >= 0 && c < width ) {
                int index = r * (this.getCols() + 1) + c;
                s.set( index, item.toString() );
            }
        }

        String sout = "";
        for( String a: s ) {
            sout += a;
        }

        return sout;
    }

    public void advance() {
        // put the agents in random oder
        ArrayList<Cell> items = agents.toShuffledList();

        // update the state of each agent
        for (Cell item: items) {
            item.updateState( this );
        }
    }

    public static void main(String argv[]) throws InterruptedException {
        int rows = 240;
        int cols = 240;
        int N = 300;
        Landscape landscape = new Landscape(rows, cols);
        Random gen = new Random();

        // Set up a game with 4 players
        Game game = new Game(4);
        // Add all the cells (players, tiles, and vertices) to the landscape
        for (Player player : game.getPlayers()) {
            landscape.addAgent(player);
        }
        for (Tile tile : game.getBoard().getTiles()) {
            landscape.addAgent(tile);
        }
        for (Vertx vertx : game.getBoard().getVertices()) {
            landscape.addAgent(vertx);
        }

        // Create a landscape display to see the game graphically run on
        LandscapeDisplay display = new LandscapeDisplay(landscape, 2);
        display.update();
        Thread.sleep(100);

    }

}
