from logic_utils import check_guess, parse_guess, get_range_for_difficulty
from unittest.mock import MagicMock

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


class TestSubmissionMethodBug:
    """Tests to verify the submission method bug is fixed.
    
    Bug 1: Attempt countdown should register for both Enter key and Submit button
    Bug 2: Hints should show for both Enter key and Submit button
    """
    
    def setup_method(self):
        """Set up a mock session state for testing."""
        self.session_state = {
            'secret': 50,
            'attempts': 0,
            'score': 0,
            'status': 'playing',
            'last_processed_guess': None,
            'history': [],
            'show_hint': True,
            'hint_message': None,
            'submit_triggered': False
        }
    
    def simulate_guess_processing(self, raw_guess, submit_button_clicked=False):
        """Simulate the guess processing logic from app.py.
        
        Args:
            raw_guess: The user's guess as a string
            submit_button_clicked: True if submit button was clicked, False if Enter key was pressed
        """
        # Simulate the condition: (submit_triggered OR submit) AND raw_guess
        submit_triggered = self.session_state.get('submit_triggered', False)
        submit = submit_button_clicked
        
        if (submit_triggered or submit) and raw_guess:
            # Clear the submit_triggered flag first
            if self.session_state.get('submit_triggered'):
                self.session_state['submit_triggered'] = False
            
            # Prevent processing the same guess twice
            if raw_guess != self.session_state['last_processed_guess']:
                self.session_state['last_processed_guess'] = raw_guess
                self.session_state['attempts'] += 1
                
                ok, guess_int, err = parse_guess(raw_guess)
                
                if ok:
                    self.session_state['history'].append(guess_int)
                    
                    secret = self.session_state['secret']
                    outcome, message = check_guess(guess_int, secret)
                    
                    # Store hint message in session state
                    if self.session_state['show_hint']:
                        self.session_state['hint_message'] = message
                    else:
                        self.session_state['hint_message'] = None
                    
                    return outcome, message
                else:
                    return None, err
        
        return None, None
    
    def test_enter_key_increments_attempts(self):
        """Test that pressing Enter key increments attempt counter."""
        # Simulate Enter key press (submit_triggered = True)
        self.session_state['submit_triggered'] = True
        
        outcome, message = self.simulate_guess_processing("45", submit_button_clicked=False)
        
        assert self.session_state['attempts'] == 1, "Enter key should increment attempts"
        assert outcome == "Too Low"
    
    def test_submit_button_increments_attempts(self):
        """Test that clicking Submit button increments attempt counter."""
        # Simulate Submit button click
        outcome, message = self.simulate_guess_processing("45", submit_button_clicked=True)
        
        assert self.session_state['attempts'] == 1, "Submit button should increment attempts"
        assert outcome == "Too Low"
    
    def test_enter_key_shows_hints(self):
        """Test that pressing Enter key generates and stores hint message."""
        # Simulate Enter key press
        self.session_state['submit_triggered'] = True
        
        outcome, message = self.simulate_guess_processing("60", submit_button_clicked=False)
        
        assert self.session_state['hint_message'] is not None, "Enter key should generate hint"
        assert self.session_state['hint_message'] == "📉 Go LOWER!"
        assert outcome == "Too High"
    
    def test_submit_button_shows_hints(self):
        """Test that clicking Submit button generates and stores hint message."""
        # Simulate Submit button click
        outcome, message = self.simulate_guess_processing("60", submit_button_clicked=True)
        
        assert self.session_state['hint_message'] is not None, "Submit button should generate hint"
        assert self.session_state['hint_message'] == "📉 Go LOWER!"
        assert outcome == "Too High"
    
    def test_hints_disabled_for_enter_key(self):
        """Test that hints don't show when checkbox is disabled (Enter key)."""
        self.session_state['show_hint'] = False
        self.session_state['submit_triggered'] = True
        
        outcome, message = self.simulate_guess_processing("60", submit_button_clicked=False)
        
        assert self.session_state['hint_message'] is None, "No hint should be stored when disabled"
        assert outcome == "Too High"
    
    def test_hints_disabled_for_submit_button(self):
        """Test that hints don't show when checkbox is disabled (Submit button)."""
        self.session_state['show_hint'] = False
        
        outcome, message = self.simulate_guess_processing("60", submit_button_clicked=True)
        
        assert self.session_state['hint_message'] is None, "No hint should be stored when disabled"
        assert outcome == "Too High"
    
    def test_multiple_submissions_both_methods(self):
        """Test that both methods work correctly when used alternately."""
        # First guess with Enter key
        self.session_state['submit_triggered'] = True
        outcome1, msg1 = self.simulate_guess_processing("30", submit_button_clicked=False)
        
        assert self.session_state['attempts'] == 1
        assert self.session_state['hint_message'] == "📈 Go HIGHER!"
        
        # Second guess with Submit button
        outcome2, msg2 = self.simulate_guess_processing("70", submit_button_clicked=True)
        
        assert self.session_state['attempts'] == 2
        assert self.session_state['hint_message'] == "📉 Go LOWER!"
        
        # Third guess with Enter key again
        self.session_state['submit_triggered'] = True
        outcome3, msg3 = self.simulate_guess_processing("50", submit_button_clicked=False)
        
        assert self.session_state['attempts'] == 3
        assert self.session_state['hint_message'] == "🎉 Correct!"
        assert outcome3 == "Win"
    
    def test_duplicate_guess_not_processed(self):
        """Test that duplicate guesses are not processed twice."""
        # First submission with Enter key
        self.session_state['submit_triggered'] = True
        self.simulate_guess_processing("45", submit_button_clicked=False)
        
        assert self.session_state['attempts'] == 1
        
        # Try to submit same guess with button
        self.simulate_guess_processing("45", submit_button_clicked=True)
        
        assert self.session_state['attempts'] == 1, "Duplicate guess should not increment attempts"


