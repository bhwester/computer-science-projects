/**
 * File: Game.java
 *
 * Author: Brian Westerman
 *
 * Runs a game of Settlers of Catan. Players seek to gain 10 victory points. They gain victory points by building
 * settlements and cities on vertices of the board, as well as by buying development cards that may elicit victory
 * points. Players also build roads to connect vertices. The board is comprised of 19 hexagonal tiles, each of which
 * can be one of five resource types. Vertices are located at the corners of tiles where they meet with other tiles.
 * Players collect resources into their hands by rolling the dice and collecting resources of the type matching a tile
 * that displays the number rolled, provided that they have a settlement or city bordering that tile.
 *
 * Game.java sets up the game; Landscape.java runs the game and draws it to a landscape display.
 */

import java.lang.reflect.Array;
import java.util.*;

public class Game {
    public static final int SCALE = 240;
    // Number of total turns taken this game (divide by the number of players to get the number of rounds in the game)
    private int totalTurns;
    // A list of all the development cards in the game
    private ArrayList<DevelopmentCard> developmentCards;
    // The Board holding ****** all of the vertices and tiles
    private Board board;
    // A list of the players
    private ArrayList<Player> players;

    public Game(int numPlayers) {
        this.totalTurns = 0;
        this.developmentCards = new ArrayList<>();
        this.board = new Board();
        this.players = new ArrayList<Player>();
        for (int i = 0; i < numPlayers; i++) {
            this.players.add(new Player(i+1));
        }
        this.setUp();
    }

    // Sets up the game by initializing the development cards and the tiles
    public void setUp() {
        this.initializeDevCards();
        this.initializeTiles(this.board);
        this.initializeVertices(this.board);
    }

    // Creates a shuffled deck of development cards
    public void initializeDevCards() {
        // Add knight cards
        for (int i = 0; i < 14; i++) {
            this.developmentCards.add(new DevelopmentCard(1));
        }
        // Add victory point cards
        for (int i = 0; i < 5; i++) {
            this.developmentCards.add(new DevelopmentCard(2));
        }
        // Add year of plenty cards
        for (int i = 0; i < 2; i++) {
            this.developmentCards.add(new DevelopmentCard(3));
        }
        // Add road building cards
        for (int i = 0; i < 2; i++) {
            this.developmentCards.add(new DevelopmentCard(4));
        }
        // Add monopoly cards
        for (int i = 0; i < 2; i++) {
            this.developmentCards.add(new DevelopmentCard(5));
        }
        // Shuffle cards
        Collections.shuffle(this.developmentCards);
    }

