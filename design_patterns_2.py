"""
In this file, we improve the design in `design_patterns_1.py`.
"""
from design_patterns_1 import Human

"""
Platform Code
"""
from abc import ABC, abstractmethod
from typing import Self
import uuid
import random
import logging


class AgentState:
    ALIVE = 1
    INFECTED = 2
    DEAD = 3


class AgentType:
    HUMAN = 1
    ZOMBIE = 2


class IAgent:
    """
    The interface of agent.
    """
    def interact(self, selected_neighbor:Self) -> bool:
        pass

    def move(self) -> None:
        pass

    def get_aid(self):
        pass

    def get_state(self):
        pass

    def get_energy(self):
        pass

    def get_type(self):
        pass


"""
User Code
"""
class MyHuman(IAgent):
    """
    Custom human class.
    """

    """
    [private]
    !!!
    Inside this custom human class, it creates a hidden zombie instance.
    """
    __m_hidden_zombie = None

    def __init__(self):
        super().__init__()
        logging.info('[MyHuman:__init__] Create a MyHuman: %s' % self.get_aid())
        self.__m_hidden_zombie = ZombieGame().create_agent(AgentType.ZOMBIE)
        logging.info('[MyHuman:__init__] Create a hidden Zombie: %s' % self.__m_hidden_zombie.get_aid())

    def interact(self, selected_neighbor:Self) -> bool:
        """
        !!!
        This interact behavior is not a normal human behavior but in fact a zombie behavior. However, the user was not prevented from doing so.
        """
        logging.info('[MyHuman:interact] MyHuman interact. Neighbor type: %s' % selected_neighbor.get_type())
        # ----- Testing code starts -----
        if selected_neighbor.get_type() == AgentType.HUMAN:
            logging.error('[MyHuman:interact] Trying to bite a Human!')
        # ----- Testing code ends -----
        return self.__m_hidden_zombie.interact(selected_neighbor)


"""
Platform Code
"""
class ZombieGame:
    """
    The class for the Zombie Game.
    """

    class __Agent(IAgent):
        """
        The abstract class for agent.
        """

        """
        [private] 
        The unique ID of the agent.
        """
        __m_aid = None

        """
        [private] 
        The energy of the agent.
        """
        __m_energy = None

        """
        [private] 
        The state of the agent.
        """
        __m_state = None

        """
        [private]
        The type of the agent.
        """
        __m_type = None

        def __init__(self, type):
            self.__m_aid = uuid.uuid4()
            self.__m_energy = 100
            self.__m_state = AgentState.ALIVE
            self.__m_type = type

        def interact(self, selected_neighbor: Self) -> bool:
            """
            [public]
            This agent interacts with a selected neighbor agent.
            :param selected_neighbor: The selected neighbor agent.
            :return: True - The interaction succeeded.
            """
            return False

        def move(self) -> None:
            """
            [public]
            The agent moves to a new position.
            """
            pass

        def get_aid(self):
            """
            [public]
            """
            return self.__m_aid

        def get_energy(self):
            """
            [public]
            """
            return self.__m_energy

        def get_state(self):
            """
            [public]
            """
            return self.__m_state

        def get_type(self):
            """
            [public]
            """
            return self.__m_type

    class __Human(__Agent):
        """
        The default human class.
        """

        def __init__(self):
            super().__init__(AgentType.HUMAN)
            logging.info('[Human:__init__] Create a Human: %s' % self.get_aid())

        def interact(self, selected_neighbor: Self) -> bool:
            """
            Suppose Human can only interact with Human.
            """
            print('[Human:interact] Default Human interact. Neighbor type: %s' % selected_neighbor.get_type())
            # ----- Testing code starts-----
            if selected_neighbor.get_type() != AgentType.HUMAN:
                logging.error('[Human:interact] Trying to interact with Zombie!')
            # ----- Testing code ends -----
            return True

        def move(self) -> None:
            logging.info('[Human:move] Default Human move.')

    class __Zombie(__Agent):
        """
        The default zombie class.
        """

        def __init__(self):
            super().__init__(AgentType.ZOMBIE)
            logging.info('[Zombie:__init__] Create a Zombie: %s' % self.get_aid())

        def interact(self, selected_neighbor: Self) -> bool:
            """
            Suppose Zombie can only interact with Human.
            """
            logging.info('[Zombie:interact] Default Zombie interact. Neighbor type: %s' % selected_neighbor.get_type())
            # ----- Testing code starts-----
            if selected_neighbor.get_type() != AgentType.HUMAN:
                logging.error('[Zombie:interact] Trying to interact with Zombie!')
            # ----- Testing code ends -----
            return True

        def move(self) -> None:
            logging.info('[Zombie:move] Default Zombie move.')

    """
    [private]
    The collection of all agent instances.
    """
    __m_agents = []

    """
    [private]
    The singleton instance of the game.
    """
    __g_game_instance = None

    def __new__(cls, *args, **kwargs):
        """
        Implement a singleton instance pattern. In one process, only one instance is created.
        """
        if cls.__g_game_instance is None:
            cls.__g_game_instance = super().__new__(cls)
        return cls.__g_game_instance

    def __initialize_agents(self) -> None:
        """
        [private]
        """
        for i in range(10):
            self.__m_agents.append(self.__Human())
        for i in range(10):
            self.__m_agents.append(self.__Zombie())
        self.__m_agents.append(MyHuman())

    def create_agent(self, agent_type:int) -> [IAgent, None]:
        """
        [public]
        Create an agent instance.
        :param agent_type: The type of agent.
        :return: An agent instance. None, if `agent_type` is invalid.
        """
        if agent_type == AgentType.HUMAN:
            agent_ins = self.__Human()
        elif agent_type == AgentType.ZOMBIE:
            agent_ins = self.__Zombie()
        else:
            agent_ins = None
        return agent_ins

    def run(self):
        """
        [public]
        Run the game.
        """
        self.__initialize_agents()
        logging.info('[ZombieGame:run] Run the game.')
        for i in range(20):
            selected_neighbor = random.choice(self.__m_agents)
            if selected_neighbor.get_type() == AgentType.HUMAN:
                self.__m_agents[-1].interact(selected_neighbor)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    game_instance = ZombieGame()
    game_instance.run()