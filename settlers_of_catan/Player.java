/**
 * File: Player.java
 *
 * Author: Brian Westerman
 *
 * Maintains a Player object that keeps track of the contents of the player's hand, an ID number (for turn order),
 * the player's victory points, and their development cards
 */

import java.awt.Graphics;
import java.lang.reflect.Array;
import java.util.ArrayList;
//import java.util.HashMap;
import java.util.Random;
import java.util.Scanner;

public class Player extends Cell {
    /**
     * Inherited fields:
     * double x
     * double y
     */

    // The player's ID number (for turn order)
    private int id;
    // The number of victory points the player has
    private int victoryPoints;
    // An array list containing all the player's development cards
    private ArrayList<DevelopmentCard> devCards;
    // The player's hand
    private HashMap<Tile.Resource, Integer> hand;
    // Number of available roads to place
    private int roads;
    // Number of available settlements to place
    private int settlements;
    // Number of available cities to place
    private int cities;
    // Number of roads on the board
    private int roadsOnBoard;
    // Does the player have longest road
    private boolean longestRoad;
    // Number of knights this player has played
    private int knights;
    // Does the player have largest army
    private boolean largestArmy;

    public Player(int id) {
        super(0, 0);
        this.id = id;
        this.victoryPoints = 0;
        this.devCards = new ArrayList<DevelopmentCard>();
        this.hand = new HashMap<>();
        this.roads = 15;
        this.settlements = 5;
        this.cities = 4;
        this.roadsOnBoard = 0;
        this.longestRoad = false;
        this.knights = 0;
        this.largestArmy = false;
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

    // Accessor for the player's ID number
    public int getId() {
        return this.id;
    }

    // Accessor for victoryPoints
    public int getVictoryPoints() {
        return this.victoryPoints;
    }

    // Modifier for victoryPoints
    public void incrementVictoryPoints() {
        this.victoryPoints++;
    }

    // Accessor for devCards
    public ArrayList<DevelopmentCard> getDevCards() {
        return this.devCards;
    }

    // Adds a card to player's devCards
    public void addDevCard(DevelopmentCard card) {
        this.devCards.add(card);
    }

    // Accessor for hand
    public HashMap<Tile.Resource, Integer> getHand() {
        return this.hand;
    }

    // Accessor for settlements
    private int getSettlements() {
        return this.settlements;
    }

    // Accessor for cities
    private int getCities() {
        return this.cities;
    }

    // Accessor for roads
    private int getRoads() {
        return this.roads;
    }

    // Accessor for roadsOnBoard
    private int getRoadsOnBoard() {
        return this.roadsOnBoard;
    }

    // Accessor for longestRoad
    private boolean hasLongestRoad() {
        return this.longestRoad;
    }

    // Modifier for longestRoad
    private void setLongestRoad(boolean a) {
        this.longestRoad = a;
    }

    // Accessor for knights
    private int getKnights() {
        return this.knights;
    }

    // Accessor for largestArmy
    private boolean hasLargestArmy() {
        return this.largestArmy;
    }

    // Modifier for largestArmy
    private void setLargestArmy(boolean a) {
        this.largestArmy = a;
    }

    // Adds a resource card of type Tile.Resource to the player's hand
    public void addResource(Tile.Resource resource) {
        if (this.hand.get(resource) == null) {
            this.hand.put(resource, 1);
        } else {
            this.hand.put(resource, (int) this.hand.get(resource) + 1);
        }
    }

    // Buys a road and places it between two vertices on the board
    public void buyRoad(Game game) {
        Scanner input = new Scanner(System.in);
        // If the player has at least one wood and brick
        if ((int) this.hand.get(Tile.Resource.WOOD) >= 1
                && (int) this.hand.get(Tile.Resource.BRICK) >= 1) {
            // Remove those cards from the player's hand
            this.hand.put(Tile.Resource.WOOD, (int) this.hand.get(Tile.Resource.WOOD) - 1);
            this.hand.put(Tile.Resource.BRICK, (int) this.hand.get(Tile.Resource.BRICK) - 1);
            // Decrement the number of available roads and increment the number of roads on the board
            this.roads--;
            this.roadsOnBoard++;
            // Get user input and place the road
            System.out.println("You have purchased a road. Please specify where you would like to place it.\n" +
                    "Vertex 1:");
            int vertex1 = Integer.parseInt(input.next());
            System.out.println("Vertex 2:");
            int vertex2 = Integer.parseInt(input.next());
            //game.getBoard().setRoad(vertex1, vertex2);
        }
    }

    // Buys a settlement and places it on an open vertex on the board
    public void buySettlement(Game game) {
        Scanner input = new Scanner(System.in);
        // If the player has at least one wood, brick, sheep, and wheat
        if ((int) this.hand.get(Tile.Resource.WOOD) >= 1
                && (int) this.hand.get(Tile.Resource.BRICK) >= 1
                && (int) this.hand.get(Tile.Resource.SHEEP) >= 1
                && (int) this.hand.get(Tile.Resource.WHEAT) >= 1) {
            // Remove those cards from the player's hand
            this.hand.put(Tile.Resource.WOOD, (int) this.hand.get(Tile.Resource.WOOD) - 1);
            this.hand.put(Tile.Resource.BRICK, (int) this.hand.get(Tile.Resource.BRICK) - 1);
            this.hand.put(Tile.Resource.SHEEP, (int) this.hand.get(Tile.Resource.SHEEP) - 1);
            this.hand.put(Tile.Resource.WHEAT, (int) this.hand.get(Tile.Resource.WHEAT) - 1);
            // Decrement the number of available settlements
            this.settlements--;
            // Get user input and place the settlement, setting its player field to this player
            System.out.println("You have purchased a settlement. Please specify where you would like to place it.");
            int vertex = Integer.parseInt(input.next());
            //game.getBoard().setSettlement(vertex);
            //vertex.setPlayer(this);
            // Gain one victory point for placing a settlement
            this.victoryPoints++;
        }
    }

    // Buys a city and replaces a settlement owned by this player with a city
    public void buyCity(Game game) {
        Scanner input = new Scanner(System.in);
        // If the player has at least two wheat and three ore
        if ((int) this.hand.get(Tile.Resource.WHEAT) >= 2
                && (int) this.hand.get(Tile.Resource.ORE) >= 3) {
            // Remove those cards from the player's hand
            this.hand.put(Tile.Resource.WHEAT, (int) this.hand.get(Tile.Resource.WHEAT) - 2);
            this.hand.put(Tile.Resource.ORE, (int) this.hand.get(Tile.Resource.ORE) - 3);
            // Decrement the number of available cities, get a settlement back, and replace a settlement owned by this
            // player with a city
            this.cities--;
            this.settlements++;
            // Get user input and place the city, setting its player field to this player
            System.out.println("You have purchased a settlement. Please specify where you would like to place it.");
            int vertex = Integer.parseInt(input.next());
            //game.getBoard().setCity(vertex);
            //vertex.setPlayer(this);
            // Gain one victory point for replacing a settlement with a city
            this.victoryPoints++;
        }
    }

    // Buys a development card
    public void buyDevCard(Game game) {
        // If the player has at least one sheep, wheat, and ore
        if ((int) this.hand.get(Tile.Resource.SHEEP) >= 1
                && (int) this.hand.get(Tile.Resource.WHEAT) >= 1
                && (int) this.hand.get(Tile.Resource.ORE) >= 1) {
            // Remove a development card from the top of the deck and give it to the player
            this.devCards.add(game.getDevelopmentCards().remove(0));
        } else {
            System.out.println("Error: not enough resources to buy a development card.");
        }
    }

    // Flips a development card
    public DevelopmentCard flipDevCard(String s) {
        for (DevelopmentCard card : this.devCards) {
            if (s.equals(card.toString())) {
                card.setPlayed(false);
                return card; // return ends the method, we don't need to check if this condition also applies to other cards in this.devCards
            }
        }
        System.out.println("Error: player doesn't have the specified card.");
        return null;
    }

    // Executes the action of a development card
    public void playDevCard(DevelopmentCard card, Game game) {
        // If a "Knight" card is played
        if (card.getType() == DevelopmentCard.DevCard.KNIGHT) {
            // Player moves the robber to a new location and gets a card from a player who has settled around that tile
            this.knight(game);
        // If a "Victory point" card is played
        } else if (card.getType() == DevelopmentCard.DevCard.VICTORYPOINT) {
            // Increment this player's victory points by one
            this.incrementVictoryPoints();
        // If a "Year of plenty" card is played
        } else if (card.getType() == DevelopmentCard.DevCard.YEAROFPLENTY) {
            // Player picks any two resources and adds them to their hand, by running the yearOfPlenty method
            this.yearOfPlenty(game);
        // If a "Road building" card is played
        } else if (card.getType() == DevelopmentCard.DevCard.ROADBUILDING) {
            // Player places two of their roads on the board without needing to purchase them
            this.roadBuilding(game);
        // If a "Monopoly" card is played
        } else if (card.getType() == DevelopmentCard.DevCard.MONOPOLY) {
            // Player asks for a certain type of resource, all other players must give them all their resources of that type
            this.monopoly(game);
        // Catch errors with an exception
        } else {
            System.out.println("Error: null argument or improper input. Try again.");
            // More user interaction?
        }
    }

    // Executes the "Knight" development card -
    // Player moves the robber to a new location and gets a card from a player who has settled around that tile
    public void knight(Game game) {
        Scanner input = new Scanner(System.in);
        // Increment number of knights this player owns
        this.knights++;
        // Set the robber to a new location and get a random card from a player who owns a settlement or city
        // adjacent to that tile
        // Get user input for which tile to place the robber on
        System.out.println("You have played a 'Robber' card. You can move the robber to a new tile and pick a random" +
                " card from one of the players settled around that tile. Which tile do you want to put the robber on?" +
                " [1 ... 19]");
        int tile = Integer.parseInt(input.next());
        this.setRobber(game, tile);
    }

    // Executes the "Year of plenty" development card -
    // Player picks any two resources and adds them to their hand
    public void yearOfPlenty(Game game) {
        Scanner input = new Scanner(System.in);
        // Get user input for which two resources the player would like to add to their hand
        System.out.println("You have played a 'Year of plenty' card. You can choose two new resources to add to your " +
                "hand. Which resources would you like?\nFirst resource:");
        String input1 = input.next();
        switch (input1) {
            case "Wood":
                // Add a wood to the player's hand
                if (this.hand.get(Tile.Resource.WOOD) == null) {
                    this.hand.put(Tile.Resource.WOOD, 1);
                } else {
                    this.hand.put(Tile.Resource.WOOD, (int) this.hand.get(Tile.Resource.WOOD) + 1);
                }
                break;
            case "Brick":
                // Add a brick to the player's hand
                if (this.hand.get(Tile.Resource.BRICK) == null) {
                    this.hand.put(Tile.Resource.BRICK, 1);
                } else {
                    this.hand.put(Tile.Resource.BRICK, (int) this.hand.get(Tile.Resource.BRICK) + 1);
                }
                break;
            case "Sheep":
                // Add a sheep to the player's hand
                if (this.hand.get(Tile.Resource.SHEEP) == null) {
                    this.hand.put(Tile.Resource.SHEEP, 1);
                } else {
                    this.hand.put(Tile.Resource.SHEEP, (int) this.hand.get(Tile.Resource.SHEEP) + 1);
                }
                break;
            case "Wheat":
                // Add a wheat to the player's hand
                if (this.hand.get(Tile.Resource.WHEAT) == null) {
                    this.hand.put(Tile.Resource.WHEAT, 1);
                } else {
                    this.hand.put(Tile.Resource.WHEAT, (int) this.hand.get(Tile.Resource.WHEAT) + 1);
                }
                break;
            case "Ore":
                // Add an ore to the player's hand
                if (this.hand.get(Tile.Resource.ORE) == null) {
                    this.hand.put(Tile.Resource.ORE, 1);
                } else {
                    this.hand.put(Tile.Resource.ORE, (int) this.hand.get(Tile.Resource.ORE) + 1);
                }
                break;
            // Catch errors with an exception
            default:
                System.out.println("Error: improper input. Try again, checking spelling and capitalization.");
                // More user interaction?
        }
        System.out.println("Second resource:");
        String input2 = input.next();
        // I wish there were a better way to make this code more concise. Alas, either way is just as messy.
        switch (input2) {
            case "Wood":
                // Add a wood to the player's hand
                if (this.hand.get(Tile.Resource.WOOD) == null) {
                    this.hand.put(Tile.Resource.WOOD, 1);
                } else {
                    this.hand.put(Tile.Resource.WOOD, (int) this.hand.get(Tile.Resource.WOOD) + 1);
                }
            case "Brick":
                // Add a brick to the player's hand
                if (this.hand.get(Tile.Resource.BRICK) == null) {
                    this.hand.put(Tile.Resource.BRICK, 1);
                } else {
                    this.hand.put(Tile.Resource.BRICK, (int) this.hand.get(Tile.Resource.BRICK) + 1);
                }
            case "Sheep":
                // Add a sheep to the player's hand
                if (this.hand.get(Tile.Resource.SHEEP) == null) {
                    this.hand.put(Tile.Resource.SHEEP, 1);
                } else {
                    this.hand.put(Tile.Resource.SHEEP, (int) this.hand.get(Tile.Resource.SHEEP) + 1);
                }
            case "Wheat":
                // Add a wheat to the player's hand
                if (this.hand.get(Tile.Resource.WHEAT) == null) {
                    this.hand.put(Tile.Resource.WHEAT, 1);
                } else {
                    this.hand.put(Tile.Resource.WHEAT, (int) this.hand.get(Tile.Resource.WHEAT) + 1);
                }
            case "Ore":
                // Add an ore to the player's hand
                if (this.hand.get(Tile.Resource.ORE) == null) {
                    this.hand.put(Tile.Resource.ORE, 1);
                } else {
                    this.hand.put(Tile.Resource.ORE, (int) this.hand.get(Tile.Resource.ORE) + 1);
                }
            // Catch errors with an exception
            default:
                System.out.println("Error: improper input. Try again, checking spelling and capitalization.");
                // More user interaction?
        }
    }

    // Executes the "Road building" development card -
    // Player places two of their roads on the board without needing to purchase them
    public void roadBuilding(Game game) {
        Scanner input = new Scanner(System.in);
        // Make sure they have enough roads to place two
        if (this.roads >= 2) {
            this.roads -= 2;
            this.roadsOnBoard += 2;
        } else {
            System.out.println("Sorry, you don't have enough roads to place. Poor luck.");
        }
        // Get user input and place the roads
        System.out.println("You have played a 'Road building' card. You can place two of your roads on the board for " +
                "free. Please specify where you would like to place the roads.\nVertex 1 of first road:");
        int vertex1 = Integer.parseInt(input.next());
        System.out.println("Vertex 2 of first road:");
        int vertex2 = Integer.parseInt(input.next());
        System.out.println("Vertex 1 of second road:");
        int vertex3 = Integer.parseInt(input.next());
        System.out.println("Vertex 2 of second road:");
        int vertex4 = Integer.parseInt(input.next());
        //game.getBoard().setRoad(vertex1, vertex2);
        //game.getBoard().setRoad(vertex3, vertex4);
    }


    // Executes the "Monopoly" development card -
    // Player asks for a certain type of resource, all other players must give them all their resources of that type
    public void monopoly(Game game) {
        Scanner input = new Scanner(System.in);
        // Get a list of the other opponents
        ArrayList<Player> opponents = new ArrayList<>();
        for (Player player : game.getPlayers()) {
            if (! this.equals(player)) {
                opponents.add(player);
            }
        }
        // Get all resources of the specified type
        System.out.println("You have played a 'Monopoly' card. You can take all resources of a specific type from " +
                "each of your opponents. Which resource do you want to choose? " +
                "[Wood, Brick, Sheep, Wheat, Ore]");
        String type = input.next();
        if (type.equals("Wood")) {
            // Take away all the wood resources from this player's opponents and count them up
            int wood = 0;
            for (Player player : opponents) {
                if (player.getHand().get(Tile.Resource.WOOD) != null) {
                    wood += (int) player.getHand().get(Tile.Resource.WOOD);
                }
                player.getHand().remove(Tile.Resource.WOOD);
            }
            // Give all those resources to this player
            if (this.hand.get(Tile.Resource.WOOD) == null) {
                this.hand.put(Tile.Resource.WOOD, wood);
            } else {
                this.hand.put(Tile.Resource.WOOD, (int) this.hand.get(Tile.Resource.WOOD) + wood);
            }
        } else if (type.equals("Brick")) {
            // Take away all the brick resources from this player's opponents and count them up
            int brick = 0;
            for (Player player : opponents) {
                if (player.getHand().get(Tile.Resource.BRICK) != null) {
                    brick += (int) player.getHand().get(Tile.Resource.BRICK);
                }
                player.getHand().remove(Tile.Resource.BRICK);
            }
            // Give all those resources to this player
            if (this.hand.get(Tile.Resource.BRICK) == null) {
                this.hand.put(Tile.Resource.BRICK, brick);
            } else {
                this.hand.put(Tile.Resource.BRICK, (int) this.hand.get(Tile.Resource.BRICK) + brick);
            }
        } else if (type.equals("Sheep")) {
            // Take away all the sheep resources from this player's opponents and count them up
            int sheep = 0;
            for (Player player : opponents) {
                if (player.getHand().get(Tile.Resource.SHEEP) != null) {
                    sheep += (int) player.getHand().get(Tile.Resource.SHEEP);
                }
                player.getHand().remove(Tile.Resource.SHEEP);
            }
            // Give all those resources to this player
            if (this.hand.get(Tile.Resource.SHEEP) == null) {
                this.hand.put(Tile.Resource.SHEEP, sheep);
            } else {
                this.hand.put(Tile.Resource.SHEEP, (int) this.hand.get(Tile.Resource.SHEEP) + sheep);
            }
        } else if (type.equals("Wheat")) {
            // Take away all the wheat resources from this player's opponents and count them up
            int wheat = 0;
            for (Player player : opponents) {
                if (player.getHand().get(Tile.Resource.WHEAT) != null) {
                    wheat += (int) player.getHand().get(Tile.Resource.WHEAT);
                }
                player.getHand().remove(Tile.Resource.WHEAT);
            }
            // Give all those resources to this player
            if (this.hand.get(Tile.Resource.WHEAT) == null) {
                this.hand.put(Tile.Resource.WHEAT, wheat);
            } else {
                this.hand.put(Tile.Resource.WHEAT, (int) this.hand.get(Tile.Resource.WHEAT) + wheat);
            }
        } else if (type.equals("Ore")) {
            // Take away all the ore resources from this player's opponents and count them up
            int ore = 0;
            for (Player player : opponents) {
                if (player.getHand().get(Tile.Resource.ORE) != null) {
                    ore += (int) player.getHand().get(Tile.Resource.ORE);
                }
                player.getHand().remove(Tile.Resource.ORE);
            }
            // Give all those resources to this player
            if (this.hand.get(Tile.Resource.ORE) == null) {
                this.hand.put(Tile.Resource.ORE, ore);
            } else {
                this.hand.put(Tile.Resource.ORE, (int) this.hand.get(Tile.Resource.ORE) + ore);
            }
            // Catch errors with an exception
        } else {
            System.out.println("Error: improper input. Try again.");
            // More user interaction?
        }
    }

    // Sets the robber to a new tile
    public void setRobber(Game game, int newTile) throws NullPointerException {
        Scanner input = new Scanner(System.in);
        Tile oldRobber = null;
        ArrayList<Tile> tiles = game.getBoard().getTiles();
        // Find the tile that currently has the robber on it
        for (Tile tile : tiles) {
            if (tile.hasRobber()) {
                oldRobber = tile;
            }
        }
        // Set that tile to not have the robber on it
        if (oldRobber != null) {
            oldRobber.setRobber(false);
        } else {
            throw new NullPointerException("Error: there was no robber on the board.");
        }
        // Set a new tile to hold the robber
        System.out.println("Which tile would you like to place the robber on? Please do not put it on the tile it was" +
                "just at.");
        int next = Integer.parseInt(input.next());
        Tile newRobber = null;
        for (Tile tile : tiles) {
            if (tile != oldRobber && tiles.get(newTile - 1).equals(tile)) {
                newRobber = tile;
                newRobber.setRobber(true);
            }
        }
        // Catch errors
        if (newRobber == null) {
            System.out.println("Error: no new tile chosen to place robber on. Please choose again.");
        }
    }

    // Rolls the dice
    public int rollDice() {
        Random r = new Random();
        return (r.nextInt(6) + 1) + (r.nextInt(6) + 1);
    }

    // Updates the state of this player each turn
    public void updateState(Landscape scape) {
        // Don't need to do anything here; the game is updated in the method Game.advance()
    }

    // Inherited from Cell
    public void draw(Graphics g, int x, int y, int scale) {
        // Don't need to do anything here; Player doesn't get drawn on the landscape display
    }

    public static void main(String[] args) {
        Game game = new Game(4);
        Player player = new Player(1);
        Vertx vertex = new Vertx(0, 0);
        if (vertex.isAvailableForSettling(game.getBoard())) {
            player.buySettlement(game);
        }
        player.rollDice();
        player.setRobber(game, 4);
        player.flipDevCard("Knight");
        player.getId();
        player.getVictoryPoints();
        player.incrementVictoryPoints();
        player.getDevCards();
        player.addDevCard(new DevelopmentCard(3));
        player.getSettlements();
        player.getCities();
        player.getRoads();
        player.getRoadsOnBoard();
        player.hasLongestRoad();
        player.setLongestRoad(true);
        player.hasLongestRoad();
        player.hasLargestArmy();
        player.setLargestArmy(true);
        player.hasLargestArmy();
        player.getKnights();
        player.buyDevCard(game);
        player.buyRoad(game);
        player.buySettlement(game);
        player.buyCity(game);
    }

}
