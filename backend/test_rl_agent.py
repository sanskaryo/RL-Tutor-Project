"""
Unit Tests for RL Agent
Tests Q-Learning algorithm, state representation, and reward calculation
"""
import pytest
import numpy as np
import os
from app.services.rl_agent import RLAgent

# Test fixtures
@pytest.fixture
def agent():
    """Create a fresh RL agent for testing"""
    # Use a test Q-table file
    test_agent = RLAgent(q_table_file="test_q_table.pkl")
    yield test_agent
    # Cleanup
    if os.path.exists("test_q_table.pkl"):
        os.remove("test_q_table.pkl")


@pytest.fixture
def sample_state():
    """Sample student knowledge state"""
    return np.array([0.5, 0.3, 0.7, 0.2, 2.5])  # 4 topics + difficulty preference


@pytest.fixture
def sample_content():
    """Sample content list"""
    return [
        {'id': 1, 'topic': 'algebra', 'difficulty': 2},
        {'id': 2, 'topic': 'calculus', 'difficulty': 3},
        {'id': 3, 'topic': 'geometry', 'difficulty': 1},
        {'id': 4, 'topic': 'statistics', 'difficulty': 4},
    ]


class TestRLAgent:
    """Test suite for RL Agent"""

    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.learning_rate == 0.1
        assert agent.discount_factor == 0.9
        assert agent.exploration_rate == 0.1
        assert isinstance(agent.q_table, dict)

    def test_state_to_key(self, agent, sample_state):
        """Test state representation conversion"""
        key = agent._state_to_key(sample_state)
        assert isinstance(key, str)
        assert 'algebra' in key or '0.5' in key  # Should contain state info

    def test_get_q_value_new_state(self, agent, sample_state):
        """Test Q-value retrieval for new state-action pair"""
        action = 1
        q_value = agent.get_q_value(sample_state, action)
        assert q_value == 0.0  # New states should default to 0

    def test_set_q_value(self, agent, sample_state):
        """Test Q-value setting"""
        action = 1
        new_value = 0.85
        agent._set_q_value(sample_state, action, new_value)
        retrieved_value = agent.get_q_value(sample_state, action)
        assert retrieved_value == new_value

    def test_select_action_exploration(self, agent, sample_state, sample_content):
        """Test action selection with exploration"""
        # Force exploration by setting high exploration rate
        agent.exploration_rate = 1.0
        actions = [c['id'] for c in sample_content]
        
        # Run multiple times to check randomness
        selected_actions = set()
        for _ in range(20):
            action = agent.select_action(sample_state, actions)
            selected_actions.add(action)
        
        # With exploration, should try different actions
        assert len(selected_actions) > 1

    def test_select_action_exploitation(self, agent, sample_state, sample_content):
        """Test action selection with exploitation (greedy)"""
        # Set Q-values to prefer action 2
        agent._set_q_value(sample_state, 1, 0.5)
        agent._set_q_value(sample_state, 2, 0.9)  # Highest
        agent._set_q_value(sample_state, 3, 0.3)
        
        # Force exploitation
        agent.exploration_rate = 0.0
        actions = [1, 2, 3]
        
        action = agent.select_action(sample_state, actions)
        assert action == 2  # Should select highest Q-value

    def test_calculate_reward_correct_answer(self, agent):
        """Test reward calculation for correct answer"""
        reward = agent.calculate_reward(
            is_correct=True,
            time_spent=10.0,
            optimal_time=15.0,
            difficulty=2,
            student_knowledge=0.5
        )
        assert reward > 0  # Correct answer should give positive reward
        assert reward <= 1.5  # Should be within reasonable bounds

    def test_calculate_reward_incorrect_answer(self, agent):
        """Test reward calculation for incorrect answer"""
        reward = agent.calculate_reward(
            is_correct=False,
            time_spent=10.0,
            optimal_time=15.0,
            difficulty=2,
            student_knowledge=0.5
        )
        assert reward <= 0  # Incorrect answer should give negative or zero reward

    def test_calculate_reward_time_bonus(self, agent):
        """Test that faster answers get better rewards"""
        fast_reward = agent.calculate_reward(
            is_correct=True,
            time_spent=5.0,
            optimal_time=15.0,
            difficulty=2,
            student_knowledge=0.5
        )
        
        slow_reward = agent.calculate_reward(
            is_correct=True,
            time_spent=25.0,
            optimal_time=15.0,
            difficulty=2,
            student_knowledge=0.5
        )
        
        assert fast_reward >= slow_reward  # Faster should be better or equal

    def test_update_q_value(self, agent, sample_state):
        """Test Q-value update using Q-learning formula"""
        action = 1
        reward = 1.0
        next_state = np.array([0.6, 0.3, 0.7, 0.2, 2.5])  # Slightly improved
        next_actions = [1, 2, 3]
        
        # Set initial Q-value
        initial_q = 0.5
        agent._set_q_value(sample_state, action, initial_q)
        
        # Set Q-values for next state
        agent._set_q_value(next_state, 1, 0.6)
        agent._set_q_value(next_state, 2, 0.8)
        agent._set_q_value(next_state, 3, 0.4)
        
        # Update Q-value
        agent.update_q_value(sample_state, action, reward, next_state, next_actions)
        
        # Get updated Q-value
        updated_q = agent.get_q_value(sample_state, action)
        
        # Should have changed from initial value
        assert updated_q != initial_q
        
        # Should be moving towards reward + discounted max future Q
        # Q(s,a) = Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
        max_next_q = 0.8
        expected_delta = agent.learning_rate * (reward + agent.discount_factor * max_next_q - initial_q)
        expected_q = initial_q + expected_delta
        
        assert abs(updated_q - expected_q) < 0.001  # Should match formula

    def test_q_learning_convergence(self, agent, sample_state):
        """Test that Q-values converge with repeated updates"""
        action = 1
        reward = 1.0
        next_state = sample_state.copy()
        next_actions = [1]
        
        # Initial Q-value
        initial_q = agent.get_q_value(sample_state, action)
        
        # Perform many updates with same reward
        for _ in range(100):
            agent.update_q_value(sample_state, action, reward, next_state, next_actions)
        
        # Q-value should have converged close to reward
        final_q = agent.get_q_value(sample_state, action)
        
        # Should be closer to reward than initial value
        assert abs(final_q - reward) < abs(initial_q - reward)

    def test_save_and_load_q_table(self, agent, sample_state):
        """Test Q-table persistence"""
        # Set some Q-values
        agent._set_q_value(sample_state, 1, 0.75)
        agent._set_q_value(sample_state, 2, 0.85)
        
        # Save
        agent.save_q_table()
        
        # Create new agent (should load saved Q-table)
        new_agent = RLAgent(q_table_file="test_q_table.pkl")
        
        # Verify values were loaded
        assert new_agent.get_q_value(sample_state, 1) == 0.75
        assert new_agent.get_q_value(sample_state, 2) == 0.85

    def test_recommend_content(self, agent, sample_state, sample_content):
        """Test content recommendation"""
        # Set Q-values to prefer geometry
        agent._set_q_value(sample_state, 1, 0.5)
        agent._set_q_value(sample_state, 3, 0.9)  # Geometry - highest
        
        # Force exploitation
        agent.exploration_rate = 0.0
        
        # Get recommendation
        recommended = agent.recommend_content(sample_state, sample_content)
        
        assert recommended is not None
        assert recommended['id'] == 3  # Should recommend geometry

    def test_get_statistics(self, agent):
        """Test agent statistics retrieval"""
        stats = agent.get_statistics()
        
        assert 'q_table_size' in stats
        assert 'exploration_rate' in stats
        assert 'learning_rate' in stats
        assert 'discount_factor' in stats
        assert isinstance(stats['q_table_size'], int)


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_action_list(self, agent, sample_state):
        """Test behavior with empty action list"""
        with pytest.raises(ValueError):
            agent.select_action(sample_state, [])

    def test_invalid_state_shape(self, agent):
        """Test behavior with invalid state"""
        invalid_state = np.array([0.5, 0.3])  # Too short
        with pytest.raises((ValueError, IndexError)):
            agent.select_action(invalid_state, [1, 2, 3])

    def test_negative_reward(self, agent):
        """Test handling of negative rewards"""
        reward = agent.calculate_reward(
            is_correct=False,
            time_spent=100.0,
            optimal_time=15.0,
            difficulty=5,
            student_knowledge=0.1
        )
        assert reward <= 0  # Should handle negative rewards

    def test_extreme_knowledge_values(self, agent):
        """Test with knowledge at boundaries"""
        # Knowledge at 0
        reward_zero = agent.calculate_reward(
            is_correct=True,
            time_spent=10.0,
            optimal_time=15.0,
            difficulty=1,
            student_knowledge=0.0
        )
        
        # Knowledge at 1
        reward_one = agent.calculate_reward(
            is_correct=True,
            time_spent=10.0,
            optimal_time=15.0,
            difficulty=5,
            student_knowledge=1.0
        )
        
        assert reward_zero > 0
        assert reward_one > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