    // Adds the tiles to the game board, randomly selecting from the list of roll numbers
    // Warning: there appears to be no better way to automate the precise positioning of the tiles,
    // so unfortunately it all had to be done out by hand.
    public void initializeTiles(Board board) {
        Random r = new Random();
        // Create a list containing all the possible roll numbers: 18 possible numbers
        ArrayList<Integer> rolls = new ArrayList<>();
        int[] rollNums = { 2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9 ,9, 10, 10, 11, 11, 12 };
        for (int i : rollNums) {
            rolls.add(i);
        }
        // Create a list containing all the possible resources: 4 wood, 3 brick, 4 sheep, 4 wheat, 3 ore
        ArrayList<Tile.Resource> resources = new ArrayList<>();
        Tile.Resource[] types = { Tile.Resource.WOOD, Tile.Resource.WOOD, Tile.Resource.WOOD, Tile.Resource.WOOD,
                Tile.Resource.BRICK, Tile.Resource.BRICK, Tile.Resource.BRICK,
                Tile.Resource.SHEEP, Tile.Resource.SHEEP, Tile.Resource.SHEEP, Tile.Resource.SHEEP,
                Tile.Resource.WHEAT, Tile.Resource.WHEAT, Tile.Resource.WHEAT, Tile.Resource.WHEAT,
                Tile.Resource.ORE, Tile.Resource.ORE, Tile.Resource.ORE };
        for (Tile.Resource i : types) {
            resources.add(i);
        }
        // Initialize all 19 tiles with a random roll number from the list and a random resource from the list
        // Order tile1...tile19 is read left to right, row by row, as shown in the board shape below
        //
        //       . . .
        //      . . . .
        //     . . . . .
        //      . . . .
        //       . . .
        //
        // I wish there were a more concise way to do this...
        Tile tile1 = new Tile(((SCALE/2)-(SCALE/12)*(Math.sqrt(3))),
                ((SCALE/2)-(SCALE/4)),
                1, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile2 = new Tile((SCALE/2),
                ((SCALE/2)-(SCALE/4)),
                2, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile3 = new Tile(((SCALE/2)+(SCALE/12)*(Math.sqrt(3))),
                ((SCALE/2)-(SCALE/4)),
                3, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile4 = new Tile(((SCALE/2)-(SCALE/12)*(3*Math.sqrt(3)/2)),
                ((SCALE/2)-(SCALE/8)),
                4, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile5 = new Tile(((SCALE/2)-(SCALE/12)*(Math.sqrt(3)/2)),
                ((SCALE/2)-(SCALE/8)),
                5, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile6 = new Tile(((SCALE/2)+(SCALE/12)*(Math.sqrt(3)/2)),
                ((SCALE/2)-(SCALE/8)),
                6, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile7 = new Tile(((SCALE/2)+(SCALE/12)*(3*Math.sqrt(3)/2)),
                ((SCALE/2)-(SCALE/8)),
                7, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile8 = new Tile(((SCALE/2)-(SCALE/12)*(2*Math.sqrt(3))),
                (SCALE/2),
                8, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile9 = new Tile(((SCALE/2)-(SCALE/12)*(Math.sqrt(3))),
                (SCALE/2),
                9, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile10 = new Tile((SCALE/2),
                (SCALE/2),
                10, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile11 = new Tile(((SCALE/2)+(SCALE/12)*(Math.sqrt(3))),
                (SCALE/2),
                11, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile12 = new Tile(((SCALE/2)+(SCALE/12)*(2*Math.sqrt(3))),
                (SCALE/2),
                12, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile13 = new Tile(((SCALE/2)-(SCALE/12)*(3*Math.sqrt(3)/2)),
                ((SCALE/2)+(SCALE/8)),
                13, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile14 = new Tile(((SCALE/2)-(SCALE/12)*(Math.sqrt(3)/2)),
                ((SCALE/2)+(SCALE/8)),
                14, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile15 = new Tile(((SCALE/2)+(SCALE/12)*(Math.sqrt(3)/2)),
                ((SCALE/2)+(SCALE/8)),
                15, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile16 = new Tile(((SCALE/2)+(SCALE/12)*(3*Math.sqrt(3)/2)),
                ((SCALE/2)+(SCALE/8)),
                16, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile17 = new Tile(((SCALE/2)-(SCALE/12)*(Math.sqrt(3))),
                ((SCALE/2)+(SCALE/4)),
                17, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile18 = new Tile((SCALE/2),
                ((SCALE/2)+(SCALE/4)),
                18, rolls.remove(r.nextInt(rolls.size())), resources.remove(r.nextInt(resources.size())));
        Tile tile19 = new Tile(((SCALE/2)+(SCALE/12)*(Math.sqrt(3))),
                ((SCALE/2)+(SCALE/4)),
                19, 0, Tile.Resource.DESERT);
        // Add tiles to this.tiles
        board.getTiles().add(tile1);
        board.getTiles().add(tile2);
        board.getTiles().add(tile3);
        board.getTiles().add(tile4);
        board.getTiles().add(tile5);
        board.getTiles().add(tile6);
        board.getTiles().add(tile7);
        board.getTiles().add(tile8);
        board.getTiles().add(tile9);
        board.getTiles().add(tile10);
        board.getTiles().add(tile11);
        board.getTiles().add(tile12);
        board.getTiles().add(tile13);
        board.getTiles().add(tile14);
        board.getTiles().add(tile15);
        board.getTiles().add(tile16);
        board.getTiles().add(tile17);
        board.getTiles().add(tile18);
        board.getTiles().add(tile19);
    }

    // Initializes the vertices (type Vertx) stored in Board.boardGraph (a Graph data structure) that comprise the
    // game board grid
    // Warning: there appears to be no better way to automate the precise positioning of the vertices,
    // so unfortunately it all had to be done out by hand.
    public void initializeVertices(Board board) {
        // First, get all the tiles to make positioning easier
        ArrayList<Tile> tiles = this.getBoard().getTiles();
        Tile tile1 = tiles.get(0);
        Tile tile2 = tiles.get(1);
        Tile tile3 = tiles.get(2);
        Tile tile4 = tiles.get(3);
        Tile tile5 = tiles.get(4);
        Tile tile6 = tiles.get(5);
        Tile tile7 = tiles.get(6);
        Tile tile8 = tiles.get(7);
        Tile tile9 = tiles.get(8);
        Tile tile10 = tiles.get(9);
        Tile tile11 = tiles.get(10);
        Tile tile12 = tiles.get(11);
        Tile tile13 = tiles.get(12);
        Tile tile14 = tiles.get(13);
        Tile tile15 = tiles.get(14);
        Tile tile16 = tiles.get(15);
        Tile tile17 = tiles.get(16);
        Tile tile18 = tiles.get(17);
        Tile tile19 = tiles.get(18);
        // Make some constants that will facilitate positioning of the vertices
        double xOffset = (SCALE/12)*(Math.sqrt(3)/2);
        double yMidOffset = (SCALE/24);
        double yFullOffset = (SCALE/12);
        // Then get the graph
        Graph<Vertx> graph = this.getBoard().getBoardGraph();
        // Add all vertices to graph
        // First, the outer ring:
        Vertx v1 = new Vertx(tile1.getX() - xOffset, tile1.getY() - yMidOffset);
        Vertx v2 = new Vertx(tile1.getX(), tile1.getY() - yFullOffset);
        Vertx v3 = new Vertx(tile2.getX() - xOffset, tile2.getY() - yMidOffset);
        Vertx v4 = new Vertx(tile2.getX(), tile2.getY() - yFullOffset);
        Vertx v5 = new Vertx(tile3.getX() - xOffset, tile3.getY() - yMidOffset);
        Vertx v6 = new Vertx(tile3.getX(), tile3.getY() - yFullOffset);
        Vertx v7 = new Vertx(tile1.getX() + xOffset, tile3.getY() - yMidOffset);
        Vertx v8 = new Vertx(tile1.getX() + xOffset, tile3.getY() + yMidOffset);
        Vertx v9 = new Vertx(tile7.getX(), tile7.getY() - yMidOffset);
        Vertx v10 = new Vertx(tile7.getX(), tile7.getY() + yMidOffset);
        Vertx v11 = new Vertx(tile12.getX(), tile12.getY() - yMidOffset);
        Vertx v12 = new Vertx(tile12.getX(), tile12.getY() + yMidOffset);
        Vertx v13 = new Vertx(tile16.getX(), tile16.getY() - yMidOffset);
        Vertx v14 = new Vertx(tile16.getX(), tile16.getY() + yMidOffset);
        Vertx v15 = new Vertx(tile19.getX(), tile19.getY() - yMidOffset);
        Vertx v16 = new Vertx(tile19.getX(), tile19.getY() + yMidOffset);
        Vertx v17 = new Vertx(tile19.getX(), tile19.getY() + yFullOffset);
        Vertx v18 = new Vertx(tile18.getX() + xOffset, tile18.getY() + yMidOffset);
        Vertx v19 = new Vertx(tile18.getX(), tile18.getY() + yFullOffset);
        Vertx v20 = new Vertx(tile17.getX() + xOffset, tile17.getY() + yMidOffset);
        Vertx v21 = new Vertx(tile17.getX(), tile17.getY() + yFullOffset);
        Vertx v22 = new Vertx(tile17.getX() - xOffset, tile17.getY() + yMidOffset);
        Vertx v23 = new Vertx(tile17.getX() - xOffset, tile17.getY() - yMidOffset);
        Vertx v24 = new Vertx(tile13.getX() - xOffset, tile13.getY() + yMidOffset);
        Vertx v25 = new Vertx(tile13.getX() - xOffset, tile13.getY() - yMidOffset);
        Vertx v26 = new Vertx(tile8.getX() - xOffset, tile8.getY() + yMidOffset);
        Vertx v27 = new Vertx(tile8.getX() - xOffset, tile8.getY() - yMidOffset);
        Vertx v28 = new Vertx(tile4.getX() - xOffset, tile4.getY() + yMidOffset);
        Vertx v29 = new Vertx(tile4.getX() - xOffset, tile4.getY() - yMidOffset);
        Vertx v30 = new Vertx(tile1.getX() - xOffset, tile1.getY() + yMidOffset);
        // Then, the middle ring:
        Vertx v31 = new Vertx(tile5.getX() - xOffset, tile5.getY() - yMidOffset);
        Vertx v32 = new Vertx(tile5.getX(), tile5.getY() - yFullOffset);
        Vertx v33 = new Vertx(tile6.getX() - xOffset, tile6.getY() - yMidOffset);
        Vertx v34 = new Vertx(tile6.getX(), tile6.getY() - yFullOffset);
        Vertx v35 = new Vertx(tile6.getX() + xOffset, tile6.getY() - yMidOffset);
        Vertx v36 = new Vertx(tile6.getX() + xOffset, tile6.getY() + yMidOffset);
        Vertx v37 = new Vertx(tile11.getX() + xOffset, tile11.getY() - yMidOffset);
        Vertx v38 = new Vertx(tile11.getX() + xOffset, tile11.getY() + yMidOffset);
        Vertx v39 = new Vertx(tile15.getX() + xOffset, tile15.getY() - yMidOffset);
        Vertx v40 = new Vertx(tile15.getX() + xOffset, tile15.getY() + yMidOffset);
        Vertx v41 = new Vertx(tile15.getX(), tile15.getY() + yFullOffset);
        Vertx v42 = new Vertx(tile15.getX() - xOffset, tile15.getY() + yMidOffset);
        Vertx v43 = new Vertx(tile14.getX(), tile14.getY() + yFullOffset);
        Vertx v44 = new Vertx(tile14.getX() - xOffset, tile14.getY() + yMidOffset);
        Vertx v45 = new Vertx(tile15.getX() - xOffset, tile15.getY() - yMidOffset);
        Vertx v46 = new Vertx(tile9.getX() - xOffset, tile9.getY() + yMidOffset);
        Vertx v47 = new Vertx(tile9.getX() - xOffset, tile9.getY() - yMidOffset);
        Vertx v48 = new Vertx(tile5.getX() - xOffset, tile5.getY() + yMidOffset);
        // Then, the inner ring:
        Vertx v49 = new Vertx(tile10.getX() - xOffset, tile10.getY() - yMidOffset);
        Vertx v50 = new Vertx(tile10.getX(), tile10.getY() - yFullOffset);
        Vertx v51 = new Vertx(tile10.getX() + xOffset, tile10.getY() - yMidOffset);
        Vertx v52 = new Vertx(tile10.getX() + xOffset, tile10.getY() + yMidOffset);
        Vertx v53 = new Vertx(tile10.getX(), tile10.getY() + yFullOffset);
        Vertx v54 = new Vertx(tile10.getX() - xOffset, tile10.getY() + yMidOffset);
        // Then add all edges to vertices in appropriate configuration
        // First, the outer ring of edges:
        v1.setEdge(v2);
        v2.setEdge(v3);
        v3.setEdge(v4);
        v4.setEdge(v5);
        v5.setEdge(v6);
        v6.setEdge(v7);
        v7.setEdge(v8);
        v8.setEdge(v9);
        v9.setEdge(v10);
        v10.setEdge(v11);
        v11.setEdge(v12);
        v12.setEdge(v13);
        v13.setEdge(v14);
        v14.setEdge(v15);
        v15.setEdge(v16);
        v16.setEdge(v17);
        v17.setEdge(v18);
        v18.setEdge(v19);
        v19.setEdge(v20);
        v20.setEdge(v21);
        v21.setEdge(v22);
        v22.setEdge(v23);
        v23.setEdge(v24);
        v24.setEdge(v25);
        v25.setEdge(v26);
        v26.setEdge(v27);
        v27.setEdge(v28);
        v28.setEdge(v29);
        v29.setEdge(v30);
        v30.setEdge(v1);
        // Then, the middle ring of edges:
        v31.setEdge(v32);
        v32.setEdge(v33);
        v33.setEdge(v34);
        v34.setEdge(v35);
        v35.setEdge(v36);
        v36.setEdge(v37);
        v37.setEdge(v38);
        v38.setEdge(v39);
        v39.setEdge(v40);
        v40.setEdge(v41);
        v41.setEdge(v42);
        v42.setEdge(v43);
        v43.setEdge(v44);
        v44.setEdge(v45);
        v45.setEdge(v46);
        v46.setEdge(v47);
        v47.setEdge(v48);
        v48.setEdge(v31);
        // Then, the inner ring of edges:
        v49.setEdge(v50);
        v50.setEdge(v51);
        v51.setEdge(v52);
        v52.setEdge(v53);
        v53.setEdge(v54);
        v54.setEdge(v49);
        // Then, the outer connectors:
        v31.setEdge(v30);
        v32.setEdge(v3);
        v34.setEdge(v5);
        v35.setEdge(v8);
        v37.setEdge(v10);
        v38.setEdge(v13);
        v40.setEdge(v15);
        v41.setEdge(v18);
        v43.setEdge(v20);
        v44.setEdge(v23);
        v46.setEdge(v25);
        v47.setEdge(v28);
        // Then, the inner connectors:
        v49.setEdge(v48);
        v50.setEdge(v33);
        v51.setEdge(v36);
        v52.setEdge(v39);
        v53.setEdge(v42);
        v54.setEdge(v45);
        // I will never write that much code again in my life.
    }

    // Accessor for totalTurns
    public int getTotalTurns() {
        return totalTurns;
    }

    // Accessor for development cards
    public ArrayList<DevelopmentCard> getDevelopmentCards() {
        return this.developmentCards;
    }

    // Accessor for board
    public Board getBoard() {
        return this.board;
    }

    // Accessor for players
    public ArrayList<Player> getPlayers() {
        return this.players;
    }

    // Distributes resources to players who have settlements or cities adjacent to tiles that possess the rolled number
    public void distributeResources(int roll) {
        for (Tile tile : this.board.getTiles()) {
            if (tile.getRollNum() == roll) {
                tile.giveResources();
            }
        }
    }

    // Increments each turn taken
    public void advance() {
        this.totalTurns++;
    }

    public static void main(String[] args) {
        Game game = new Game(4);
        game.setUp();
        game.getTotalTurns();
        game.getDevelopmentCards();
        game.getBoard();
        game.getPlayers();
        game.distributeResources(5);
        game.advance();
    }

}
