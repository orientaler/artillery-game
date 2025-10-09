from math import sin, cos, radians
import random


class Game:
    """This is the model of the game"""

    def __init__(self, cannon_size, ball_size):
        self.players = [Player(self, False, -90, "blue"), Player(self, True, 90, "red")]
        self.cannon_size = cannon_size
        self.ball_size = ball_size
        self.current_player_index = 0
        wind = random.random() * 20 - 10
        self.setCurrentWind(wind)

    def getPlayers(self):
        """A list containing both players"""
        return self.players

    def getCannonSize(self):
        """The height/width of the cannon"""
        return self.cannon_size

    def getBallSize(self):
        """The radius of cannon balls"""
        return self.ball_size

    def getCurrentPlayer(self):
        """The current player, i.e. the player whose turn it is"""
        currentPlayer = self.players[self.current_player_index]
        return currentPlayer

    def getOtherPlayer(self):
        """The opponent of the current player"""
        otherPlayer = self.players[not self.current_player_index]
        return otherPlayer

    def getCurrentPlayerNumber(self):
        """
        The number (0 or 1) of the current player. This should be the
        position of the current player in getPlayers().
        """
        return self.current_player_index

    def nextPlayer(self):
        """Switch active player"""
        if self.current_player_index:
            self.current_player_index = 0
        else:
            self.current_player_index = 1

    def setCurrentWind(self, wind):
        """Set the current wind speed, only used for testing"""
        self.currentWind = wind

    def getCurrentWind(self):
        """Get the current wind speed"""
        return self.currentWind

    def newRound(self):
        """Start a new round with a random wind value (-10 to +10)"""
        wind = random.random() * 20 - 10
        self.setCurrentWind(wind)


class Projectile:
    """
    Models a projectile (a cannonball, but could be used more generally)

    Constructor parameters:
    angle and velocity: the initial angle and velocity of the projectile
        angle 0 means straight east (positive x-direction) and 90 straight up
    wind: The wind speed value affecting this projectile
    xPos and yPos: The initial position of this projectile
    xLower and xUpper: The lowest and highest x-positions allowed
    """

    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity * cos(theta)
        self.yvel = velocity * sin(theta)
        self.wind = wind

    def update(self, time):
        """
        Advance time by a given number of seconds
        (typically, time is less than a second,
        for large values the projectile may move erratically)
        """
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8 * time
        xvel1 = self.xvel + self.wind * time

        # Move based on the average velocity in the time period
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0

        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)

        # Make sure xLower <= xPos <= mUpper
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)

        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1

    def isMoving(self):
        """A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits"""
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    def getY(self):
        """The current y-position (height) of the projectile". Should never be below 0."""
        return self.yPos


class Player:
    """Models a player"""

    def __init__(self, game: Game, isReversed: bool, xPos: int, color: str):
        self.game = game
        self.isReversed = isReversed
        self.xPos = xPos
        self.color = color
        self.score = 0
        self.aim = [45, 40]

    def fire(self, angle, velocity):
        """Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player."""
        if self.isReversed:
            angle = 180 - angle

        wind = self.game.getCurrentWind()
        startingXPos = self.getX()
        startingYPos = self.game.cannon_size / 2

        lowerXBound = -110
        upperXBound = 110

        self.aim = (angle, velocity)
        return Projectile(
            angle, velocity, wind, startingXPos, startingYPos, lowerXBound, upperXBound
        )

    def projectileDistance(self, proj: Projectile):
        """Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch (assuming the projectile is on the ground and factoring in both cannon and projectile size) this method should return 0"""
        halfCannonSize = self.game.cannon_size / 2
        halfProjSize = self.game.ball_size
        combinedSize = halfCannonSize + halfProjSize

        rawDistance = proj.getX() - self.getX()

        if abs(rawDistance) < combinedSize:
            return 0

        if rawDistance < 0:
            return rawDistance + combinedSize

        return rawDistance - combinedSize

    def getScore(self):
        """The current score of this player"""
        return self.score

    def increaseScore(self):
        """Increase the score of this player by 1."""
        self.score += 1

    def getColor(self):
        """Returns the color of this player (a string)"""
        return self.color

    def getX(self):
        """The x-position of the centre of this players cannon"""
        return self.xPos

    def getAim(self):
        """The angle and velocity of the last projectile this player fired, initially (45, 40)"""
        return self.aim
