#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A small docstring for Assignment 8"""


import sys
import argparse
import time
from random import randint, seed

seed(0)

class Die():
    """The Die class."""

    def roll(self):
        """Roll the die."""

        number = randint(1, 6)
        return number



class Player():
   
    def __init__(self):
        """Player constructor method."""

        self.total_score = 0
        self.running_score = 0
        self.this_roll = 0


    def show_running_score(self):
        """Show running score.

        Returns:
            running_score (int): Current running score.
        """

        return self.running_score


    def set_running_score(self, this_roll):
        """Set running score.

        Args:
            this_roll (int): Current number rolled.

        Returns:
            running_score (int): Current running score.
        """

        if this_roll != 1:
            self.running_score += this_roll
        else:
            self.running_score = 0

        return self.running_score


    def show_total_score(self):
        """Show total score.

        Returns:
            total_score (int): Current total score.
        """

        return self.total_score


    def set_total_score(self, running_score):
        """Set total score.

        Args:
            running_score (int): Current running score.

        Returns:
            total_score (int): Current total score.
        """

        self.total_score += running_score
        self.running_score = 0

        return self.total_score


    def roll_or_hold(self):
        """Roll or hold."""
    
        self.choice = raw_input("(r)oll or (h)old: ")



class ComputerPlayer(Player):

    def __init__(self):
        self.name = None
        Player.__init__(self)


    def roll_or_hold(self):
        """Function to determine roll or hold."""
        hold_25 = 25
        hold_100 = 100 - self.running_score

        if hold_25 < hold_100:
            hold_score = hold_25
        else:
            hold_score = hold_100

        if self.running_score < hold_score:
            self.choice = "r"
        elif self.running_score >= hold_score:
            self.choice = "h"



class HumanPlayer(Player):

    def __init__(self):
        self.name = None
        Player.__init__(self)



class PlayerFactory():

    def __init__(self, player):
        if player == "human":
            self.playerObj = HumanPlayer()
        if player == "computer":
            self.playerObj = ComputerPlayer()


class Game():

    def __init__(self, player1_type, player2_type, timed):
        """Game class constuctor function.

        args:
            player1_type (str): human | computer
            player2_type (str): human | computer
            timed (boolean):    Timed or not timed
        """

        self.player1_type = player1_type
        self.player2_type = player2_type
        self.timed = timed

        self.player1 = PlayerFactory(self.player1_type)
        self.player2 = PlayerFactory(self.player2_type)


        self.player_list = ['self.player1', 'self.player2']

        self.first_player_index = randint(0, len(self.player_list)-1)
        self.player_list = self.player_list[self.first_player_index:] + self.player_list[:self.first_player_index]

        self.player_turn = 0

    def play_game(self):
        """The play_gaeme function executes the game."""
        
        #print ("Player1 = ", self.player1.playerObj)
        #print ("Player2 = ", self.player2.playerObj)

        while self.player1.playerObj.total_score < 100 and self.player2.playerObj.total_score < 100:
            player = self.player_list[self.player_turn]
            while True:
                print "Now playing: {}".format(player)
                eval(player).playerObj.roll_or_hold()
                if eval(player).playerObj.choice == "r":
                    this_turn = Die()
                    this_roll = this_turn.roll()
                    print "roll is: {}".format(this_roll)

                    running_score = eval(player).playerObj.set_running_score(this_roll)
                    print "({}) Running Score is: {}".format(player, running_score)
                    total_score = eval(player).playerObj.show_total_score()
                    print "({}) Total Score is: {}".format(player, total_score)
                    if running_score == 0:
                        break

                if eval(player).playerObj.choice == "h":
                    total_score = eval(player).playerObj.set_total_score(running_score)
                    print "{} Total Score is: {}".format(player, total_score)
                    break
            
            if self.timed:
                if time.time() - 60 > TimedProxy.start_time:
                    if self.player1.playerObj.total_score > self.player2.playerObj.total_score:
                        winner = "Player1"
                    else:
                        winner = "player2"
                    print ("Time is up! The winner is {}!").format(winner)
                    break

            if total_score >= 100:
                print "The winner is {}!".format(player)
            else:
                print "\nNow switching Players...\n"
            
            if self.player_turn == 0:
                self.player_turn = 1
            else:
                self.player_turn = 0
            

class TimedProxy(Game):

        start_time = time.time()


def main():

    parser = argparse.ArgumentParser(description='Player Types')
    parser.add_argument('--player1', default="human")
    parser.add_argument('--player2', default="computer")
    parser.add_argument('--timed', default="False")
    args = parser.parse_args()
    
    if args.timed is True:
        game = TimedProxy(args.player1, args.player2, args.timed)
        game.play_game()
    else:
        game = Game(args.player1, args.player2, args.timed)
        game.play_game()


if __name__ == "__main__":
    main()
