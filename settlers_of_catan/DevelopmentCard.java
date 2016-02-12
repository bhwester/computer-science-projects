/**
 * File: DevelopmentCard.java
 *
 * Author: Brian Westerman
 *
 * Maintains data for development cards. Players "purchase" development cards and store them in an array list called
 * Player.devCards. The Game keeps track of all of the development cards in the game in a shuffled array list.
 * 14 knight cards
 * 5 victory point cards
 * 2 year of plenty cards
 * 2 road building cards
 * 2 monopoly cards
 */

public class DevelopmentCard {
    // The type of development card
    public enum DevCard { KNIGHT, VICTORYPOINT, YEAROFPLENTY, ROADBUILDING, MONOPOLY }
    private DevCard type;
    // The index of the development card
    private int index;
    // Whether the card has been played
    private boolean played;

    // Explicit constructor
    public DevelopmentCard(DevCard type) throws IllegalArgumentException {
        this.type = type;
        this.played = false;
        if (type == DevCard.KNIGHT) {
            this.index = 1;
        } else if (type == DevCard.VICTORYPOINT) {
            this.index = 2;
        } else if (type == DevCard.YEAROFPLENTY) {
            this.index = 3;
        } else if (type == DevCard.ROADBUILDING) {
            this.index = 4;
        } else if (type == DevCard.MONOPOLY) {
            this.index = 5;
        } else {
            throw new IllegalArgumentException("Error: improper development card type");
        }
    }

    // Randomized constructor
    public DevelopmentCard(int card) throws IllegalArgumentException {
        this.index = card;
        this.played = false;
        if (card == 1) {
            this.type = DevCard.KNIGHT;
        } else if (card == 2) {
            this.type = DevCard.VICTORYPOINT;
        } else if (card == 3) {
            this.type = DevCard.YEAROFPLENTY;
        } else if (card == 4) {
            this.type = DevCard.ROADBUILDING;
        } else if (card == 5) {
            this.type = DevCard.MONOPOLY;
        } else {
            throw new IllegalArgumentException("Error: improper index for assigning card type");
        }
    }

    // Accessor for type
    public DevCard getType() {
        return this.type;
    }

    // Accessor for index
    public int getIndex() {
        return this.index;
    }

    // Accessor for played
    public boolean hasBeenPlayed() {
        return this.played;
    }

    // Modifier for played
    public void setPlayed(boolean played) {
        this.played = played;
    }

    // Turns a development card into a string representation
    public String toString() {
        if (this.type == DevCard.KNIGHT) {
            return "Knight";
        } else if (this.type == DevCard.VICTORYPOINT) {
            return "Victory point";
        } else if (this.type == DevCard.YEAROFPLENTY) {
            return "Year of plenty";
        } else if (this.type == DevCard.ROADBUILDING) {
            return "Road building";
        } else if (this.type == DevCard.MONOPOLY) {
            return "Monopoly";
        } else {
            System.out.println("Error: improper input. Check spelling and capitalization.");
            return null;
        }
    }

    public static void main(String[] args) {
        DevelopmentCard devCard = new DevelopmentCard(3);
        devCard.getIndex();
        devCard.getType();
        devCard.setPlayed(true);
        devCard.hasBeenPlayed();
        System.out.println(devCard.toString());
    }

}