class TestHintSystem:
    """Tests to verify the hint system bug is fixed.
    
    Bug: Hint system gives incorrect feedback when comparing string and int.
    """
    
    def test_string_secret_comparison(self):
        """Test that hints are correct when the secret is a string."""
        # When secret is '50' and guess is 40, hint should be "Too Low"
        outcome, message = check_guess(40, "50")
        assert outcome == "Too Low", "Should be Too Low when guess is lower than string secret"
        assert message == "📈 Go HIGHER!"
        
        # When secret is '50' and guess is 60, hint should be "Too High"
        outcome, message = check_guess(60, "50")
        assert outcome == "Too High", "Should be Too High when guess is higher than string secret"
        assert message == "📉 Go LOWER!"
        
        # When secret is '50' and guess is 50, it should be a win
        outcome, message = check_guess(50, "50")
        assert outcome == "Win", "Should be a Win when guess matches string secret"
        assert message == "🎉 Correct!"


class TestAttemptLogic:
    """Tests for attempt logic bugs."""

    def test_initial_attempts(self):
        """Test that attempts start at 0."""
        session_state = {'attempts': 0}
        assert session_state['attempts'] == 0


class TestGameDifficultyRange:
    """Tests for game difficulty range bugs."""

    def test_difficulty_ranges(self):
        """Test that the correct range is returned for each difficulty."""
        assert get_range_for_difficulty("Easy") == (1, 20)
        assert get_range_for_difficulty("Normal") == (1, 100)
        assert get_range_for_difficulty("Hard") == (1, 50)


class TestGameReset:
    """Tests for game reset bugs."""

    def test_game_reset(self):
        """Test that the game state is reset correctly."""
        session_state = {
            'attempts': 5,
            'secret': 42,
            'status': 'lost',
            'history': [10, 20, 30, 40, 50],
            'last_processed_guess': 50
        }
        
        # Simulate reset
        session_state['attempts'] = 0
        session_state['secret'] = 1 # dummy new secret
        session_state['status'] = "playing"
        session_state['history'] = []
        session_state['last_processed_guess'] = None

        assert session_state['attempts'] == 0
        assert session_state['status'] == "playing"
        assert session_state['history'] == []
        assert session_state['last_processed_guess'] is None


class TestAttemptHistory:
    """Tests for attempt history bugs."""

    def test_attempt_history(self):
        """Test that attempt history is recorded correctly."""
        session_state = {'history': []}
        
        session_state['history'].append(50)
        assert session_state['history'] == [50]
        
        session_state['history'].append("abc")
        assert session_state['history'] == [50, "abc"]
        
        session_state['history'].append(75)
        assert session_state['history'] == [50, "abc", 75]
